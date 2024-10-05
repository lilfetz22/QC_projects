## SFTP Email Automation

This folder contains scripts and resources for automating the process of sending SFTP credentials to multiple partners via encrypted emails. The project was developed to streamline the distribution of usernames and passwords to over 100+ partners within a tight two-day deadline.

### Contents

- `sftp.py`: Python script for generating formatted email bodies with SFTP credentials
- `send_emails_macro.vb`: Excel macro for creating Outlook emails
- `autohotkey_script.ahk`: AutoHotkey script for automating email sending process

### Project Overview

The automation process consists of three main components:

1. **Python Script (`sftp.py`)**: 
   - Reads partner information from Excel files
   - Generates formatted email bodies for SFTP usernames and passwords
   - Outputs a consolidated Excel file with email content

2. **Excel Macro (`send_emails_macro.vb`)**:
   - Creates Outlook email drafts using the data from the Python script output

3. **AutoHotkey Script (`AutoHotkey.ahk`)**:
   - Automates the process of selecting the correct sending email address
   - Ensures proper encryption of each email
   - Triggers the sending of emails

### Why This Approach?

This solution was developed to address specific constraints:

- Requirement to send emails from a particular email address
- Need for email encryption
- Tight deadline (2 days) for implementation
- In-house solution preferred over third-party email services

While direct Python-to-Outlook integration would have been ideal, connectivity issues with the required email address necessitated this multi-step approach. The combination of Python, Excel macros, and AutoHotkey allowed for a rapid, effective solution that significantly reduced the time and effort compared to manual email sending.

### Usage

1. Run `sftp.py` to generate the email content Excel file
2. Open the Excel file with the macro and execute it to create email drafts
3. Run the AutoHotkey.ahk script to automate the final email sending process

### Notes

- Ensure all necessary dependencies are installed for the Python script
- The AutoHotkey script may need adjustments based on screen resolution and Outlook interface
- excel_execution.ahk, mouse_location.ahk, and name_pos_control.ahk are AutoHotkey scripts that were used during the testing and development process. They are not required for the final version of the project.

This solution demonstrates the power of combining different tools and scripting languages to overcome specific challenges in business process automation.
