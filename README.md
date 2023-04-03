# WNYCC-LSIP

West & North Yorkshire Chamber of Commerce Local Skills Improvement Plans

## Data

Data for this project is collected from four main locations:

- Department for Education Statistics (school and further education)
- Higher Education Statistics Agency (universities)
- Office for National Statistics (via NOMIS) (employment and business data)
- The Data City (including Lightcast data) (individual company-level data and job advertisement/skills data)

In the first phase, data is aggregated from the first three sources to allow the client to determine exactly which data variables are needed. Raw downloaded data from the sources us saved in `/data-raw`, processed via scripts stored in `/R`, with final datasets saved in `/data`. A Shiny web application that allows quick investigation of the data is provided in `/app`.

The data processing pipelines are located in `/site/_pipelines` and the data which gets used in the final charts is saved in `/wycc/supply` and `wycc/demand`. There are identical locations under `/site/nycc`.

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

Variables:
- Average Attainment 8 score of all pupils
- Average EBacc APS score per pupil
- Percentage of pupils achieving the English Baccalaureate (grades 4 or above in English and maths, A*-C in unreformed subjects)
- Percentage of pupils achieving the English Baccalaureate (grades 5 or above in English and maths, A*-C in unreformed subjects)
- Percentage of pupils entering the English Baccalaureate
- Percentage of pupils entering English and Mathematics GCSEs
- Percentage of pupils achieving grades 4 or above in English and Mathematics GCSEs
- Percentage of pupils achieving grades 5 or above in English and Mathematics GCSEs
- Total sum of pupils Attainment 8 scores
- Total number of pupils achieving the English Baccalaureate (grades 4 or above in English and maths, A*-C in unreformed subjects)
- Total number of pupils achieving the English Baccalaureate (grades 5 or above in English and maths, A*-C in unreformed subjects)
- Total number of pupils entering the English Baccalaureate
- Total EBacc APS score of pupils
- Total number of pupils entering English and Mathematics GCSEs
- Total number of pupils achieving grades 4 or above in English and Mathematics GCSEs
- Total number of pupils achieving grades 5 or above in English and Mathematics GCSEs
- Total number of pupils at the end of key stage 4
- Total number of schools

