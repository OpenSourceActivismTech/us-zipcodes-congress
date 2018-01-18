# US Zipcodes to Congressional Districts

Mapping between US zipcode tabulation areas and Federal Congressional districts.


## Why is this necessary?

There are many commercial sources of zipcode data available, and some of them include congressional representatives. There are also several APIs to look up a congressperson based on an address, or a lat/lon point. However, phone based contact methods like [CallPower](https://github.com/spacedogXYZ/call-power) require a fast and free way to match a person to their rep, ideally without requiring them to type in a full address. Thus, we still need zipcodes.

### Caveats
- Zipcodes are not area designations, they are linear routes designed for mail delivery. The US Census delineates boundaries with the [most frequently used](https://www.census.gov/geo/reference/zcta/zcta_delin_anim.html) zipcode within an tract area, but they have not released an official zipcode to ZCTA map since 2000.
- Census ZCTAs are not an exact match to USPS zipcodes, because they are not produced for lightly populated areas. However 'in most instances the ZCTA code is the same as the ZIP Code for an area.' [US Census, 2015](https://www.census.gov/geo/reference/zctas.html)
- In 2000, the ZCTA delineation process excluded 10,068 ZIP codes, including 2,523 ZIP Codes that served specific companies or organizations with high volumes of mail and 6,419 ZIP Codes dedicated to Post Office (PO) Box and/or general delivery addresses. [ASDC 2010](http://cber.cba.ua.edu/asdc/zip_zcta.html)
- ZCTAs may span states and congressional districts. 'Nearly 15 percent of all ZIP codes cross congressional district boundaries.' [ZipInfo](https://www.zipinfo.com/products/cdz/cdz.htm) 'There are 153 ZIP Codes in more than one state.' [US Census, 1994](https://www.census.gov/population/www/documentation/twps0007/twps0007.html)
- If you have the ability to look up districts from a full address or zip+4, [you should](https://sunlightfoundation.com/2012/01/19/dont-use-zipcodes/). If you are still interested in matching zipcode to US Congressional District, read on.

## How does this work?

We start with the most recent Census mapping for the 115th Congress, which includes redistricting in 2016 for FL, MN, NC and VA. It does not however include data for states and territories with at-large representation (AK, DE, MT, ND, SD, VT, WY, PR, and DC). We  add all available ZCTAs for those states as well at the US Minor Outlying Islands, using 2010 data. This is unfortunately the latest available. We de-duplicate this data, ensuring not to alter ZCTAs that span state lines. We also clean it, to remove unsightly `null` strings, and obviously incorrect values in Colorado that start with `000`.

We are left with a reasonably clean dataset. When tested against older publically available ones from the [Sunlight Foundation](https://sunlightlabs.github.io/congress/#zip-codes-to-congressional-districts]) (`RIP`) and [18F](https://github.com/18F/openFEC/blob/master/data/natl_zccd_delim.csv), we show that we are not missing any ZCTAs, and have updated 1079 out of 39435 to new congressional districts. Run `make test` to see exact changes.

We have also included a crosswalk file [sourced from HUD](https://www.huduser.gov/portal/datasets/usps_crosswalk.html#codebook), parsed from Excel and split to match the format of the above file. This may be more complete, as it is derived from in the quarterly [USPS Vacancy Data](https://www.huduser.gov/portal/datasets/usps.html) and last updated in September 2017. It is available only for government entities and non-profit organizations related to the ["stated purpose"](https://www.huduser.gov/portal/usps/sublicense_agreement.html#statedpurpose) of the HUD Sublicensing Agreement (*measuring and forecasting neighborhood changes, assessing neighborhood needs, and measuring/assessing various HUD programs*).

## Data Sources

- [2016 US Gazetteer](https://www.census.gov/geo/maps-data/data/gazetteer2016.html)
- [2010 ZCTA Relationships](https://www.census.gov/geo/maps-data/data/zcta_rel_overview.html)
- [Guam Zip Codes](http://mcog.guam.gov/guam_zip_codes.html)
- [HUD USPS ZIP code Crosswalk](https://www.huduser.gov/portal/datasets/usps_crosswalk.html#data)
- Checked against state overlaps noted on [GIS StackExchange](http://gis.stackexchange.com/questions/53918/determining-which-us-zipcodes-map-to-more-than-one-state-or-more-than-one-city)

### More about ZIP codes and ZCTA
- US Census. How ZCTAs are Created [census.gov](https://www.census.gov/geo/reference/zctas.html)
- USPS Fun Facts [USPS.com](https://about.usps.com/who-we-are/postal-facts/fun-facts.htm)
- WTF Zipcodes [Ian Dees](https://github.com/iandees/wtf-zipcodes)
- Don't Use Zip Codes Unless You Have To. [Tom Lee, Sunlight Foundation, 2012](https://sunlightfoundation.com/2012/01/19/dont-use-zipcodes/)
- Using Zipcodes for epidemiological analysis can be harmful. [Grubesic and Matisziw, 2006](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1762013/)
- How ZIP codes nearly masked the lead problem in Flint. [Sadler, 2016](http://theconversation.com/how-zip-codes-nearly-masked-the-lead-problem-in-flint-65626)