import utils
import logging

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())

def load_zccd(fn):
    column_map = {
        'State': 'state_fips',
        'ZCTA': 'zcta',
        'Congressional District': 'house_district'
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

def append_missing_zips(zccd, states_list, fips):
    # flip state abbr list back to fips codes
    fips_dict_invert = {v: k for k, v in fips.iteritems()}
    states_fips = []
    for s in states_list:
        states_fips.append(fips_dict_invert[s])

    # load zcta_county_rel, which has full entries for each state
    column_map = {
        'ZCTA5': 'zcta',
        'STATE': 'state_fips'
    }
    all_zips = utils.load_csv_columns('raw/zcta_county_rel_10.txt', column_map)

    for z in all_zips:
        if z['state_fips'] in states_fips:
            zccd.append({
                'zcta': z['zcta'],
                'state_fips': z['state_fips'],
                'house_district': '0' # at-large
            })

    return zccd

def fips_to_state(zccd, fips):
    # append state abbreviation from 
    merged = {}
    for row in zccd:
        row['state_abbr'] = fips[row['state_fips']]
    return zccd

def remove_district_padding(zccd):
    cleaned = []
    for row in zccd:
        if row['house_district'] == 'null':
            # natl_zccd_delim includes several rows with 'null' for uninhabited areas in Maine
            # skip them
            continue
        row['house_district'] = str(int(row['house_district']))
        # do this weird conversion to get rid of zero padding
        cleaned.append(row)
    return cleaned

if __name__ == "__main__":
    # load state FIPS codes
    fips = load_fips('raw/state_fips.txt')

    # load national zccd file
    zccd_missing = load_zccd('raw/natl_zccd_delim.txt')

    # append zipcodes for at-large states
    at_large_states = ['AK', 'DE', 'MT', 'ND', 'SD', 'VT', 'WY', 'PR', 'DC']
    zccd_complete = append_missing_zips(zccd_missing, at_large_states, fips)

    # clean output
    zccd_cleaned = remove_district_padding(zccd_complete)

    # re-sort by state FIPS code
    zccd_sorted = sorted(zccd_cleaned, key=lambda k: k['state_fips'])

    # insert state abbreviation column
    zccd_named = fips_to_state(zccd_sorted, fips)

    # write output
    utils.csv_writer('zccd.csv', zccd_named, ['state_fips', 'state_abbr', 'zcta', 'house_district'])