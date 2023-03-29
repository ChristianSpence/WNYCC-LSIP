# Defines all LAD codes for the projects
geog_codes <- list(wy = paste0("E080000", 32:36),
                   ny = c("E06000014", # York
                          paste0("E070001", 63:69), # Craven:Selby
                          "E10000023" # North Yorkshire (A-level and FE Dest)
                   )
)

# Transforms academic years of format "202122" into "2021/22"
academic_year <- function(x) {
  return(paste(substr(x, 1, 4), substr(x, 5, 6), sep = "/"))
}


# Renames column names in wide format to match those from the meta data files, i.e. full descriptive names rather than short codes
rename_variables <- function(df, lookup) {
  temp <- data.frame(original = names(df))
  temp <- dplyr::left_join(temp, lookup, by = c("original" = "Variable name"))
  names(temp) <- c("original", "new")
  temp <- temp |>
    dplyr::mutate(new = dplyr::coalesce(new, original))
  out <- df
  names(out) <- temp$new
  return(out)
}

# Contains all the different dimensions that various datasets use and we need, to enable reshaping of only variables in datasets into a long format for Shiny app
dimensions <- c("date",
                "geography_name", "geography_code",
                "school_type_group", "school_type",
                "characteristic_type", "characteristic_value",
                "school_type_group", "school_type",
                "subject_area", "subject_name",
                "subject_level", "age_youth_adult",
                "age_detailed", "sex", "ethnicity_group",
                "age_summary_with_unknowns",
                "ssa_t1_desc",
                "notional_nvq_level",
                "apprenticeships_or_further_education",
                "level_or_type", "age_group",
                "start_age", "prior_attainment_group",
                "employment_status", "lldd", "ethnicity",
                "ssa_t1", "ssa_t2",
                "institution_group", "institution_type",
                "cohort_level_group", "cohort_level",
                "characteristic_group", "characteristic",
                "data_type")

# Contains all the dimensions in datasets that we can discard
dims_to_remove <- c("time_identifier", "geographic_level",
                    "country_code", "country_name",
                    "region_code", "region_name",
                    "pcon_code", "pcon_name",
                    "version",
                    "old_la_code",
                    "english_devolved_area_code", "english_devolved_area_name",
                    "opportunity_area_code", "opportunity_area_name",
                    "level_methodology")

# KS4 ---------------------------------------------------------------------
ks4_lookup <- readr::read_delim("data/KS4/data-guidance/data-guidance.txt",
                                delim = "|", trim_ws = TRUE,
                                skip = 26) |>
  dplyr::filter(!is.na(`Variable description`), !grepl("---", `Variable description`), `Variable description` != "Variable description") |>
  dplyr::distinct()

# write ks4 lookup
readr::write_csv(ks4_lookup, "data/csv/lookups/ks4.csv")

ks4 <- readr::read_csv("data/KS4/data/2122_lad_pr_data.csv") |>
  dplyr::filter(lad_code %in% c(geog_codes$wy, geog_codes$ny)) |>
  dplyr::select(-dplyr::any_of(dims_to_remove)) |>
  dplyr::rename(date = time_period,
                geography_code = lad_code,
                geography_name = lad_name) |>
  dplyr::mutate(date = academic_year(date))

# write geography lookup
readr::write_csv(dplyr::select(ks4, geography_code, geography_name),
                 "data/csv/lookups/geography.csv")

# write ks4 csv with changed variable names
ks4 |>
  rename_variables(ks4_lookup) |>
  readr::write_csv("data/csv/ks4/Key stage 4 performance.csv")

ks4 |>
  tidyr::pivot_longer(cols = -(dplyr::any_of(dimensions)),
                      names_to = "variable_code") |>
  dplyr::inner_join(ks4_lookup, by = c("variable_code" = "Variable name")) |>
  dplyr::rename(variable_name = `Variable description`) |>
  saveRDS("data/app/ks4.rds")


# A level -----------------------------------------------------------------

