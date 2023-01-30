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

Local authority and regional level headline entry and attainment measures for the latest year broken down gender. State-funded schools only.

- URL: `https://explore-education-statistics.service.gov.uk/find-statistics/key-stage-4-performance-revised/2021-22`
- Original file: `data-raw/key-stage-4-performance-revised_2021-22.zip`
- Unzipped data: `data/KS4`
- Processed data (wide): `data/csv/ks4/`
- Processed data (long): `data/app/ks4.rds`

#### A-level
[https://explore-education-statistics.service.gov.uk/find-statistics/a-level-and-other-16-to-18-results](Source)

Included: all files with regional data

- Original file: `data-raw/a-level-and-other-16-to-18-results_2021-22.zip`
- Unzipped data: `data/A-level`
- Processed data (wide): `data/csv/a-level/`
- Processed data (long): `data/app/a-level.rds`

#### FE

[https://explore-education-statistics.service.gov.uk/find-statistics/further-education-and-skills](Source)

Included: all files with regional data and provider data

- Original file: `data-raw/further-education-and-skills_2021-22.zip`
- Unzipped file: `data/FE`
- Processed data (wide): `data/csv/fe/`
- Processed data (long): `data/app/fe.rds`

#### FE Destination Measures:

[https://explore-education-statistics.service.gov.uk/find-statistics/16-18-destination-measures](Source)

Included: all files with regional data and provider data

- Original file: `data-raw/16-18-destination-measures_2020-21.zip`
- Unzipped file: `data/FE_destination`
- Processed data (wide): `data/csv/fe_dest/`
- Processed data (long): `data/app/fe_dest.rds`

### HESA

HESA data is stored at persistent URLs, though the .csv links download a .zip.

[https://www.hesa.ac.uk/support/definitions/students](Source)

#### Change of data definitions
NB Three types of student record data file exist: 051, 054, 056
- 051 (student record) has been used for historic data, up to and including 18/19.
- 054 (alternative student record) is used for 19/20 to current latest (20/21), but 051 is also available for this period. Main difference is a different course classification system.
- 056 will be introduced for Future publications (21/22 onwards, due to drop in Feb 23) and will not have options of 051 or 054 available.

### HESA Students

#### Table 1 - HE student enrolments by HE provider 2014/15 to 2020/21 (051, 054)

- URL: `https://www.hesa.ac.uk/data-and-analysis/students/table-1.csv`
- Original file: `data/HESA/table-1/`
- Processed: `data/csv/he/table1.csv`
- Processed: `data/app/hesa1.rds`

#### Table 19 - HE qualifiers by HE provider and subject of study 2014/15 to 2018/19 (051)

- URL: `https://www.hesa.ac.uk/data-and-analysis/students/table-19.csv`
- Original file: `data/HESA/table-19/`
- Processed: `data/csv/he/table19.csv`
- Processed: `data/app/hesa19.rds`

#### Table 51 - HE qualifiers by HE provider and subject of study 2019/20 to 2020/21 (051, 054)

- URL: `https://www.hesa.ac.uk/data-and-analysis/students/table-51.csv`, `https://www.hesa.ac.uk/data-and-analysis/students/table-51-051.csv`
- Original file: `data/HESA/table-51/`, `data/HESA/table-51-051/`
- Processed: `data/csv/he/table51.csv`, `data/csv/he/table51-051.csv`
- Processed: `data/app/hesa51.rds`, `data/app/hesa51-051.rds`

#### Table 13 - HE student enrolments by HE provider and subject of study 2014/15 to 2018/19 (051)

- URL: `https://www.hesa.ac.uk/data-and-analysis/students/table-13.csv`
- Original file: `data/HESA/table-13/`
- Processed: `data/csv/he/table13.csv`
- Processed: `data/app/hesa13.rds`

#### Table 49 - HE student enrolments by HE provider and subject of study 2019/20 to 2020/21 (051, 054)

- URL: `https://www.hesa.ac.uk/data-and-analysis/students/table-49.csv`, `https://www.hesa.ac.uk/data-and-analysis/students/table-49-051.csv`
- Original file: `data/HESA/table-49/`, `data/HESA/table-49-051.csv`
- Processed: `data/csv/he/table49.csv/`, `data/csv/he/table49-051.csv`
- Processed: `data/app/hesa49.rds`, `data/app/hesa49-051.rds`

#### HESA Graduates

#### Graduates Table 1 - Graduate activities by provider and sex

- URL: `https://www.hesa.ac.uk/data-and-analysis/graduates/table-1.csv`

#### Graduates Table 6 - Graduate activities by provider

- URL: `https://www.hesa.ac.uk/data-and-analysis/graduates/table-6.csv`

#### Graduates Table 28 - Graduate activities by provider and subject area of degree

- URL: `https://www.hesa.ac.uk/data-and-analysis/graduates/table-28.csv`

### ONS/NOMIS

#### Business Register and Employment Survey

- Employees by sector and geography

#### United Kingdom Business Counts

- Number of enterprises by employees, sector and geography
- Number of enterprises by turnover, sector and geography
- Number of local units by employees, sector and geography

#### Annual Population Survey

- Number of employed, self-employed, unemployed, inactive, etc.

#### Workforce Jobs

- Number of jobs (official ONS measure)

### The Data City (and Lightcast)

Job Postings - Top Title & Skills by Sector / Geography

- Total Job Postings by Sector
- Total Job Postings by LA district
- Total Unique Job Postings by Sector
- Top 10 Titles
- Top 20 Skills
- Skills / Job Titles by Sector
- Ability to filter skills to specialized, common or certifications
- Ability to filter to LA district level
