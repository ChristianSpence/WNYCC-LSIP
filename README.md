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

Variables:
avg_att8           |  Average Attainment 8 score of all pupils
avg_ebaccaps       |  Average EBacc APS score per pupil
pt_ebacc_94        |  Percentage of pupils achieving the English Baccalaureate (grades 4 or above in English and maths, A*-C in unreformed subjects)
pt_ebacc_95        |  Percentage of pupils achieving the English Baccalaureate (grades 5 or above in English and maths, A*-C in unreformed subjects)
pt_ebacc_e_ptq_ee  |  Percentage of pupils entering the English Baccalaureate
pt_entbasics       |  Percentage of pupils entering English and Mathematics GCSEs
pt_l2basics_94     |  Percentage of pupils achieving grades 4 or above in English and Mathematics GCSEs
pt_l2basics_95     |  Percentage of pupils achieving grades 5 or above in English and Mathematics GCSEs
t_att8             |  Total sum of pupils Attainment 8 scores
t_ebacc_94         |  Total number of pupils achieving the English Baccalaureate (grades 4 or above in English and maths, A*-C in unreformed subjects)
t_ebacc_95         |  Total number of pupils achieving the English Baccalaureate (grades 5 or above in English and maths, A*-C in unreformed subjects)
t_ebacc_e_ptq_ee   |  Total number of pupils entering the English Baccalaureate
t_ebaccaps         |  Total EBacc APS score of pupils
t_entbasics        |  Total number of pupils entering English and Mathematics GCSEs
t_l2basics_94      |  Total number of pupils achieving grades 4 or above in English and Mathematics GCSEs
t_l2basics_95      |  Total number of pupils achieving grades 5 or above in English and Mathematics GCSEs
t_pupils           |  Total number of pupils at the end of key stage 4
t_schools          |  Total number of schools

