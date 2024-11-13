all: clean zccd.csv

clean:
	rm -rf raw/*
	rm -f zccd.csv

zccd.csv: raw/cd119 raw/zcta520_tract20_natl.txt raw/state_fips.txt
	python merge_data.py

zccd_hud.csv: raw/hud_crosswalk.xlsx
	python hud_crosswalk.py

# Districts for 119th Congress
raw/cd119:
	curl "https://www2.census.gov/programs-surveys/decennial/rdo/mapping-files/2025/119-congressional-district-befs/cd119.zip" -o raw/cd119.zip
	unzip raw/cd119.zip -d raw/cd119

# 2020 ZCTA to census block
raw/zcta520_tract20_natl.txt:
	curl 'https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_tract20_natl.txt' -o $@

# FIPS State/Territory codes to names
raw/state_fips.txt:
	curl 'https://www2.census.gov/geo/docs/reference/state.txt' -o $@

# HUD data from Q2 2024
# available only under USPS sublicense - see readme
raw/hud_crosswalk.xlsx:
	curl 'https://www.huduser.gov/apps/public/uspscrosswalk/download_file/ZIP_CD_062024.xlsx' -o $@

# test against previously released data from Sunlight Foundation
test: raw/old_sunlight_districts.csv
	python test.py

raw/old_sunlight_districts.csv:
	curl 'https://raw.githubusercontent.com/OpenSourceActivismTech/call-power/0ee10f026d2c0758e49a786b43b980c1c2d1d4c7/call_server/political_data/data/us_districts.csv' -o $@.download
	mv $@.download $@.raw
	echo 'zipcode,state,house_district' >> raw/old_sunlight_headers.txt
	cat raw/old_sunlight_headers.txt $@.raw > $@
	rm raw/old_sunlight_headers.txt $@.raw