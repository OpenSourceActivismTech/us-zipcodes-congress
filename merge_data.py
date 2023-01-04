import utils
import logging
import sys

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.WARNING)

def load_districts(fn):
    column_map = {
        'GEOID': 'tract',
        'CDFP': 'cd',
    }

    tract_list = utils.load_csv_columns(fn, column_map)
    # trim tract to block geoid, so we can use dict for faster lookup
    for tract in tract_list:
        tract['block'] = tract['tract'][:-4]

    blocks = utils.list_key_values(tract_list, 'block')
    return blocks

def load_tracts(fn):
    column_map = {
        'GEOID_TRACT_20': 'tract',
        'GEOID_ZCTA5_20': 'zcta',
    }

    tracts_list = utils.load_csv_columns(fn, column_map, delimiter='|')
    zcta = utils.list_key_values(tracts_list, 'zcta')
    return zcta

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

def merge_by_tract(cd_dict, zcta_dict):
    merged = []
    for (zcta, zcta_row) in zcta_dict.items():
        if not zcta:
            # skip initial blanks
            continue

        tract = zcta_row[0]['tract']

        matched_cds = cd_dict[tract]
        matched_list = list(m['cd'] for m in matched_cds)
        matched_unique = list(set(matched_list))

        for matched_cd in matched_unique:
            new_zcta = {'zcta': zcta, 'cd': matched_cd, 'state_fips': tract[:2]}
            log.info(new_zcta)
            merged.append(new_zcta)
    return merged

def state_fips_to_name(zccd):
    # append state abbreviation from FIPS
    for row in zccd:
        row['state_abbr'] = FIPS_TO_STATE[row['state_fips']]
    return zccd

def remove_district_padding(zccd):
    cleaned = []
    for row in zccd:
        if row['cd'] in ['null', '', 'ZZ']:
            # skip empty rows
            # ZZ means mostly water
            continue

        # non-voting districts are noted as 98 in census, but 0 in other sources
        if row['cd'] == '98':
            row['cd'] = 0

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
                log.info('zcta %s in %s should not start with %s, SKIPPING' % (row['zcta'], state, should_not_start_with))
                continue
        checked.append(row)
    return checked


FIPS_TO_STATE = {}
STATE_TO_FIPS = {}

if __name__ == "__main__":
    # load state FIPS codes
    FIPS_TO_STATE = load_fips('raw/state_fips.txt')
    STATE_TO_FIPS = {v: k for k, v in FIPS_TO_STATE.items()}

    # load national tract file
    tract_to_zcta = load_tracts('raw/zcta520_tract20_natl.txt')
    zccd_national = []

    for (state,fips) in STATE_TO_FIPS.items():
        # load statewide districts file
        cd_to_tract = load_districts(f"raw/cd118/{fips}_{state}_CD118.txt")

        # merge by the tract geoid
        zccd = merge_by_tract(cd_to_tract, tract_to_zcta)

        # clean output
        zccd_cleaned = remove_district_padding(zccd)

        # insert state abbreviation column
        zccd_named = state_fips_to_name(zccd_cleaned)

        print("got %s ZCTA->CD mappings for %s" % (len(zccd_named), state))
        zccd_national.extend(zccd_named)

    print("got %s ZCTA->CD mappings for %s" % (len(zccd_national), 'national'))

    # re-sort by state FIPS code
    zccd_sorted = sorted(zccd_national, key=lambda k: (k['state_fips'], k['zcta'], k['cd']))

        
    # write output
    utils.csv_writer('zccd.csv', zccd_national, ['state_fips', 'state_abbr', 'zcta', 'cd'])
