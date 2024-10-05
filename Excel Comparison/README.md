# Excel Comparison

## Overview

This folder contains tools and scripts used to validate data consistency after a Salesforce environment migration. The migration resulted in changes to several fields used for generating daily reports. These tools were crucial in ensuring data integrity and correct field mapping post-migration.

## Contents

1. **excel comparison - ops.ipynb**
2. **excel comparison - planning.ipynb**
3. **excel_diff_finder.R**

## Purpose

The primary purpose of these tools is to:

1. Compare data between the old and new Salesforce environments
2. Validate correct field mapping
3. Ensure data consistency in daily reports

## Jupyter Notebooks

### excel comparison - ops.ipynb

This notebook focuses on comparing operational data between the old and new Salesforce environments. It helps identify any discrepancies in field mappings or data values related to operational processes.

### excel comparison - planning.ipynb

This notebook is dedicated to comparing planning-related data. It assists in validating the consistency of planning information across the old and new Salesforce environments.

## R Script

### excel_diff_finder.R

This is a utility R script designed for quick comparisons between multiple Excel files. It was frequently used throughout the migration process to verify file consistency across various stages of the project.

Key features:
- Simple and efficient file comparison
- Easily adaptable for different Excel file structures
- Useful for repeated validation tasks

## Note

These tools were instrumental in maintaining data integrity during our Salesforce environment migration. They helped ensure that our daily reports remained accurate and consistent despite changes in field structures and data sources.
