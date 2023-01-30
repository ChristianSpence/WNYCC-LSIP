# Defines all LAD codes for the projects
geog_codes <- list(wy = paste0("E080000", 32:36),
                   ny = c("E0600000014", # York
                          paste0("E070001", 63:69) # Craven:Selby
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
                                skip = 26, n_max = 19)
ks4_lookup <- ks4_lookup[-1, ]

ks4 <- readr::read_csv("data/KS4/data/2122_lad_pr_data.csv") |>
  dplyr::filter(lad_code %in% c(geog_codes$wy, geog_codes$ny)) |>
  dplyr::select(-dplyr::any_of(dims_to_remove)) |>
  dplyr::rename(date = time_period,
                geography_code = lad_code,
                geography_name = lad_name) |>
  dplyr::mutate(date = academic_year(date))

ks4 |>
  rename_variables(ks4_lookup) |>
  readr::write_csv("data/csv/ks4.csv")

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
  dplyr::filter(!is.na(`Variable description`), !grepl("---", `Variable description`), `Variable description` != "Variable description")


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

for (i in seq_along(a_level)) {
  readr::write_csv(a_level[[i]], paste0("data/csv/a-level/",names(a_level[i])))
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
  dplyr::filter(!is.na(`Variable description`), !grepl("---", `Variable description`), `Variable description` != "Variable description")

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

for (i in seq_along(fe)) {
  if (is.data.frame(fe[[i]])) {
    readr::write_csv(fe[[i]], paste0("data/csv/fe/",names(fe[i])))
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
  dplyr::filter(!is.na(`Variable description`), !grepl("---", `Variable description`), `Variable description` != "Variable description")

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
                                                          geog_codes$ny)) |>
                      tidyr::pivot_longer(cols = -(dplyr::any_of(dimensions)),
                                          names_to = "variable_code") |>
                      dplyr::left_join(fe_dest_lookup,
                                       by = c("variable_code" = "Variable name")) |>
                      dplyr::rename(variable_name = `Variable description`)
                  }) |>
  setNames(basename(list.files("data/FE_destination/data")))

saveRDS(fe_dest, "data/app/fe_dest.rds")