a_level_lookup <- readr::read_delim("data/A-level/data-guidance/data-guidance.txt",
                                    delim = "|", trim_ws = TRUE,
                                    skip = 28) |>
  dplyr::filter(!is.na(`Variable description`), !grepl("---", `Variable description`), `Variable description` != "Variable description") |>
  dplyr::distinct()


a_level <- lapply(list.files("data/A-level/data", full.names = TRUE),
                  function(file) {
                    readr::read_csv(file, col_types = readr::cols(.default = readr::col_character()),
                                    na = c("c", "z")) |>
                      dplyr::select(-dplyr::any_of(dims_to_remove)) |>
                      dplyr::rename(date = time_period,
                                    geography_code = new_la_code,
                                    geography_name = la_name) |>
                      dplyr::mutate(date = academic_year(date)) |>
                      dplyr::filter(geography_code %in% c(geog_codes$wy,
                    geog_codes$ny))
                  }) |>
  setNames(basename(list.files("data/A-level/data")))

a_level_names <- c("Attainment and other performance measures - region and student characteristics",
                   "Entries and Results - A level and AS by region and subject",
                   "Student counts and Results - A level by region and subject (end of 16-18 study)",
                   "Maths and science entries - percent entered by region"
                   )

for (i in seq_along(a_level)) {
  rename_variables(a_level[[i]], a_level_lookup) |>
  readr::write_csv(paste0("data/csv/a-level/", a_level_names[i], ".csv"))
}

a_level |>
  lapply(function(df) {
    df |>
      tidyr::pivot_longer(cols = -(dplyr::any_of(dimensions)),
                          names_to = "variable_code") |>
      dplyr::left_join(a_level_lookup,
                       by = c("variable_code" = "Variable name")) |>
      dplyr::rename(variable_name = `Variable description`)
  }) |>
  saveRDS("data/app/a-level.rds")

# FE ----------------------------------------------------------------------

fe_lookup <- readr::read_delim("data/FE/data-guidance/data-guidance.txt",
                               delim = "|", trim_ws = TRUE,
                               skip = 28) |>
  dplyr::filter(!is.na(`Variable description`), !grepl("---", `Variable description`), `Variable description` != "Variable description") |>
  dplyr::distinct()

fe <- lapply(list.files("data/FE/data", full.names = TRUE),
             function(file) {
               # currently ignoring providers as we have no geo lookup for them
               if (!grepl("provider|geography-summary", file)) {
                 readr::read_csv(file,
                                 na = c("z"),
                                 col_types = readr::cols(
                                   .default = readr::col_character())) |>
                   dplyr::select(-dplyr::any_of(dims_to_remove)) |>
                   dplyr::rename(date = time_period,
                                 geography_code = lad_code,
                                 geography_name = lad_name) |>
                   dplyr::mutate(date = academic_year(date)) |>
                   dplyr::filter(geography_code %in% c(geog_codes$wy,
                                                       geog_codes$ny))
               }

             }) |>
  setNames(basename(list.files("data/FE/data")))

fe_names <- c("Basic skills - regional breakdown",
              "Community learning geography - local authority district",
              "Education and training geography - English devolved areas",
              "Education and training geography - local authority district",
              NA,
              NA,
              NA,
              "Further education and skills geography - detailed summary",
              NA,
              "Further education and skills subject - free courses for jobs detailed")

for (i in seq_along(fe)) {
  if (is.data.frame(fe[[i]])) {
    # TODO not currently running rename_variables as there are duplicate issues in the lookup table
    readr::write_csv(fe[[i]], paste0("data/csv/fe/", fe_names[i], ".csv"))
  }
}

fe |>
  lapply(function(df) {
    if (is.data.frame(df)) {
      df |>
        tidyr::pivot_longer(cols = -(dplyr::any_of(dimensions)),
                            names_to = "variable_code") |>
        dplyr::left_join(fe_lookup,
                         by = c("variable_code" = "Variable name")) |>
        dplyr::rename(variable_name = `Variable description`)
    }
  }) |>
  saveRDS("data/app/fe.rds")