#### A-level
[https://explore-education-statistics.service.gov.uk/find-statistics/a-level-and-other-16-to-18-results](Source)

Included: all files with regional data

- Original file: `data-raw/a-level-and-other-16-to-18-results_2021-22.zip`
- Unzipped data: `data/A-level`
- Processed data (wide): `data/csv/a-level/`
- Processed data (long): `data/app/a-level.rds`

Variables:

aps_per_entry_acad                                          |  APS per academic entry
aps_per_entry_agen                                          |  APS per applied general entry
aps_per_entry_alev                                          |  APS per A level entry
aps_per_entry_best3                                         |  APS per 'Best 3' entries
aps_per_entry_grade_acad                                    |  Average academic result
aps_per_entry_grade_agen                                    |  Average applied general result
aps_per_entry_grade_alev                                    |  Average A level result
aps_per_entry_grade_best3                                   |  APS per 'Best 3' entries (grade)
aps_per_entry_grade_technicalcertificate                    |  Average technical certificate result
aps_per_entry_grade_tlev                                    |  Average tech level result
aps_per_entry_technicalcertificate                          |  APS per entry technical certificate students
aps_per_entry_tlev                                          |  APS per tech level entry
characteristic_value                                        |  Characteristic
entered_any_level3_vocational_excluding_applied_generals    |  Number of students entered for any level 3 vocational (excluding applied generals)
entered_any_level3_vocational_excluding_tech_levels         |  Number of students entered for any level 3 vocational (excluding tech levels)
entered_for_one_or_more_alev                                |  Number of students entered for ≥ 1 A level
entered_for_one_or_more_alev_or_applied                     |  Number of students entered for ≥ 1 A level or applied A level
number_of_students_acad                                     |  Number of academic students
number_of_students_agen                                     |  Number of applied general students
number_of_students_alev                                     |  Number of A level students
number_of_students_highest_entry_was_l2                     |  Number of students with level 2 as highest entry
number_of_students_level3                                   |  Number of level 3 students
number_of_students_potential                                |  Students at end of 16-18 study
number_of_students_technicalcertificate                     |  Number of technical certificate students
number_of_students_tlev                                     |  Number of tech level students
pc_achieving_3_astar_to_a_alev                              |  % achieving 3 A* to A
pc_achieving_aab_or_better_alev                             |  % achieving ≥ AAB
pc_achieving_aab_or_better_atleast_two_facilitating_alev    |  % achieving ≥ AAB for a minimum of 2 facilitating A levels
pc_achieving_atleast_two_alev                               |  % achieving ≥ 2 A levels
pc_achieving_atleast_two_substantial_lev3                   |  % achieving ≥ 2 substantial level 3 results
pc_achieving_atleast_two_substantial_lev3_acad              |  % achieving ≥ 2 academic results
pc_level2_vocational_students_entered_technicalcertificate  |  % level 2 students entered for technical certificate
pc_level3_vocational_students_entered_applied_generals      |  % level 3 vocational students (excluding tech levels) who entered applied general
pc_level3_vocational_students_entered_tech_levels           |  % level 3 vocational students (excluding applied generals) who entered tech levels
school_type                                                 |  Institution

Single academic year:
a_grade_achieved             |  Number at grade A.
astar_grade_achieved         |  Number at grade A*.
b_grade_achieved             |  Number at grade B.
c_grade_achieved             |  Number at grade C.
d_grade_achieved             |  Number at grade D.
e_grade_achieved             |  Number at grade E.
entry_count                  |  Exam entries
perc_astar_a_grade_achieved  |  Percent achieving grade A* - A
perc_astar_b_grade_achieved  |  Percent achieving grade A* - B
perc_astar_c_grade_achieved  |  Percent achieving grade A* - C
perc_astar_d_grade_achieved  |  Percent achieving grade A* - D
perc_astar_e_grade_achieved  |  Percent achieving grade A* - E
perc_astar_grade_achieved    |  Percent achieving grade A*
qualification                |  Qualification
school_type                  |  Institution
subject_name                 |  Subject
u_grade_achieved             |  Number at grade U.

End of study:
a_grade_achieved             |  Number at grade A.
astar_grade_achieved         |  Number at grade A*.
b_grade_achieved             |  Number at grade B.
c_grade_achieved             |  Number at grade C.
d_grade_achieved             |  Number at grade D.
e_grade_achieved             |  Number at grade E.
perc_astar_a_grade_achieved  |  Percent achieving grade A* - A
perc_astar_b_grade_achieved  |  Percent achieving grade A* - B
perc_astar_c_grade_achieved  |  Percent achieving grade A* - C
perc_astar_d_grade_achieved  |  Percent achieving grade A* - D
perc_astar_e_grade_achieved  |  Percent achieving grade A* - E
perc_astar_grade_achieved    |  Percent achieving grade A*
school_type                  |  Institution
subject_name                 |  Subject
total_students               |  Total number of students
u_grade_achieved             |  Number at grade U.

number_alev_students      |  Number of students
pc_entered_1plus_MatScis  |  Percent entered for 1 or more STEM subjects
pc_entered_2plus_MatScis  |  Percent entered for 2 or more STEM subjects
pc_entered_3plus_MatScis  |  Percent entered for 3 or more STEM subjects
pc_entered_4plus_MatScis  |  Percent entered for 4 or more STEM subjects
pc_entered_5plus_MatScis  |  Percent entered for 5 or more STEM subjects
pc_entered_Biology        |  Percent entered for biology
pc_entered_Chemistry      |  Percent entered for chemistry
pc_entered_Computing      |  Percent entered for computing
pc_entered_FurtherMaths   |  Percent entered for further maths
pc_entered_Maths          |  Percent entered for maths
pc_entered_no_MatSci      |  Percent not entered for a STEM subject
pc_entered_Physics        |  Percent entered for physics

#### FE

[https://explore-education-statistics.service.gov.uk/find-statistics/further-education-and-skills](Source)

Included: all files with regional data and provider data

- Original file: `data-raw/further-education-and-skills_2021-22.zip`
- Unzipped file: `data/FE`
- Processed data (wide): `data/csv/fe/`
- Processed data (long): `data/app/fe.rds`

Variables:

Basic skills total participation and total achievements geographical breakdowns.
achievements     |  Achievements
age_youth_adult  |  Age (under 19/19+)
participation    |  Participation
subject_level    |  Subject and level

Community learning geographical breakdowns
ach_family_english_maths_and_language               |  Achievements Family english maths and language
ach_neighbourhood_learning_in_deprived_communities  |  Achievements Neighbourhood learning in deprived communities
ach_personal_and_community_development_learning     |  Achievements Personal and community development learning
ach_total                                           |  Total Achievements
ach_wider_family_learning                           |  Achievements Wider family learning
age_detailed                                        |  Age group (with unknowns)
ethnicity_group                                     |  Ethnicity group
family_english_maths_and_language                   |  Participation Family english maths and language
neighbourhood_learning_in_deprived_communities      |  Participation Neighbourhood learning in deprived communities
personal_and_community_development_learning         |  Participation Personal and community development learning
sex                                                 |  Sex
total                                               |  Total Participation
wider_family_learning                               |  Participation Wider family learning

Community learning detailed provider breakdowns
ach_feml   |  Achievement - Family english, maths and language
ach_nldc   |  Achievement - Neighbourhood learning in deprived communities
ach_pcdl   |  Achievement - Personal and community development learning
ach_total  |  Achievement - All community learning
ach_wfl    |  Achievement - Wider family learning
p_feml     |  Participation - Family english, maths and language
p_nldc     |  Participation - Neighbourhood learning in deprived communities
p_pcdl     |  Participation - Personal and community development learning
p_total    |  Participation - All community learning
p_wfl      |  Participation - Wider family learning

Adult (19+) Education and training learner participation and achievements detailed provider file
ach_basic_skills           |  Achievements Basic skills (Aug to Jul)
ach_bl2_ex_basic_skills    |  Achievements Below level 2 (excluding basic skills) (Aug to Jul)
ach_full_l2                |  Achievements Full level 2 (Aug to Jul)
ach_full_l3                |  Achievements Full level 3 (Aug to Jul)
ach_l2                     |  Achievements Level 2 (Aug to Jul)
ach_l3                     |  Achievements Level 3 (Aug to Jul)
ach_l4plus                 |  Achievements Level 4+ (Aug to Jul)
ach_no_lx                  |  Achievements No level assigned (Aug to Jul)
ach_total                  |  Total Achievements (Aug to Jul)
age_summary_with_unknowns  |  Age group (with unknowns)
ethnicity_group            |  Ethnicity group
p_basic_skills             |  Participation Basic skills (Aug to Jul)
p_bl2_ex_basic_skills      |  Participation Below level 2 (excluding basic skills) (Aug to Jul)
p_full_l2                  |  Participation Full level 2 (Aug to Jul)
p_full_l3                  |  Participation Full level 3 (Aug to Jul)
p_l2                       |  Participation Level 2 (Aug to Jul)
p_l3                       |  Participation Level 3 (Aug to Jul)
p_l4plus                   |  Participation Level 4+ (Aug to Jul)
p_no_lx                    |  Participation No level assigned (Aug to Jul)
p_total                    |  Total Participation (Aug to Jul)
sex                        |  Sex

Adult (19+) Education and Training aim enrolments and and achievements English devolved area breakdowns
e_and_t_aims_ach         |  Aim Achievements (Aug to Jul)
e_and_t_aims_enrolments  |  Aim Enrolments (Aug to Jul)
ethnicity_group          |  Ethnicity group
notional_nvq_level       |  Detailed level
sex                      |  Sex
ssa_t1_desc              |  Sector subject area (tier 1)

Adult (19+) Education and Training aim enrolments detailed provider breakdowns
enrols       |  Enrolments
level        |  Level
ssa_t1_desc  |  Sector subject area (tier 1)

Further education and skills detailed geography summary. The file figures for adult (19+) Further education and skills, 19+ Education and training, Community Learning, and all age apprenticeships.
achievements                              |  Achievements
achievements_rate_per_100000_population   |  Indicative achievements rate per 100,000 population
age_group                                 |  Age group
apprenticeships_or_further_education      |  Apprenticeships or further education
level_or_type                             |  Level or type
participation                             |  Participation
participation_rate_per_100000_population  |  Indicative participation rate per 100,000 population
starts                                    |  Starts
starts_rate_per_100000_population         |  Indicative starts rate per 100,000 population

Adult (19+) Further education and skills learner participation by region summary.
p_basic_skills         |  Participation Basic skills (Aug to Jul)
p_bl2_ex_basic_skills  |  Participation Below level 2 (excluding basic skills) (Aug to Jul)
p_full_l2              |  Participation Full level 2 (Aug to Jul)
p_full_l3              |  Participation Full level 3 (Aug to Jul)
p_l2                   |  Participation Level 2 (Aug to Jul)
p_l3                   |  Participation Level 3 (Aug to Jul)
p_l4plus               |  Participation Level 4+ (Aug to Jul)
p_no_lx                |  Participation No level assigned (Aug to Jul)
p_total                |  Total Participation (Aug to Jul)

Free courses for jobs detailed
employment_status                  |  Employment status
ethnicity                          |  Ethnicity
lldd                               |  LLDD
prior_attainment_group             |  Prior attainment group
sex                                |  Sex
ssa_t1                             |  Sector subject area (tier 1)
ssa_t2                             |  Sector subject area (tier 2)
start_age                          |  Start age
total_takeup_extended_adult_offer  |  Free courses for jobs total starts including extended offer (April 21 to July 22)
total_takeup_original_adult_offer  |  Free courses for jobs total starts under original offer (April 21 to July 22)

Adult (19+) Education and training learner participation and achievements detailed provider file
ach_basic_skills         |  Achievements Basic skills
ach_bl2_ex_basic_skills  |  Achievements Below level 2 (excluding basic skills)
ach_full_l2              |  Achievements Full level 2
ach_full_l3              |  Achievements Full level 3
ach_l2                   |  Achievements Level 2
ach_l3                   |  Achievements Level 3
ach_l4plus               |  Achievements Level 4+
ach_no_lx                |  Achievements No level assigned
ach_total                |  Total Achievements
p_basic_skills           |  Participation Basic skills
p_bl2_ex_basic_skills    |  Participation Below level 2 (excluding basic skills)
p_full_l2                |  Participation Full level 2
p_full_l3                |  Participation Full level 3
p_l2                     |  Participation Level 2
p_l3                     |  Participation Level 3
p_l4plus                 |  Participation Level 4+
p_no_lx                  |  Participation No level assigned
p_total                  |  Total Participation

#### FE Destination Measures:

[https://explore-education-statistics.service.gov.uk/find-statistics/16-18-destination-measures](Source)

Included: all files with regional data and provider data

- Original file: `data-raw/16-18-destination-measures_2020-21.zip`
- Unzipped file: `data/FE_destination`
- Processed data (wide): `data/csv/fe_dest/`
- Processed data (long): `data/app/fe_dest.rds`

Variables:

Local authority level destinations data for students leaving 16 to 18 study for different characteristic groups, provider types, and qualification levels.
all_notsust         |  Not recorded as a sustained destination
all_unknown         |  Activity not captured
all_work            |  Sustained employment destination
appl2               |  Intermediate apprenticeships (level 2)
appl3               |  Advanced apprenticeships (level 3)
appl4               |  Higher and degree apprenticeships (level 4 and above)
appren              |  Sustained apprenticeships
characteristic      |  Student characteristic
cohort              |  Number of pupils completing 16-18 study
cohort_level_group  |  Qualification level
data_type           |  Data type
education           |  Sustained education destination
fe                  |  Further education
fel1                |  FE entry level and no identified level
fel2                |  FE Level 2
fel3                |  FE Level 3
he                  |  UK higher education institution
institution_group   |  Institution group
level_methodology   |  Level based on LEA area or provider location
other_edu           |  Other education destinations
overall             |  Sustained education, apprenticeship or employment

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
