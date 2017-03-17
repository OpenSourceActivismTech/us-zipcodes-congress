all: clean zccd.csv

clean:
	rm -f raw/*.txt raw/*.zip
	rm -f zccd.csv

zccd.csv: raw/natl_zccd_delim.txt  raw/zcta_county_rel_10.txt raw/state_fips.txt
	python merge_data.py

# Congressional districts by zip code tabulation area (ZCTA) national, comma delimited
# NB: does not include at-large districts for AK, DE, MT, ND, SD, VT, WY, PR or DC
raw/natl_zccd_delim.txt:
	curl "http://www2.census.gov/geo/relfiles/cdsld16/natl/natl_zccd_delim.txt" -o raw/natl_zccd_delim.txt

# 2010 ZCTA to state & county
# TODO, try to find an updated version
raw/zcta_county_rel_10.txt:
	curl 'http://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt' -o $@

# FIPS State/Territory codes to names
raw/state_fips.txt:
	curl 'http://www2.census.gov/geo/docs/reference/state.txt' -o $@