# FE destination ----------------------------------------------------------

fe_dest_lookup <- readr::read_delim("data/FE_destination/data-guidance/data-guidance.txt",
                                    delim = "|", trim_ws = TRUE,
                                    skip = 52) |>
  dplyr::filter(!is.na(`Variable description`), !grepl("---", `Variable description`), `Variable description` != "Variable description") |>
  dplyr::distinct()

fe_dest <- lapply(list.files("data/FE_destination/data", full.names = TRUE),
                  function(file) {
                    readr::read_csv(file, na = c("c", "x", "z", "low")) |>
                      dplyr::select(-dplyr::any_of(dims_to_remove)) |>
                      dplyr::select(-c(lad_code, lad_name)) |>
                      dplyr::rename(date = time_period,
                                    geography_code = new_la_code,
                                    geography_name = la_name) |>
                      dplyr::mutate(date = academic_year(date)) |>
                      dplyr::filter(geography_code %in% c(geog_codes$wy,
                                                          geog_codes$ny))
                  }) |>
  setNames(basename(list.files("data/FE_destination/data")))

fe_dest_names <- c("16-18 local authority level destinations")

for (i in seq_along(fe_dest)) {
  if (is.data.frame(fe_dest[[i]])) {
    rename_variables(fe_dest[[i]], fe_dest_lookup) |>
    readr::write_csv(paste0("data/csv/fe_dest/", fe_dest_names[i], ".csv"))
  }
}

fe_dest |>
  lapply(function(df) {
    if (is.data.frame(df)) {
      df |>
        tidyr::pivot_longer(cols = -(dplyr::any_of(dimensions)),
                            names_to = "variable_code") |>
        dplyr::left_join(fe_dest_lookup,
                         by = c("variable_code" = "Variable name")) |>
        dplyr::rename(variable_name = `Variable description`)
    }
  }) |>
  saveRDS("data/app/fe_dest.rds")



# Apprenticeships ---------------------------------------------------------

apprenticeships <- lapply(list.files("data/apprenticeships/data",
                                     full.names = TRUE),
                          function(file) {
                            readr::read_csv(file)
                          }) |>
  setNames(basename(list.files("data/apprenticeships/data")))

# data is so granular, everything is suppressed!
apprenticeships$`app-geography-detailed-202223-q1.csv` |>
  dplyr::group_by(achievements_with_suppressed_values = ifelse(achievements == "low", TRUE, FALSE)) |>
  dplyr::summarise(n = dplyr::n())

# bespoke data, generated to total sex and ethnicity BUT 22/23 so far only
apprenticeships <- readr::read_csv("data/apprenticeships/data-apprenticeships-and-traineeships.csv") |>
  dplyr::filter(lad_code %in% c(geog_codes$wy, geog_codes$ny)) |>
  dplyr::mutate(date = academic_year(time_period)) |>
  dplyr::select(date,
                geography_code = lad_code,
                geography_name = lad_name,
                ssa_t1_desc,
                apprenticeship_level = apps_level,
                starts,
                achievements) |>
  readr::write_csv("data/csv/apprenticeships/apprenticeship_starts_achievements_2022_23.csv")


# HESA --------------------------------------------------------------------

# HE UKPRN geography lookup

ukprn_region_lookup <- data.frame(UKPRN = c("10007785",
                                            "10007148",
                                            "10021682",
                                            "10003854",
                                            "10003861",
                                            "10034449",
                                            "10007795",
                                            "10003863",
                                            "10004740",
                                            "10007713",
                                            "10007167")) |>
  dplyr::mutate(region = dplyr::case_when(UKPRN %in% c("10007785",
                                                       "10007148",
                                                       "10021682",
                                                       "10003854",
                                                       "10003861",
                                                       "10034449",
                                                       "10007795",
                                                       "10003863") ~ "WY",
                                          UKPRN %in% c("10004740",
                                                       "10007713",
                                                       "10007167") ~ "NY")
  )

