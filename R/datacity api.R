# single call

datacity <- httr::POST(
  url = "https://serverdec22.thedatacity.com/api/getfilteredcompanies?insights=true",
  body = '{
            "OnlyCompaniesWithRegisteredAddressWithinFilterLocation": true,
            "CalculateInsightsBasedOnlyOnRegisteredAddresses": true,
            "SelectedLANames": [
              "Bradford",
              "Calderdale",
              "Craven",
              "Hambleton",
              "Harrogate",
              "Kirklees",
              "Leeds",
              "Richmondshire",
              "Ryedale",
              "Scarborough",
              "Selby",
              "Wakefield",
              "York"
            ],
            "ReturnCount": 0
           }',
  encode = "raw")

content <- rawToChar(datacity$content)

content_list <- jsonlite::fromJSON(content) |> as.list()

content_dfs <- lapply(content_list$insights, function(x) {
    if (is.data.frame(x)) {
      return(x)
    }
})



isdf <- sapply(content_dfs, \(x) is.data.frame(x))

dfs <- content_dfs[isdf]

for (i in seq_along(dfs)) {
  readr::write_csv(dfs[[i]], paste0("data/csv/datacity/", names(dfs)[i], ".csv"))
}


# multiple calls, one per LA

LAs <- c("Bradford",
         "Calderdale",
         "Craven",
         "Hambleton",
         "Harrogate",
         "Kirklees",
         "Leeds",
         "Richmondshire",
         "Ryedale",
         "Scarborough",
         "Selby",
         "Wakefield",
         "York")

datacity_las <- lapply(LAs, function(LA) {
  httr::POST(
    url = "https://serverdec22.thedatacity.com/api/getfilteredcompanies?insights=true",
    body = paste0(
            '{
              "OnlyCompaniesWithRegisteredAddressWithinFilterLocation": true,
              "CalculateInsightsBasedOnlyOnRegisteredAddresses": true,
              "SelectedLANames": ["',
            LA,
            '"],
            "ReturnCount": 0
           }'),
    encode = "raw")
}) |> setNames(LAs)

datacity_la_processed <- lapply(datacity_las, function(LA) {
  content <- rawToChar(LA$content)
  content_list <- jsonlite::fromJSON(content) |> as.list()
  content_dfs <- lapply(content_list$insights, function(x) {
    if (is.data.frame(x)) {
      return(x)
    }
  })
  isdf <- sapply(content_dfs, \(x) is.data.frame(x))
  dfs <- content_dfs[isdf]
  return(dfs)
})

# temporary serial dump of the above object to come back to
saveRDS(datacity_la_processed, "data/datacity/datacity_la_processed.rds")













