from utils import load_csv_columns, list_key_set, list_key_values

if __name__ == "__main__":
    print "\t new, old"

    new_data = load_csv_columns('zccd.csv')
    old_data = load_csv_columns('raw/old_sunlight_districts.csv')
    print "length", len(new_data), len(old_data)
    print

    new_states = list_key_set(new_data, 'state_abbr')
    old_states = list_key_set(old_data, 'state')
    print "states", len(new_states), len(old_states)
    assert len(old_states.difference(new_states)) == 0
    assert len(new_states.difference(old_states)) == 0
    print

    new_zctas = list_key_set(new_data, 'zcta')
    old_zctas = list_key_set(old_data, 'zipcode')
    print "ZCTAs", len(new_zctas), len(old_zctas)
    # we should not be missing any old zctas
    assert len(old_zctas.difference(new_zctas)) == 0
    print "added", new_zctas.difference(old_zctas)
    print

    new_zcta_list = list_key_values(new_data, 'zcta')
    old_zcta_list = list_key_values(old_data, 'zipcode')
    cds_changed = 0
    states_changed = set()
    for (n, l) in sorted(new_zcta_list.items()):
        new_cd_set = list_key_set(l, 'cd')
        old_cd_set = list_key_set(old_zcta_list[n], 'house_district')
        if old_cd_set.symmetric_difference(new_cd_set):
            cds_changed += 1
            new_state = list_key_values(l,'state_abbr')
            old_state = list_key_values(old_zcta_list[n], 'state')
            print "%s was %s-%s now %s-%s" % (n, ','.join(old_state), ','.join(old_cd_set), ','.join(new_state), ','.join(new_cd_set))
            states_changed.update(new_state.keys())
            states_changed.update(old_state.keys())

    print "CDs changed",  cds_changed
    print "from states", states_changed
    print