all: clean zccd.csv

clean:
	rm -f raw/*
	rm -f zccd.csv

zccd.csv: raw/cd118 raw/zcta520_tract20_natl.txt raw/state_fips.txt
	python merge_data.py

zccd_hud.csv: raw/hud_crosswalk.xlsx
	python hud_crosswalk.py

# Districts for 118th Congress, post redistricting
raw/cd118:
	curl "https://www2.census.gov/programs-surveys/decennial/rdo/mapping-files/2023/118-congressional-district-bef/cd118.zip" -o raw/cd118.zip
	unzip raw/cd118.zip -d raw/cd118

# 2020 ZCTA to census block
raw/zcta520_tract20_natl.txt:
	curl 'https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_tract20_natl.txt' -o $@

# FIPS State/Territory codes to names
raw/state_fips.txt:
	curl 'https://www2.census.gov/geo/docs/reference/state.txt' -o $@

# HUD data from Q4 2021
# available only under USPS sublicense - see readme
raw/hud_crosswalk.xlsx:
	curl 'https://www.huduser.gov/portal/datasets/usps/ZIP_CD_122021.xlsx' -o $@

# test against previously released data from Sunlight Foundation
test: raw/old_sunlight_districts.csv
	python test.py

raw/old_sunlight_districts.csv:
	curl 'https://raw.githubusercontent.com/OpenSourceActivismTech/call-power/0ee10f026d2c0758e49a786b43b980c1c2d1d4c7/call_server/political_data/data/us_districts.csv' -o $@.download
	mv $@.download $@.raw
	echo 'zipcode,state,house_district' >> raw/old_sunlight_headers.txt
	cat raw/old_sunlight_headers.txt $@.raw > $@
	rm raw/old_sunlight_headers.txt $@.raw