#### A-level
[https://explore-education-statistics.service.gov.uk/find-statistics/a-level-and-other-16-to-18-results](Source)

Included: all files with regional data

- Original file: `data-raw/a-level-and-other-16-to-18-results_2021-22.zip`
- Unzipped data: `data/A-level`
- Processed data (wide): `data/csv/a-level/`
- Processed data (long): `data/app/a-level.rds`

Variables:

- APS per academic entry
- APS per applied general entry
- APS per A level entry
- APS per 'Best 3' entries
- Average academic result
- Average applied general result
- Average A level result
- APS per 'Best 3' entries (grade)
- Average technical certificate result
- Average tech level result
- APS per entry technical certificate students
- APS per tech level entry
- Characteristic
- Number of students entered for any level 3 vocational (excluding applied generals)
- Number of students entered for any level 3 vocational (excluding tech levels)
- Number of students entered for ≥ 1 A level
- Number of students entered for ≥ 1 A level or applied A level
- Number of academic students
- Number of applied general students
- Number of A level students
- Number of students with level 2 as highest entry
- Number of level 3 students
- Students at end of 16-18 study
- Number of technical certificate students
- Number of tech level students
- % achieving 3 A* to A
- % achieving ≥ AAB
- % achieving ≥ AAB for a minimum of 2 facilitating A levels
- % achieving ≥ 2 A levels
- % achieving ≥ 2 substantial level 3 results
- % achieving ≥ 2 academic results
- % level 2 students entered for technical certificate
- % level 3 vocational students (excluding tech levels) who entered applied general
- % level 3 vocational students (excluding applied generals) who entered tech levels
- Institution

Single academic year:
- Number at grade A.
- Number at grade A*.
- Number at grade B.
- Number at grade C.
- Number at grade D.
- Number at grade E.
- Exam entries
- Percent achieving grade A* - A
- Percent achieving grade A* - B
- Percent achieving grade A* - C
- Percent achieving grade A* - D
- Percent achieving grade A* - E
- Percent achieving grade A*
- Qualification
- Institution
- Subject
- Number at grade U.

End of study:
- Number at grade A.
- Number at grade A*.
- Number at grade B.
- Number at grade C.
- Number at grade D.
- Number at grade E.
- Percent achieving grade A* - A
- Percent achieving grade A* - B
- Percent achieving grade A* - C
- Percent achieving grade A* - D
- Percent achieving grade A* - E
- Percent achieving grade A*
- Institution
- Subject
- Total number of students
- Number at grade U.

- Number of students
- Percent entered for 1 or more STEM subjects
- Percent entered for 2 or more STEM subjects
- Percent entered for 3 or more STEM subjects
- Percent entered for 4 or more STEM subjects
- Percent entered for 5 or more STEM subjects
- Percent entered for biology
- Percent entered for chemistry
- Percent entered for computing
- Percent entered for further maths
- Percent entered for maths
- Percent not entered for a STEM subject
- Percent entered for physics

#### FE

[https://explore-education-statistics.service.gov.uk/find-statistics/further-education-and-skills](Source)

Included: all files with regional data and provider data

- Original file: `data-raw/further-education-and-skills_2021-22.zip`
- Unzipped file: `data/FE`
- Processed data (wide): `data/csv/fe/`
- Processed data (long): `data/app/fe.rds`

Variables:

Basic skills total participation and total achievements geographical breakdowns.
<<<<<<< HEAD
- Achievements
- Age (under 19/19+)
- Participation
- Subject and level

Community learning geographical breakdowns
- Achievements Family english maths and language
- Achievements Neighbourhood learning in deprived communities
- Achievements Personal and community development learning
- Total Achievements
- Achievements Wider family learning
- Age group (with unknowns)
- Ethnicity group
- Participation Family english maths and language
- Participation Neighbourhood learning in deprived communities
- Participation Personal and community development learning
- Sex
- Total Participation
- Participation Wider family learning

Community learning detailed provider breakdowns
- Achievement - Family english, maths and language
- Achievement - Neighbourhood learning in deprived communities
- Achievement - Personal and community development learning
- Achievement - All community learning
- Achievement - Wider family learning
- Participation - Family english, maths and language
- Participation - Neighbourhood learning in deprived communities
- Participation - Personal and community development learning
- Participation - All community learning
- Participation - Wider family learning

Adult (19+) Education and training learner participation and achievements detailed provider file
- Achievements Basic skills (Aug to Jul)
- Achievements Below level 2 (excluding basic skills) (Aug to Jul)
- Achievements Full level 2 (Aug to Jul)
- Achievements Full level 3 (Aug to Jul)
- Achievements Level 2 (Aug to Jul)
- Achievements Level 3 (Aug to Jul)
- Achievements Level 4+ (Aug to Jul)
- Achievements No level assigned (Aug to Jul)
- Total Achievements (Aug to Jul)
- Age group (with unknowns)
- Ethnicity group
- Participation Basic skills (Aug to Jul)
- Participation Below level 2 (excluding basic skills) (Aug to Jul)
- Participation Full level 2 (Aug to Jul)
- Participation Full level 3 (Aug to Jul)
- Participation Level 2 (Aug to Jul)
- Participation Level 3 (Aug to Jul)
- Participation Level 4+ (Aug to Jul)
- Participation No level assigned (Aug to Jul)
- Total Participation (Aug to Jul)
- Sex

Adult (19+) Education and Training aim enrolments and and achievements English devolved area breakdowns
- Aim Achievements (Aug to Jul)
- Aim Enrolments (Aug to Jul)
- Ethnicity group
- Detailed level
- Sex
- Sector subject area (tier 1)

Adult (19+) Education and Training aim enrolments detailed provider breakdowns
- Enrolments
- Level
- Sector subject area (tier 1)

Further education and skills detailed geography summary. The file figures for adult (19+) Further education and skills, 19+ Education and training, Community Learning, and all age apprenticeships.
- Achievements
- Indicative achievements rate per 100,000 population
- Age group
- Apprenticeships or further education
- Level or type
- Participation
- Indicative participation rate per 100,000 population
- Starts
- Indicative starts rate per 100,000 population

Adult (19+) Further education and skills learner participation by region summary.
- Participation Basic skills (Aug to Jul)
- Participation Below level 2 (excluding basic skills) (Aug to Jul)
- Participation Full level 2 (Aug to Jul)
- Participation Full level 3 (Aug to Jul)
- Participation Level 2 (Aug to Jul)
- Participation Level 3 (Aug to Jul)
- Participation Level 4+ (Aug to Jul)
- Participation No level assigned (Aug to Jul)
- Total Participation (Aug to Jul)

Free courses for jobs detailed
- Employment status
- Ethnicity
- LLDD
- Prior attainment group
- Sex
- Sector subject area (tier 1)
- Sector subject area (tier 2)
- Start age
- Free courses for jobs total starts including extended offer (April 21 to July 22)
- Free courses for jobs total starts under original offer (April 21 to July 22)

Adult (19+) Education and training learner participation and achievements detailed provider file
- Achievements Basic skills
- Achievements Below level 2 (excluding basic skills)
- Achievements Full level 2
- Achievements Full level 3
- Achievements Level 2
- Achievements Level 3
- Achievements Level 4+
- Achievements No level assigned
- Total Achievements
- Participation Basic skills
- Participation Below level 2 (excluding basic skills)
- Participation Full level 2
- Participation Full level 3
- Participation Level 2
- Participation Level 3
- Participation Level 4+
- Participation No level assigned
- Total Participation

- Achievements
- Age (under 19/19+)
- Participation
- Subject and level

Community learning geographical breakdowns
- Achievements Family english maths and language
- Achievements Neighbourhood learning in deprived communities
- Achievements Personal and community development learning
- Total Achievements
- Achievements Wider family learning
- Age group (with unknowns)
- Ethnicity group
- Participation Family english maths and language
- Participation Neighbourhood learning in deprived communities
- Participation Personal and community development learning
- Sex
- Total Participation
- Participation Wider family learning

Community learning detailed provider breakdowns
- Achievement - Family english, maths and language
- Achievement - Neighbourhood learning in deprived communities
- Achievement - Personal and community development learning
- Achievement - All community learning
- Achievement - Wider family learning
- Participation - Family english, maths and language
- Participation - Neighbourhood learning in deprived communities
- Participation - Personal and community development learning
- Participation - All community learning
- Participation - Wider family learning

Adult (19+) Education and training learner participation and achievements detailed provider file
- Achievements Basic skills (Aug to Jul)
- Achievements Below level 2 (excluding basic skills) (Aug to Jul)
- Achievements Full level 2 (Aug to Jul)
- Achievements Full level 3 (Aug to Jul)
- Achievements Level 2 (Aug to Jul)
- Achievements Level 3 (Aug to Jul)
- Achievements Level 4+ (Aug to Jul)
- Achievements No level assigned (Aug to Jul)
- Total Achievements (Aug to Jul)
- Age group (with unknowns)
- Ethnicity group
- Participation Basic skills (Aug to Jul)
- Participation Below level 2 (excluding basic skills) (Aug to Jul)
- Participation Full level 2 (Aug to Jul)
- Participation Full level 3 (Aug to Jul)
- Participation Level 2 (Aug to Jul)
- Participation Level 3 (Aug to Jul)
- Participation Level 4+ (Aug to Jul)
- Participation No level assigned (Aug to Jul)
- Total Participation (Aug to Jul)
- Sex

Adult (19+) Education and Training aim enrolments and and achievements English devolved area breakdowns
- Aim Achievements (Aug to Jul)
- Aim Enrolments (Aug to Jul)
- Ethnicity group
- Detailed level
- Sex
- Sector subject area (tier 1)

Adult (19+) Education and Training aim enrolments detailed provider breakdowns
- Enrolments
- Level
- Sector subject area (tier 1)

Further education and skills detailed geography summary. The file figures for adult (19+) Further education and skills, 19+ Education and training, Community Learning, and all age apprenticeships.
- Achievements
- Indicative achievements rate per 100,000 population
- Age group
- Apprenticeships or further education
- Level or type
- Participation
- Indicative participation rate per 100,000 population
- Starts
- Indicative starts rate per 100,000 population

Adult (19+) Further education and skills learner participation by region summary.
- Participation Basic skills (Aug to Jul)
- Participation Below level 2 (excluding basic skills) (Aug to Jul)
- Participation Full level 2 (Aug to Jul)
- Participation Full level 3 (Aug to Jul)
- Participation Level 2 (Aug to Jul)
- Participation Level 3 (Aug to Jul)
- Participation Level 4+ (Aug to Jul)
- Participation No level assigned (Aug to Jul)
- Total Participation (Aug to Jul)

Free courses for jobs detailed
- Employment status
- Ethnicity
- LLDD
- Prior attainment group
- Sex
- Sector subject area (tier 1)
- Sector subject area (tier 2)
- Start age
- Free courses for jobs total starts including extended offer (April 21 to July 22)
- Free courses for jobs total starts under original offer (April 21 to July 22)

Adult (19+) Education and training learner participation and achievements detailed provider file
- Achievements Basic skills
- Achievements Below level 2 (excluding basic skills)
- Achievements Full level 2
- Achievements Full level 3
- Achievements Level 2
- Achievements Level 3
- Achievements Level 4+
- Achievements No level assigned
- Total Achievements
- Participation Basic skills
- Participation Below level 2 (excluding basic skills)
- Participation Full level 2
- Participation Full level 3
- Participation Level 2
- Participation Level 3
- Participation Level 4+
- Participation No level assigned
- Total Participation

#### FE Destination Measures:

[https://explore-education-statistics.service.gov.uk/find-statistics/16-18-destination-measures](Source)

Included: all files with regional data and provider data

- Original file: `data-raw/16-18-destination-measures_2020-21.zip`
- Unzipped file: `data/FE_destination`
- Processed data (wide): `data/csv/fe_dest/`
- Processed data (long): `data/app/fe_dest.rds`

Variables:

Local authority level destinations data for students leaving 16 to 18 study for different characteristic groups, provider types, and qualification levels.

- Not recorded as a sustained destination
- Activity not captured
- Sustained employment destination
- Intermediate apprenticeships (level 2)
- Advanced apprenticeships (level 3)
- Higher and degree apprenticeships (level 4 and above)
- Sustained apprenticeships
- Student characteristic
- Number of pupils completing 16-18 study
- Qualification level
- Data type
- Sustained education destination
- Further education
- FE entry level and no identified level
- FE Level 2
- FE Level 3
- UK higher education institution
- Institution group
- Level based on LEA area or provider location
- Other education destinations
- Sustained education, apprenticeship or employment

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

- URL: `https://www.nomisweb.co.uk/api/v01/dataset/NM_189_1.data.csv?geography=1811939398,1811939399,1811939387...1811939389,1811939400,1811939401,1811939390...1811939393,1811939402,1811939386&industry=150994945...150994965&employment_status=4&measure=1&measures=20100`
- Original file: `data-raw/NOMIS/bres.csv`


#### United Kingdom Business Counts

- Number of enterprises by employees, sector and geography

- URL: `https://www.nomisweb.co.uk/api/v01/dataset/NM_142_1.data.csv?geography=1811939398,1811939399,1811939387...1811939389,1811939400,1811939401,1811939390...1811939393,1811939402,1811939386&industry=150994945...150994965&employment_sizeband=0,10,20,30,40&legal_status=0&measures=20100`
- Original file: `data-raw/NOMIS/ukbc-emp`

- Number of enterprises by turnover, sector and geography
- URL: `https://www.nomisweb.co.uk/api/v01/dataset/NM_199_1.data.csv?geography=1811939398,1811939399,1811939387...1811939389,1811939400,1811939401,1811939390...1811939393,1811939402,1811939386&industry=150994945...150994965&turnover_sizeband=0...10&legal_status=0&measures=20100`
- Original file: `data-raw/NOMIS/ukbc-turn.csv`

- Number of local units by employees, sector and geography

- URL: `https://www.nomisweb.co.uk/api/v01/dataset/NM_141_1.data.csv?geography=1811939398,1811939399,1811939387...1811939389,1811939400,1811939401,1811939390...1811939393,1811939402,1811939386&industry=150994945...150994965&employment_sizeband=10,20,30,40&legal_status=0&measures=20100`
- Original file: `data-raw/NOMIS/ukbc-lu-emp.csv`

#### Annual Population Survey

Number of employed, self-employed, unemployed, inactive, etc.

Variables:

- Economic activity by age
- Economic activity by disability (Disability Discrimination Act) 16-64
- Economic activity by disability (Equality Act) 16-64
- Economic activity of those with health problems lasting more than 12 months
- Economic activity of those with health conditions or illnesses lasting more than 12 months
- Economic activity by ethnic group and country of birth
- Economic activity by ethnic group and nationality
- Economic activity from age of 18
- Economic inactivity
- Employment by age and full-time/part-time
- Employment by occupation (SOC2020) sub-major group and full-time/part-time
- Employment by occupation (SOC2020) and industry (SIC 2007)
- Employment by occupation (SOC2020) and flexibility
- Employment by occupation (SOC2020) and ethnic group
- Employment by occupation (SOC2010) sub-major group and full-time/part-time
- Employment by occupation (SOC2010) and industry (SIC 2007)
- Employment by age and industry (SIC 2007)
- Employment by occupation (SOC2010) and flexibility
- Employment by industry (SIC 2007) and flexibility
- Employment by industry (SIC 2007) and ethnic group
- Employment by occupation (SOC2010) and ethnic group
- Second jobs by industry (SIC 2007)
- Usual hours worked
- Ethnicity by age
- Qualification by age - NVQ
- Qualification by age - GCSE
- Job related training (SIC 2007)
- Methods of jobsearch by age
- National Identity
- Welsh Language
- Employment by public/private sector

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