readr::write_csv(ukprn_region_lookup, "data/csv/lookups/ukprn_region_lookup.csv")


# HESA 51 -----------------------------------------------------------------

#table51.url <- "https://www.hesa.ac.uk/data-and-analysis/students/table-51.csv"
#download.file(table51.url, "data-raw/HESA/table-51.zip", mode = "wb")
#unzip("data-raw/HESA/table-51.zip", exdir = "data/HESA/table-51")
table51.files <- list.files("data/HESA/table-51", full.names = TRUE)

table51 <- lapply(table51.files, function(file) {
  temp <- readr::read_csv(file, col_names = FALSE, n_max = 50)
  skip <- which(grepl("UKPRN", temp$X1)) - 1
  readr::read_csv(file, skip = skip)
}) |>
  dplyr::bind_rows()

# Generate list of UKPRNs in the areas we care about
ukprn_he_yorks <- table51 |> dplyr::select(UKPRN, `HE provider`, `Region of HE provider`) |>
  dplyr::filter(`Region of HE provider` == "Yorkshire and The Humber") |>
  dplyr::distinct() |>
  dplyr::mutate(LSIP = dplyr::case_when(UKPRN %in% c("10007785",
                                                     "10007148",
                                                     "10021682",
                                                     "10003854",
                                                     "10003861",
                                                     "10034449",
                                                     "10007795",
                                                     "10003863") ~ "WY",
                                        UKPRN %in% c("10004740",
                                                     "10007713",
                                                     "10007167") ~ "NY",
                                        TRUE ~ NA_character_)) |>
  dplyr::filter(!is.na(LSIP))

# Filter table 51

table51_filtered <- table51 |>
  dplyr::filter(UKPRN %in% ukprn_he_yorks$UKPRN)

readr::write_csv(table51_filtered, "data/csv/he/HE qualifiers by HE provider and subject of study 2019-20 to 2021-22.csv")
saveRDS(table51_filtered, "data/app/hesa51.rds")



table51_051.url <- "https://www.hesa.ac.uk/data-and-analysis/students/table-51-051.csv"
download.file(table51_051.url, "data-raw/HESA/table-51-051.zip", mode = "wb")
unzip("data-raw/HESA/table-51-051.zip", exdir = "data/HESA/table-51-051")
table51_051.files <- list.files("data/HESA/table-51-051", full.names = TRUE)
table51_051 <- lapply(table51_051.files, function(file) {
  temp <- readr::read_csv(file, col_names = FALSE, n_max = 50)
  skip <- which(grepl("UKPRN", temp$X1)) - 1
  readr::read_csv(file, skip = skip) |>
    dplyr::filter(UKPRN %in% ukprn_he_yorks$UKPRN)
}) |>
  dplyr::bind_rows()

readr::write_csv(table51_051, "data/csv/he/HE qualifiers by HE provider and subject of study 2019-20 to 2021-22 (051).csv")
saveRDS(table51_051, "data/app/hesa51-051.rds")


table19.url <- "https://www.hesa.ac.uk/data-and-analysis/students/table-19.csv"
download.file(table19.url, "data-raw/HESA/table-51-051.zip", mode = "wb")
unzip("data-raw/HESA/table-51-051.zip", exdir = "data/HESA/table-51-051")
table19.files <- list.files("data/HESA/table-51-051", full.names = TRUE)
table19 <- lapply(table19.files, function(file) {
  temp <- readr::read_csv(file, col_names = FALSE, n_max = 50)
  skip <- which(grepl("UKPRN", temp$X1)) - 1
  readr::read_csv(file, skip = skip) |>
    dplyr::filter(UKPRN %in% ukprn_he_yorks$UKPRN)
}) |>
  dplyr::bind_rows()

readr::write_csv(table19, "data/csv/he/HE qualifiers by HE provider and subject of study 2014-15 to 2018-19.csv")
saveRDS(table19, "data/app/hesa19.rds")




