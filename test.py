import utils

def list_key_set(data, key):
	s = set()
	for d in data:
		try:
			s.add(d[key])
		except KeyError:
			print d
			break
	return s

if __name__ == "__main__":
	print "\t new, old"

	new_data = utils.load_csv_columns('zccd.csv')
	old_data = utils.load_csv_columns('raw/old_sunlight_districts.csv')
	print "length", len(new_data), len(old_data)

	new_zctas = list_key_set(new_data, 'zcta')
	old_zctas = list_key_set(old_data, 'zipcode')
	print "zctas", len(new_zctas), len(old_zctas)
	print "new missing", old_zctas.difference(new_zctas)
	print "old missing", new_zctas.difference(old_zctas)

	new_states = list_key_set(new_data, 'state_abbr')
	old_states = list_key_set(old_data, 'state')
	print "states", len(new_states), len(old_states)
	print "new missing", old_states.difference(new_states)
	print "old missing", new_states.difference(old_states)