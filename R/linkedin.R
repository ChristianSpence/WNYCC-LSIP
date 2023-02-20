# LinkedIn

li_path <- "data-raw/LinkedIn/Copy of UK_DfE_GeosUpdated_05Dec22.xlsx"
li_sheets <- readxl::excel_sheets(li_path)
li_sheets <- li_sheets[grepl("RAW", li_sheets)]
li <- lapply(li_sheets, function(sht) {
  df <- readxl::read_excel(li_path, sheet = sht)

  if ("Local Area" %in% names(df)) {
    df <- df |>
      dplyr::filter(`Local Area` %in% c("West Yorkshire", "York And North Yorkshire"))
  }

  if ("Geography" %in% names(df)) {
    df <- df |>
      dplyr::filter(Geography %in% c("West Yorkshire", "York And North Yorkshire"))
  }

  return(df)
}) |>
  setNames(sub("RAW-[0-9]) ", "", li_sheets) |> trimws())

# save separate CSVs

for (i in seq_along(li)) {
  readr::write_csv(li[[i]], paste0("data/csv/linkedin/", names(li)[i], ".csv"))
}


