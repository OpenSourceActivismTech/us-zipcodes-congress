all: clean zccd.csv

clean:
	rm -f raw/*
	rm -f zccd.csv

zccd.csv: raw/natl_zccd_delim.txt  raw/zcta_county_rel_10.txt raw/state_fips.txt
	python merge_data.py

zccd_hud.csv: raw/hud_crosswalk.xlsx
	python hud_crosswalk.py

# Congressional districts by zip code tabulation area (ZCTA) national, comma delimited
# NB: does not include at-large districts for AK, DE, MT, ND, SD, VT, WY, PR or DC
raw/natl_zccd_delim.txt:
	curl "https://www2.census.gov/geo/relfiles/cdsld16/natl/natl_zccd_delim.txt" -o raw/natl_zccd_delim.txt

# 2010 ZCTA to state & county
# TODO, try to find an updated version
raw/zcta_county_rel_10.txt:
	curl 'https://www2.census.gov/geo/docs/maps-data/data/rel/zcta_county_rel_10.txt' -o $@

# FIPS State/Territory codes to names
raw/state_fips.txt:
	curl 'https://www2.census.gov/geo/docs/reference/state.txt' -o $@

# HUD data from Q4 2018
# available only under USPS sublicense - see readme
raw/hud_crosswalk.xlsx:
	curl 'https://www.huduser.gov/portal/datasets/usps/ZIP_CD_092018.xlsx' -o $@

# test against previously released data from Sunlight Foundation
test: raw/old_sunlight_districts.csv
	python test.py

raw/old_sunlight_districts.csv:
	curl 'https://raw.githubusercontent.com/OpenSourceActivismTech/call-power/0ee10f026d2c0758e49a786b43b980c1c2d1d4c7/call_server/political_data/data/us_districts.csv' -o $@.download
	mv $@.download $@.raw
	echo 'zipcode,state,house_district' >> raw/old_sunlight_headers.txt
	cat raw/old_sunlight_headers.txt $@.raw > $@
	rm raw/old_sunlight_headers.txt $@.raw