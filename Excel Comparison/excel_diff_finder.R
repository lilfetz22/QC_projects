# Load required libraries
library(readxl); library(dplyr)

# Set the file paths for the two Excel workbooks
# file_path1 <- paste0(planning_tool_proj_loc, "/Planning Tool March 11 2024 - new env 1 -v2.xlsm")
# file_path2 <- paste0(planning_tool_proj_loc, "/Planning Tool March 11 2024 - new env 1.xlsm"
file_path1 <- paste0(ops_plan_proj_loc, "/Reports.xlsm")
file_path2 <- paste0(ops_plan_proj_loc, "/report_check.xlsx")

# Get the sheet names from both workbooks
sheet_names1 <- excel_sheets(file_path1)
sheet_names2 <- excel_sheets(file_path2)

# Initialize variables to store differences
total_differences <- 0
differences_list <- list()

# Loop through each sheet and compare values
for (sheet_name in intersect(sheet_names1, sheet_names2)) {
  # Read data from both workbooks
  data1 <- read_excel(file_path1, sheet = sheet_name)
  data2 <- read_excel(file_path2, sheet = sheet_name)
  
  # Compare data
  differences <- data1 %>%
    mutate_all(as.character) %>%
    setdiff(data2 %>% mutate_all(as.character))
  
  num_differences <- nrow(differences)
  
  if (num_differences > 0) {
    total_differences <- total_differences + num_differences
    differences_list[[sheet_name]] <- differences
  }
}

# Print results
cat("Total differences found:", total_differences, "\n")

if (total_differences > 0) {
  cat("Differences found in the following sheets:\n")
  for (sheet_name in names(differences_list)) {
    cat("Sheet:", sheet_name, "\n")
    print(differences_list[[sheet_name]])
  }
}

