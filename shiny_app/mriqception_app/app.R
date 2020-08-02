#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(reshape2)
library(plotly)

IQM_descriptions <- read.csv("../../tools/iqm_descriptions_shiny.csv")

bold_choices <- list("SNR" = "snr", 
                     "TSNR" = "tsnr", 
                     "DVAR" = 'dvars_nstd', 
                     "FD" = 'fd_mean',
                     "FWHM"='fwhm_avg',
                     "Tesla"='bids_meta_MagneticFieldStrength',
                     "gsr_x" = 'gsr_x',
                     "gsr_y" = 'gsr_y',
                     "TE" = 'bids_meta_EchoTime',
                     "TR" = 'bids_meta_RepetitionTime')

T1w_choices <- list("SNR_TOTAL" = "snr_total", 
                    "SNR_GM" = "snr_gm", 
                    "SNR_WM" = "snr_wm", 
                    "SNR_CSF" = "snr_csf",
                    "CNR" = "cnr", 
                    "EFC" = "efc", 
                    "FWHM" = "fwhm_avg", 
                    "TE" = "bids_meta_EchoTime", 
                    "TR" = "bids_meta_RepetitionTime", 
                    "Tesla" = "bids_meta_MagneticFieldStrength")

T2w_choices = list("SNR_TOTAL" = "snr_total", 
                   "SNR_GM" = "snr_gm", 
                   "SNR_WM" = "snr_wm", 
                   "SNR_CSF" = "snr_csf",
                   "CNR" = "cnr", 
                   "EFC" = "efc")

