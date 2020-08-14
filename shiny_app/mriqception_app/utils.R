IQM_descriptions <- read.csv("~/Documents/Code/mriqception/shiny_app/mriqception_app/iqm_descriptions_shiny.csv")
#IQM_descriptions <- read.csv("iqm_descriptions_shiny.csv")

bold_choices <- list(
  # "SNR" = "snr", 
  # "TSNR" = "tsnr", 
  # "DVAR" = 'dvars_nstd', 
  # "FD" = 'fd_mean',
  # "FWHM"='fwhm_avg',
  # "gsr_x" = 'gsr_x',
  # "gsr_y" = 'gsr_y',
  "TE" = 'bids_meta.EchoTime',
  "TR" = 'bids_meta.RepetitionTime',
  "Tesla"='bids_meta.MagneticFieldStrength')

T1w_choices <- list(
  # "SNR_TOTAL" = "snr_total", 
  #                   "SNR_GM" = "snr_gm", 
  #                   "SNR_WM" = "snr_wm", 
  #                   "SNR_CSF" = "snr_csf",
  #                   "CNR" = "cnr", 
  #                   "EFC" = "efc", 
  #                   "FWHM" = "fwhm_avg", 
  "TE" = "bids_meta.EchoTime", 
  "TR" = "bids_meta.RepetitionTime", 
  "Tesla" = "bids_meta.MagneticFieldStrength")

T2w_choices = list(
  # "SNR_TOTAL" = "snr_total", 
  # "SNR_GM" = "snr_gm", 
  # "SNR_WM" = "snr_wm", 
  # "SNR_CSF" = "snr_csf",
  # "CNR" = "cnr", 
  # "EFC" = "efc", 
  "TE" = "bids_meta.EchoTime", 
  "TR" = "bids_meta.RepetitionTime", 
  "Tesla" = "bids_meta.MagneticFieldStrength")

measure_slider_inputs <- list(
  # snr = list(
  #   min = 3, 
  #   max = 6
  # ),
  # tsnr = list(
  #   min = 0, 
  #   max = 100
  # ),
  # dvar = list(
  #   min = 10, 
  #   max = 80
  # ),
  # fd = list(
  #   min = -2, 
  #   max = 2
  # ),
  # fwhm = list(
  #   min = 2, 
  #   max = 3.5
  # ),
  # gsr_x = list(
  #   min = -0.03, 
  #   max = 0.015
  # ),
  # gsr_y = list(
  #   min = -0.02, 
  #   max = 0.08
  # ),
  TR= list(
    min = 0, 
    max = 5
  ),
  TE = list(
    min = 0, 
    max = 0.05
  )
  # snr_total = list(
  #   min = 8, 
  #   max = 18
  # ),
  # snr_gm = list(
  #   min = 7, 
  #   max = 16
  # ),
  # snr_wm= list(
  #   min = 10, 
  #   max = 35
  # ),
  # snr_csf = list(
  #   min = 10, 
  #   max = 40
  # ),
  # cnr = list(
  #   min = 1, 
  #   max = 4.5
  # ),
  # efc = list(
  #   min = 0, 
  #   max = 1
  # )
)


for (idx in seq.int(1,length(measure_slider_inputs))){
  measure_slider_inputs[[idx]]$value <- c(measure_slider_inputs[[idx]]$min, measure_slider_inputs[[idx]]$max)
  
}

slider_input_fxn <- function(id){
  label_text <- paste0("Please select a range for ",toupper(id),":", sep = "")
  sliderInput(id, label = h5(label_text), min = measure_slider_inputs[[id]][["min"]], 
              max = measure_slider_inputs[[id]][["max"]], 
              value =measure_slider_inputs[[id]][["value"]])
}

