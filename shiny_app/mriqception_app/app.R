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
library(jsonlite)

source("~/Documents/Code/mriqception/shiny_app/mriqception_app/utils.R")

# Define UI for application that draws a histogram
ui <- fluidPage(
    
    # Application title
    titlePanel("MRIQCeption"),
    
    sidebarLayout(
        sidebarPanel(
            fileInput("local_file", h5("Please upload a tsv from MRIQC of your local data"), multiple = FALSE, accept = ".tsv"),
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
                                 "1.5T"= "1.5",
                                 "3T"="3",
                                 "7T" = "7"
                             ))
            ),
            
            
            
            actionButton("get_data", "Generate API data")
        ),
        
        mainPanel(
            textOutput("waiting_message"),
            textOutput("color_descriptions"),
            uiOutput("select_IQM_render"),
            conditionalPanel(
                condition = "input.get_data",
                plotlyOutput("plot")
            ),
            conditionalPanel(condition = "plotted == TRUE",
                             textOutput("IQM_description"))
            
        )
    )
)

server <- function(input, output) {
    values <- reactiveValues(plotted=FALSE)
    
    do_plot <- function(df){ 
        plotted=TRUE
        df %>% 
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
                color = I(get_color()),
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
                x = ~variable[df$group=="all_data"],
                y = ~value[df$group=="all_data"],
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
    
    get_color <- reactive(
        color <- IQM_descriptions$color[which(IQM_descriptions$iqm_name == input$select_IQM)]
    )
    
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
                    choices=unique(values$df$variable)
        )
    })
    
    get_API_data <- eventReactive(input$get_data,{
        # load in API data
        req(input$local_file)
        output$waiting_message <- renderText({"Please be patient, loading lots of data"})
        
        API_data <- read.table(paste('../../test_data/group_',input$modality,'.tsv', sep=""),header=TRUE)
        API_data <- melt(API_data)
        API_data$group <- "all_data"
        API_data$variable <- as.character(API_data$variable)
        # ext <- tools::file_ext(input$local_file$name)
        # switch(ext,
        #        tsv = vroom::vroom(input$file$datapath, delim = "\t"),
        #        validate("Invalid file; Please upload a .tsv file")
        # )
        inFile <- input$local_file
        local_data <- read.table(inFile$datapath, header=TRUE)
        local_data <- melt(local_data)
        local_data$group <- "local_set"
        full_data <- rbind(local_data,API_data)
        full_data$value <- as.numeric(full_data$value)
        output$waiting_message <- renderText({""})
        return(full_data)
        
        
        # in here, can do filtering  -- have access to input$filters
    })
    
    remove_outliers_reactive <- reactive({
        if (input$remove_outliers){
            values$plot_data <- remove_outliers_fxn(values$filtered_data)
        }else{
            values$plot_data <- values$filtered_data
        }
    })
    
    output$plot <-renderPlotly({
        values$df <- get_API_data()
        #browser()
        if (input$select_IQM == ""){ 
            values$filtered_data <- values$df
        }else{
            values$filtered_data <- values$df %>% filter(variable == input$select_IQM)
        }
        #browser()
        remove_outliers_reactive()
        do_plot(values$plot_data)
        #values$plotted=TRUE
        
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
