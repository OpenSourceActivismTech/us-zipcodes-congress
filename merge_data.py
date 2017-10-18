import utils
import logging
import collections

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())

def load_zccd(fn):
    column_map = {
        'State': 'state_fips',
        'ZCTA': 'zcta',
        'Congressional District': 'cd'
    }

    zccd = utils.load_csv_columns(fn, column_map, skip=1)
    return zccd

def load_fips(fn):
    column_map = {
        'STATE': 'state_fips',
        'STUSAB': 'state',
    }
    fips_data = utils.load_csv_columns(fn, column_map, delimiter='|')
    fips_dict = {}
    for row in fips_data:
        fips_dict[row['state_fips']] = row['state']
    return fips_dict

def append_missing_zips(zccd, states_list):
    states_fips = []
    for s in states_list:
        states_fips.append(STATE_TO_FIPS[s])

    # load zcta_county_rel, which has full entries for each state
    column_map = {
        'ZCTA5': 'zcta',
        'STATE': 'state_fips'
    }
    all_zips_list = utils.load_csv_columns('raw/zcta_county_rel_10.txt', column_map)
    missing_zips_states = collections.defaultdict(set)

    for z in all_zips_list:
        # dedupe with a defaultdict
        if z['state_fips'] in missing_zips_states[z['zcta']]:
            log.error('zcta %s already in %s' % (z['zcta'], z['state_fips']))
            continue
        else:
            missing_zips_states[z['zcta']].add(z['state_fips'])

        if z['state_fips'] in states_fips:
            zccd.append({
                'zcta': z['zcta'],
                'state_fips': z['state_fips'],
                'cd': '0' # at-large
            })

    # also include zipcodes from US Minor and Outlying Islands
    # which are not included in the zcta_county_rel file
    # these are copied from govt websites as available
    missing_islands = {
        'AS': ['96799'],
        'GU': ['96910', '96913', '96915', '96916', '96917', '96921', '96928', '96929', '96931', '96932'],
        'MP': ['96950', '96951', '96952'],
        'VI': ['00801', '00802', '00820', '00823', '00824', '00830', '00831','00841', '00840', '00850', '00851'],
        'PR': ['00981'] # not sure why this isn't in the country_rel, because there are a bunch of others listed
    }

    for (abbr, zcta_list) in missing_islands.items():
        for z in zcta_list:
            zccd.append({
                    'zcta': z,
                    'state_fips': STATE_TO_FIPS[abbr],
                    'state_abbr': abbr,
                    'cd': '0', # at-large
                })

    # Include some zipcodes that have small populations (so no ZCTA) but are otherwise noteworthy
    # from https://about.usps.com/who-we-are/postal-facts/fun-facts.htm
    # There are ~2,500 others used exclusively by businesses, but we don't have a list.
    missing_small_zips = {
        'NY': {
            '00501': '1', # Holtsville has IRS processing center with lowest zip
            '00544': '1', #
            '12345': '20' # Schenectady has GE plant with memorable zip
            },
        'AK': {
            '99950': '0', # Ketchikan has highest zip 
        },
        'TX': {
            '78599': '15' # near US-Mexico border
        }
    }

    for (abbr, zcta_cd_dict) in missing_small_zips.items():
        for (z, cd) in zcta_cd_dict.items():
            zccd.append({
                    'zcta': z,
                    'state_fips': STATE_TO_FIPS[abbr],
                    'state_abbr': abbr,
                    'cd': cd,
                })

    return zccd

def state_fips_to_name(zccd):
    # append state abbreviation from FIPS
    merged = {}
    for row in zccd:
        row['state_abbr'] = FIPS_TO_STATE[row['state_fips']]
    return zccd

def remove_district_padding(zccd):
    cleaned = []
    for row in zccd:
        if row['cd'] == 'null':
            # natl_zccd_delim includes several rows with 'null' for uninhabited areas
            # skip them
            continue
        row['cd'] = str(int(row['cd']))
        # do this weird conversion to get rid of zero padding
        cleaned.append(row)
    return cleaned

def sanity_check(zccd, incorrect_states_dict):
    # there are entries which are clearly inaccurate
    checked = []
    for row in zccd:
        state = row['state_abbr']
        if state in incorrect_states_dict.keys():            
            should_not_start_with = incorrect_states_dict[state]
            if row['zcta'].startswith(should_not_start_with):
                log.warning('zcta %s in %s should not start with %s, SKIPPING' % (row['zcta'], state, should_not_start_with))
                continue
        checked.append(row)
    return checked


FIPS_TO_STATE = {}
STATE_TO_FIPS = {}

if __name__ == "__main__":
    # load state FIPS codes
    FIPS_TO_STATE = load_fips('raw/state_fips.txt')
    STATE_TO_FIPS = {v: k for k, v in FIPS_TO_STATE.iteritems()}

    # load national zccd file
    zccd_missing = load_zccd('raw/natl_zccd_delim.txt')

    # append zipcodes for at-large states
    at_large_states = ['AK', 'DE', 'MT', 'ND', 'SD', 'VT', 'WY', 'PR', 'DC']
    zccd_complete = append_missing_zips(zccd_missing, at_large_states)

    # clean output
    zccd_cleaned = remove_district_padding(zccd_complete)

    # insert state abbreviation column
    zccd_named = state_fips_to_name(zccd_cleaned)

    # and sanity check to remove obvious outliers
    zccd_checked = sanity_check(zccd_named, {'CO': '0'})

    # re-sort by state FIPS code
    zccd_sorted = sorted(zccd_checked, key=lambda k: k['state_fips'])

    # write output
    utils.csv_writer('zccd.csv', zccd_sorted, ['state_fips', 'state_abbr', 'zcta', 'cd'])