remove_outliers_fxn <- function(data){
  filtered <- data %>% filter(group == "all_data")
  qnt <- quantile(filtered$value, probs=c(.25, .75), na.rm=TRUE)
  H <- 1.5 * IQR(filtered$value,na.rm=TRUE)
  data$value[(data$value < (qnt[1] - H)) & (data$group == "all_data")] <- NA
  data$value[(data$value > (qnt[2] + H)) & (data$group == "all_data")] <- NA
  return(data)
}

reorganize_bids_data <- function(temp){
  
  #' A function to take MRIQC data from the API and transform it to a useable format
  #' @param temp: the "_items" field from the list from the API 
  #' @return data.frame of readable data 
  #' 
  #' Written by C.Walsh on 8/13/2020
  
  fields <- c()
  expand_list <- c("bids_meta","provenance", "settings" )
  
  for (val in seq.int(1,length(temp[[1]])-1)){
    if (names(temp[[1]])[val] %in% expand_list){
      for (inner_val in seq.int(1,length(temp[[1]][[val]]))){
        if (names(temp[[1]][[val]])[inner_val] %in% expand_list){ 
          for (double_inner in seq.int(1,length(temp[[1]][[val]][[inner_val]]))){
            fields <- c(fields, 
                        paste0(names(temp[[1]])[val],".",names(temp[[1]][[val]])[inner_val],".",names(temp[[1]][[val]][[inner_val]])[double_inner]))
          }
        }else{
          fields <- c(fields, paste0(names(temp[[1]])[val],".",names(temp[[1]][[val]])[inner_val]))
        }
      }
    }  else{
      fields<- c(fields, names(temp[[1]])[val])
    }
  }
  
  expanded_data <- data.frame(matrix(nrow=length(temp),ncol=length(fields)))
  colnames(expanded_data) <- fields
  
  for (sub in seq.int(length(temp))){
    for (field in seq.int(1,length(fields))){
      split_name <- unlist(strsplit(fields[field], split = "[.]"))
      #print(split_name)
      if (length(split_name)==1){
        if (fields[field] %in% names(temp[[sub]])){
          expanded_data[sub,field] <- temp[[sub]][[split_name[1]]]
        }
      }else if(length(split_name)==2){
        if (split_name[2] %in% names(temp[[sub]][[split_name[1]]])){
          expanded_data[sub,field] <- temp[[sub]][[split_name[1]]][[split_name[2]]]
        }
      }else if(length(split_name)==3){
        if (split_name[3] %in% names(temp[[sub]][[split_name[1]]][[split_name[2]]])){
          expanded_data[sub,field] <- temp[[sub]][[split_name[1]]][[split_name[2]]][[split_name[3]]]
        }
      }
      
    }
    
  }
  colnames(expanded_data)[1] <- "subject_id"
  return(expanded_data)
}

create_filter_text <- function(input){
  #' A function to take reactive inputs from Shiny app and transform them into a string to be used for pulling data from the API 
  #' @param input: isolated reactive shiny input 
  #' @return string containing filter string for querying API 
  #' 
  #' Written by C.Walsh on 8/13/2020
  
  
  filter_map <- list(
    "bids_meta.EchoTime" = "TE", 
    "bids_meta.RepetitionTime" = "TR",
    "bids_meta.MagneticFieldStrength"= "mag_strength"
  )
  
  if (is.null(input$filters)){
    filters <- ""
  }else{
    filters <- "&where="
    
    for (filter in seq.int(1, length(input$filters))){
      if (input$filters[filter] != "bids_meta.MagneticFieldStrength"){
        filters <- paste0(filters,input$filters[filter],">=",input[[filter_map[[input$filters[filter]]]]][1],"&",
                          input$filters[filter],"<=",input[[filter_map[[input$filters[filter]]]]][2], sep="")
      }
      if (filter < length(input$filters)){
        filters <- paste0(filters,"&", sep="")
      }
    }
    
    if ("bids_meta.MagneticFieldStrength" %in% input$filters){
      filters <- paste0(filters,"&bids_meta.MagneticFieldStrength==",input$mag_strength)
    }
  }
  return(filters)
}