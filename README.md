# WNYCC-LSIP

West & North Yorkshire Chamber of Commerce Local Skills Improvement Plans

## Data

Data for this project is collected from four main locations:

- Department for Education Statistics (school and further education)
- Higher Education Statistics Agency (universities)
- Office for National Statistics (via NOMIS) (employment and business data)
- The Data City (including Lightcast data) (individual company-level data and job advertisement/skills data)

In the first phase, data is aggregated from the first three sources to allow the client to determine exactly which data variables are needed. Raw downloaded data from the sources us saved in `/data-raw`, processed via scripts stored in `/R`, with final datasets saved in `/data`. A Shiny web application that allows quick investigation of the data is provided in `/app`.

Sources and data transformations for each of the four main locations is described here.

### Department for Education

DfE data is not directly queryable, instead selected from menus  [https://explore-education-statistics.service.gov.uk/find-statistics](here).

Each downloaded .zip file contains a `data` folder and a `data-guidance` folder. The latter includes meta data and variable name lookups which are extracted in the scripts for each data source and joined to the `data` file.

#### Key Stage 4

- KS4 local authority data
Original file: `data-raw/key-stage-4-performance-revised_2021-22.zip`
Unzipped data: `data/KS4`
Processed data (wide): `data/csv/ks4/`
Processed data (long): `data/app/ks4.rds`

#### A-level
[https://explore-education-statistics.service.gov.uk/find-statistics/a-level-and-other-16-to-18-results](Source)

Original file: `data-raw/a-level-and-other-16-to-18-results_2021-22.zip`
Unzipped data: `data/A-level`
Processed data (wide): `data/csv/a-level/`
Processed data (long): `data/app/a-level.rds`

#### FE

[https://explore-education-statistics.service.gov.uk/find-statistics/further-education-and-skills](Source)

Original file: `data-raw/further-education-and-skills_2021-22.zip`
Unzipped file: `data/FE`
Processed data (wide): `data/csv/fe/`
Processed data (long): `data/app/fe.rds`

#### FE Destination Measures:

[https://explore-education-statistics.service.gov.uk/find-statistics/16-18-destination-measures](Source)

Original file: `data-raw/16-18-destination-measures_2020-21.zip`
Unzipped file: `data/FE_destination`
Processed data (wide): `data/csv/fe_dest/`
Processed data (long): `data/app/fe_dest.rds`

### HESA

HESA data is stored at persistent URLs.

[https://www.hesa.ac.uk/support/definitions/students](Source)

#### Change of data definitions
NB Three types of student record data file exist: 051, 054, 056
- 051 (student record) has been used for historic data, up to and including 18/19.
- 054 (alternative student record) is used for 19/20 to current latest (20/21), but 051 is also available for this period. Main difference is a different course classification system.
- 056 will be introduced for Future publications (21/22 onwards, due to drop in Feb 23) and will not have options of 051 or 054 available.

#### Table 51

URL: `https://www.hesa.ac.uk/data-and-analysis/students/table-51.csv`
Original file: `data/HESA/table-51/`
Processed: `data/csv/he/table51.csv`
Processed: `data/app/hesa51.rds`

#### Table 1

URL: `https://www.hesa.ac.uk/data-and-analysis/students/table-1.csv`
Original file: `data/HESA/table-1/`
Processed: `data/csv/he/table1.csv`
Processed: `data/app/hesa1.rds`

#### Table 13

URL: `https://www.hesa.ac.uk/data-and-analysis/students/table-13.csv`
Original file: `data/HESA/table-13`
Processed: `data/csv/he/table13.csv`
Processed: `data/app/hesa13.rds`