# Table 1
# table1.url <- "https://www.hesa.ac.uk/data-and-analysis/students/table-1.csv"
# download.file(table1.url, file.path("data-raw", "HESA", "table-1.zip"), mode = "wb")
# unzip("data-raw/HESA/table-1.zip", exdir = "data/HESA/table-1")

table1.files <- list.files("data/HESA/table-1", full.names = TRUE)

table1 <- lapply(table1.files, function(file) {
  temp <- readr::read_csv(file, col_names = FALSE, n_max = 50)
  skip <- which(grepl("UKPRN", temp$X1)) - 1
  readr::read_csv(file, skip = skip) |>
    dplyr::filter(UKPRN %in% ukprn_he_yorks$UKPRN)
}) |> dplyr::bind_rows()

readr::write_csv(table1, "data/csv/he/HE student enrolments by HE provider 2014-15 to 2021-22.csv")
saveRDS(table1, "data/app/hesa1.rds")

# Table 13 - HE student enrolments by HE provider and subject of study 2014/15 to 2018/19

# table13.url <- "https://www.hesa.ac.uk/data-and-analysis/students/table-13.csv"
#
# download.file(table13.url, "data-raw/HESA/table-13.zip", mode = "wb")
# unzip("data-raw/HESA/table-13.zip", exdir = "data/HESA/table-13")

table13.files <- list.files("data/HESA/table-13", full.names = TRUE)
table13 <- lapply(table13.files, function(file) {
  temp <- readr::read_csv(file, col_names = FALSE, n_max = 50)
  skip <- which(grepl("UKPRN", temp$X1)) - 1
  readr::read_csv(file, skip = skip) |>
    dplyr::filter(UKPRN %in% ukprn_he_yorks$UKPRN)
}) |>
  dplyr::bind_rows()

readr::write_csv(table13, "data/csv/he/HE student enrolments by HE provider and subject of study 2014-15 to 2018-19.csv")
saveRDS(table13, "data/app/hesa13.rds")


# Table 49 - HE student enrolments by HE provider and subject of study 2019/20 to 2020/21

# table49.url <- "https://www.hesa.ac.uk/data-and-analysis/students/table-49.csv"
#
# download.file(table49.url, "data-raw/HESA/table-49.zip", mode = "wb")
# unzip("data-raw/HESA/table-49.zip", exdir = "data/HESA/table-49")

table49.files <- list.files("data/HESA/table-49", full.names = TRUE)

table49 <- lapply(table49.files, function(file) {
  temp <- readr::read_csv(file, col_names = FALSE, n_max = 50)
  skip <- which(grepl("UKPRN", temp$X1)) - 1
  readr::read_csv(file, skip = skip) |>
    dplyr::filter(UKPRN %in% ukprn_he_yorks$UKPRN)
}) |>
  dplyr::bind_rows()

readr::write_csv(table49, "data/csv/he/HE student enrolments by HE provider and subject of study 2019-20 to 2020-21.csv")
saveRDS(table49, "data/app/hesa49.rds")


table49_051.url <- "https://www.hesa.ac.uk/data-and-analysis/students/table-49-051.csv"
download.file(table49_051.url, "data-raw/HESA/table-49-051.zip", mode = "wb")
unzip("data-raw/HESA/table-49-051.zip", exdir = "data/HESA/table-49-051")

table49_051.files <- list.files("data/HESA/table-49-051", full.names = TRUE)

table49_051 <- lapply(table49_051.files, function(file) {
  temp <- readr::read_csv(file, col_names = FALSE, n_max = 50)
  skip <- which(grepl("UKPRN", temp$X1)) - 1
  readr::read_csv(file, skip = skip) |>
    dplyr::filter(UKPRN %in% ukprn_he_yorks$UKPRN)
}) |>
  dplyr::bind_rows()