measure_slider_inputs <- list(
    snr = list(
        min = 3, 
        max = 6
    ),
    tsnr = list(
        min = 0, 
        max = 100
    ),
    dvar = list(
        min = 10, 
        max = 80
    ),
    fd = list(
        min = -2, 
        max = 2
    ),
    fwhm = list(
        min = 2, 
        max = 3.5
    ),
    gsr_x = list(
        min = -0.03, 
        max = 0.015
    ),
    gsr_y = list(
        min = -0.02, 
        max = 0.08
    ),
    TR= list(
        min = 0, 
        max = 5
    ),
    TE = list(
        min = 0, 
        max = 0.05
    ),
    snr_total = list(
        min = 8, 
        max = 18
    ),
    snr_gm = list(
        min = 7, 
        max = 16
    ),
    snr_wm= list(
        min = 10, 
        max = 35
    ),
    snr_csf = list(
        min = 10, 
        max = 40
    ),
    cnr = list(
        min = 1, 
        max = 4.5
    ),
    efc = list(
        min = 0, 
        max = 1
    )
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

# Define UI for application that draws a histogram
ui <- fluidPage(
    
    # Application title
    titlePanel("MRIQCeption"),
    
    sidebarLayout(
        sidebarPanel(
            fileInput("local_file", h5("Please upload a tsv of your local data"), multiple = FALSE, accept = ".tsv"),
            fileInput("json_info", h5("Optionally, upload a .json file of BIDS info for your study to automatically set filter parameters close to those in your own study"), multiple = FALSE, accept = ".json"),
            
            
            radioButtons("modality", 
                         h5("Please choose the modality you are interested in"),
                         choices = list("BOLD"='bold',
                                        "Structural (T1W)" = 'T1w', 
                                        "T2w" = "T2w")),
            checkboxInput("remove_outliers", "Remove outliers from API", value=FALSE),
            uiOutput("choose_filters"),
            # just BOLD filters
            conditionalPanel(
                condition = "input.filters.includes('snr')",
                slider_input_fxn("snr")
            ),
            conditionalPanel(
                condition = "input.filters.includes('tsnr')",
                slider_input_fxn("tsnr")
            ),
            conditionalPanel(
                condition = "input.filters.includes('dvars_nstd')",
                slider_input_fxn("dvar")
            ),
            conditionalPanel(
                condition = "input.filters.includes('fd_mean')",
                slider_input_fxn("fd")
            ),
            # just T1w filters 
            conditionalPanel(
                condition = "input.filters.includes('snr_total')",
                slider_input_fxn("snr_total")
            ),
            conditionalPanel(
                condition = "input.filters.includes('snr_gm')",
                slider_input_fxn("snr_gm")
            ),
            conditionalPanel(
                condition = "input.filters.includes('snr_wm')",
                slider_input_fxn("snr_wm")
            ),
            conditionalPanel(
                condition = "input.filters.includes('snr_csf')",
                slider_input_fxn("snr_csf")
            ),
            conditionalPanel(
                condition = "input.filters.includes('cnr')",
                slider_input_fxn("cnr")
            ),
            conditionalPanel(
                condition = "input.filters.includes('efc')",
                slider_input_fxn("efc")
            ),
            # all 
            conditionalPanel(
                condition = "input.filters.includes('fwhm_avg')",
                slider_input_fxn("fwhm")
            ),
            conditionalPanel(
                condition = "input.filters.includes('gsr_x')",
                slider_input_fxn("gsr_x")
            ),
            conditionalPanel(
                condition = "input.filters.includes('gsr_y')",
                slider_input_fxn("gsr_y")
            ),
            conditionalPanel(
                condition = "input.filters.includes('bids_meta_EchoTime')",
                slider_input_fxn("TE")
            ),
            conditionalPanel(
                condition = "input.filters.includes('bids_meta_RepetitionTime')",
                slider_input_fxn("TR")
            ),
            conditionalPanel(
                condition = "input.filters.includes('bids_meta_MagneticFieldStrength')",
                radioButtons("mag_strength", 
                             h5("Please choose a magnet strength"),
                             choices = list(
                                 "1.5T"= "1.5T",
                                 "3T"="3T",
                                 "7T" = "7T"
                             ))
            ),
            
            
            
            actionButton("get_data", "Generate API data")
        ),
        
        mainPanel(
            textOutput("waiting_message"),
            textOutput("color_descriptions"),
            conditionalPanel(
                condition = "input.get_data",
                uiOutput("select_IQM_render")
            ),
            conditionalPanel(
                condition = "input.get_data",
                plotlyOutput("plot")
            ),
            conditionalPanel(condition = "values.plotted == TRUE",
                             textOutput("IQM_description"))
            
        )
    )
)

server <- function(input, output) {
    values <- reactiveValues(full_data = data.frame(name=NULL, variable=NULL,value=NULL,group=NULL), 
                             plotted = FALSE, 
                             plot_data = NULL)
    
    output$choose_filters <- renderUI({
        if (input$modality == "bold"){
            choices_list <- bold_choices
        }else if (input$modality == "T1w"){
            choices_list <- T1w_choices
        }else if (input$modality == "T2w"){
            choices_list <- T2w_choices
        }
        checkboxGroupInput("filters", 
                           h5("Please choose the filters you want to use for the API data:"), 
                           choices = choices_list
        )
    })
    
    output$select_IQM_render <- renderUI({
        if (input$modality == "bold"){
            choices_list <- bold_choices
        }else if (input$modality == "T1w"){
            choices_list <- T1w_choices
        }else if (input$modality == "T2w"){
            choices_list <- T2w_choices
        }
        selectInput("select_IQM", h6("Please select IQM"), 
                    choices = unique(values$full_data$variable)
        )
    })
    
    get_API_data <- observeEvent(input$get_data,{
        # load in API data
        req(input$local_file)
        output$waiting_message <- renderText({"Please be patient, loading lots of data"})
        
        API_data <- read.table(paste('../../test_data/group_',input$modality,'.tsv', sep=""),header=TRUE)
        API_data <- melt(API_data)
        API_data$group <- "API"
        API_data$variable <- as.character(API_data$variable)
        
        ext <- tools::file_ext(input$local_file$name)
        switch(ext,
               tsv = vroom::vroom(input$file$datapath, delim = "\t"),
               validate("Invalid file; Please upload a .tsv file")
        )
        inFile <- input$local_file
        local_data <- read.table(inFile$datapath, header=TRUE)
        local_data <- melt(local_data)
        local_data$group <- "local_set"
        full_data <- rbind(local_data,API_data)
        full_data$group <- as.factor(full_data$group)
        values$full_data <- full_data
        values$API_data <- API_data
        values$plotted <- TRUE
        output$waiting_message <- renderText({""})
        
        # in here, can do filtering  -- have access to input$filters
    })
    
    get_color <- reactive(
        color <- IQM_descriptions$color[which(IQM_descriptions$iqm_name == input$select_IQM)]
    )
    
    do_plot <- function(data, IQM){ 
        data %>% 
            filter(variable == IQM) %>%
            plot_ly(type = 'violin') %>%
            add_trace(
                x = ~variable[df$group=="local_set"],
                y = ~value[df$group=="local_set"],
                legendgroup = 'Local',
                scalegroup = 'Local',
                name = 'Local',
                side = 'negative',
                box = list(
                    visible = T
                ),
                meanline = list(
                    visible = T
                ),
                line = list(
                    color = get_color()
                ),
                color = get_color(),
                points = 'all',
                pointpos = -0.5,
                jitter = 0.1,
                scalemode = 'count',
                meanline = list(
                    visible = T
                ),
                line = list(
                    color = get_color()
                ),
                marker = list(
                    line = list(
                        width = 2,
                        color = get_color()
                    ),
                    symbol = 'line-ns'
                )
            ) %>%
            add_trace(
                x = ~variable[df$group=="API"],
                y = ~value[df$group=="API"],
                legendgroup = 'API',
                scalegroup = 'API',
                name = 'API',
                side = 'positive',
                box = list(
                    visible = T
                ),
                meanline = list(
                    visible = T
                ),
                line = list(
                    color = 'rgb(58,54,54)'
                ), 
                color = I('dark gray')
            ) %>% 
            layout(
                xaxis = list(
                    title = ""  
                ),
                yaxis = list(
                    title = "",
                    zeroline = F
                )
            )
        
    }
    
    create_plot <- reactive(
        do_plot(values$plot_data, input$select_IQM)
    )
    
    remove_outliers_fxn <- function(data, filter_var){
        filtered <- data %>% filter(variable == filter_var & group == "API")
        qnt <- quantile(filtered$value, probs=c(.25, .75), na.rm=TRUE)
        H <- 1.5 * IQR(filtered$value,na.rm=TRUE)
        data$value[data$value < (qnt[1] - H)] <- NA
        data$value[data$value > (qnt[2] + H)] <- NA
        return(data)
    }
    
    remove_outliers_reactive <- reactive(
        if (input$remove_outliers){
            values$plot_data <- remove_outliers_fxn(values$full_data, input$select_IQM)
        }else{
            values$plot_data <- values$full_data
        }
    )
    
    output$plot <-renderPlotly({
        remove_outliers_reactive()
        create_plot()
        
    })
    
    output$IQM_description <- renderText(       
        paste(IQM_descriptions$iqm_definition[which(IQM_descriptions$iqm_name == input$select_IQM)])
    )
    
    output$color_descriptions <- renderText("Colors reflect class of IQM. In each plot, the API data is shown in dark grey. 
        Spatial IQMs are plotted in gold, temporal IQMs in orange, noise IQMs in red, motion IQMs in green, artifact IQMs in 
        light blue, descriptive IQMs in dark blue, and other IQMs in purple.")
    
}

# Run the application 
shinyApp(ui = ui, server = server)
