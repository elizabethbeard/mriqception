modality <- "bold"
url_root <- 'https://mriqc.nimh.nih.gov/api/v1/'
filters <- '&where=bids_meta.RepetitionTime<2.5'
url <- paste0(url_root,modality,"?max_results=50&page=1",filters,sep="")
tmpFile <- tempfile()
download.file(url, destfile = tmpFile, method = "curl")
temp <- jsonlite::read_json(tmpFile)

last_page_href <- temp[["_links"]][["last"]][["href"]]
last_page_id <- strsplit(strsplit(last_page_href,split="page=")[[1]][2],split="&")[[1]][1]

expanded_data <- reorganize_bids_data(temp[["_items"]])

for (page in seq.int(2,5)){
  #for (page in seq.int(2,as.numeric(last_page_id))){
  url <- paste0(url_root,modality,"/?max_results=50&page=",as.character(page),filters,sep="")
  tmpFile <- tempfile()
  download.file(url, destfile = tmpFile, method = "curl")
  temp <- jsonlite::read_json(tmpFile)
  temp_expanded <- reorganize_bids_data(temp[["_items"]])
  expanded_data <- merge(expanded_data, temp_expanded, all=TRUE)
}


filepath <- "~/Documents/Code/mriqception/test_data/task-arrows_bold.json"
json_file <- read_json(filepath, simplifyVector = TRUE)

if ("EchoTime" %in% names(json_file)){ 
  measure_slider_inputs[["TE"]][["value"]] <- c(json_file[["EchoTime"]], json_file[["EchoTime"]])
}
if ("RepetitionTime" %in% names(json_file)){ 
  measure_slider_inputs[["TR"]][["value"]] <- c(json_file[["RepetitionTime"]], json_file[["RepetitionTime"]])
}
if ("MagneticFieldStrength" %in% names(json_file)){
  measure_slider_inputs[["mag_strength"]] <- json_file[["MagneticFieldStrength"]]
}