readr::write_csv(table49_051, "data/csv/he/HE student enrolments by HE provider and subject of study 2019-20 to 2020-21 (051).csv")
saveRDS(table49_051, "data/app/hesa49_051.rds")




# HESA Graduates ----------------------------------------------------------

grad.table1.url <- "https://www.hesa.ac.uk/data-and-analysis/graduates/table-1.csv"
download.file(grad.table1.url, "data-raw/HESA/grad-table-1.zip", mode = "wb")
unzip("data-raw/HESA/grad-table-1.zip", exdir = "data/HESA/grad-table-1")

grad.table1.files <- list.files("data/HESA/grad-table-1", full.names = TRUE)

grad.table1 <- lapply(grad.table1.files, function(file) {
  temp <- readr::read_csv(file, col_names = FALSE, n_max = 50)
  skip <- which(grepl("UKPRN", temp$X1)) - 1
  readr::read_csv(file, skip = skip) |>
    dplyr::filter(UKPRN %in% ukprn_he_yorks$UKPRN)
}) |>
  dplyr::bind_rows()

readr::write_csv(grad.table1, "data/csv/he/Graduate activities by provider and sex.csv")
saveRDS(grad.table1, "data/app/hesa-grad-table-1.rds")

#########

grad.table6.url <- "https://www.hesa.ac.uk/data-and-analysis/graduates/table-6.csv"
download.file(grad.table6.url, "data-raw/HESA/grad-table-6.zip", mode = "wb")
unzip("data-raw/HESA/grad-table-6.zip", exdir = "data/HESA/grad-table-6")

grad.table6.files <- list.files("data/HESA/grad-table-6", full.names = TRUE)

grad.table6 <- lapply(grad.table6.files, function(file) {
  temp <- readr::read_csv(file, col_names = FALSE, n_max = 50)
  skip <- which(grepl("UKPRN", temp$X1)) - 1
  readr::read_csv(file, skip = skip) |>
    dplyr::filter(UKPRN %in% ukprn_he_yorks$UKPRN)
}) |>
  dplyr::bind_rows()

readr::write_csv(grad.table6, "data/csv/he/Graduate activities by provider.csv")
saveRDS(grad.table6, "data/app/hesa-grad-table-6.rds")

####

####

grad.table28.url <- "https://www.hesa.ac.uk/data-and-analysis/graduates/table-28.csv"
download.file(grad.table28.url, "data-raw/HESA/grad-table-28.zip", mode = "wb")
unzip("data-raw/HESA/grad-table-28.zip", exdir = "data/HESA/grad-table-28")

grad.table28.files <- list.files("data/HESA/grad-table-28", full.names = TRUE)

grad.table28 <- lapply(grad.table28.files, function(file) {
  temp <- readr::read_csv(file, col_names = FALSE, n_max = 50)
  skip <- which(grepl("UKPRN", temp$X1)) - 1
  readr::read_csv(file, skip = skip) |>
    dplyr::filter(UKPRN %in% ukprn_he_yorks$UKPRN)
}) |>
  dplyr::bind_rows()

readr::write_csv(grad.table28, "data/csv/he/Graduate activities by provider and subject area of degree.csv")
saveRDS(grad.table28, "data/app/hesa-grad-table-28.rds")



bres <- readr::read_csv("data-raw/NOMIS/bres.csv") |>
  dplyr::select(DATE, GEOGRAPHY_CODE, GEOGRAPHY_NAME, INDUSTRY_CODE, INDUSTRY_NAME, OBS_VALUE) |>
  readr::write_csv("data/csv/nomis/bres.csv")

ukbc_lu_emp <- readr::read_csv("data-raw/NOMIS/ukbc-lu-emp.csv") |>
  dplyr::select(DATE, GEOGRAPHY_CODE, GEOGRAPHY_NAME, INDUSTRY_CODE, INDUSTRY_NAME, EMPLOYMENT_SIZEBAND_NAME, OBS_VALUE) |>
  readr::write_csv("data/csv/nomis/ukbc-lu-emp.csv")
