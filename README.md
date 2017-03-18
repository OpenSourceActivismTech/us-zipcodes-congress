# US Zipcodes to Congressional Districts

Mapping between US zipcode tabulation areas and Federal Congressional districts.


## Why is this necessary?

There are many commercial sources of zipcode data available, and some of them include congressional representatives. There are also several APIs to look up a congressperson based on an address, or a lat/lon point. However, phone based contact methods like [CallPower](https://github.com/spacedogXYZ/call-power) require a fast and free way to match a person to their rep, ideally without requiring them to type in a full address. Thus, we still need zipcodes.

### Caveats
- USPS zipcodes are not an exact match to Census-designated ZCTAs
- ZCTAs may span states and congressional districts
- If you have the ability to look up districts from a full address or zip+4, (you should)[https://sunlightfoundation.com/2012/01/19/dont-use-zipcodes/].

## How does this work?

We start with the most recent Census mapping for the 116th Congress, which includes redistricting in 2016 for FL, MN, NC and VA. It does not however include data for states and territories with at-large representation (AK, DE, MT, ND, SD, VT, WY, PR, and DC). We  add all available ZCTAs for those states as well at the US Minor Outlying Islands, using 2010 data. This is unfortunately the latest available. We de-duplicate this data, ensuring not to alter ZCTAs that span state lines. We also clean it, to remove unsightly `null` strings, and obviously incorrect values in Colorado that start with `000`.

We are left with a reasonably clean dataset. When tested against older publically available ones from [Sunlight](https://sunlightlabs.github.io/congress/#zip-codes-to-congressional-districts) (`RIP`), we show that we are not missing any ZCTAs, and have updated 1079 out of 39435 to new congressional districts. Run `make test` to see exact changes.

## Data Sources

- [2016 US Gazetteer](https://www.census.gov/geo/maps-data/data/gazetteer2016.html)
- [2010 ZCTA Relationships](https://www.census.gov/geo/maps-data/data/zcta_rel_overview.html)
- [Guam Zip Codes](http://mcog.guam.gov/guam_zip_codes.html)