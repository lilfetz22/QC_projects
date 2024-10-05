import pandas as pd
import datetime
import numpy as np

contacts = pd.read_excel(contacts_filepath, sheet_name='Sheet2')

username_password = pd.read_excel(usernames_filepath)

username_password.loc[:, 'DefID'] = username_password['Username'].str.split('_').str[0].astype(int)

contacts_grouped = contacts.groupby(['DefID', 'Facility'])['EMAILADDRESS'].apply(lambda x: '; '.join(x)).reset_index()

contacts_grouped.loc[:, 'len_email'] = contacts_grouped['EMAILADDRESS'].apply(len)

contacts_grouped = contacts_grouped.drop('len_email', axis=1)

contacts_w_sftp_info = contacts_grouped.merge(username_password, on='DefID', how='left')

contacts_w_sftp_info[contacts_w_sftp_info['Username'].isnull()]

contacts_w_sftp_info = contacts_w_sftp_info[~contacts_w_sftp_info['Username'].isnull()]

dummy_contact = pd.DataFrame({'DefID': [1, 2], 'Facility': ['Test Hospital', 'Test Hospital2'],
'EMAILADDRESS': ['jane.doe@example.com', 'john.smith@example.com'],
'Username': ['1_test', '2_test'], 'Password': ['password1', 'password2']})

contacts_w_sftp_info = pd.concat([dummy_contact, contacts_w_sftp_info], ignore_index=True)

contacts_w_sftp_info.isnull().sum()

contacts_w_sftp_info[contacts_w_sftp_info['Username'].isnull() | contacts_w_sftp_info['Password'].isnull()]

contacts_w_sftp_info[contacts_w_sftp_info['Facility'].str.contains('Example')]

def generate_email_bodies(row):
    username_email_body = f"""Good morning,

Please see below for the SFTP Username for {row['Facility']}. Your SFTP password will follow in a separate email.

User: {row['Username']}

Login URL: http://sftp.example.com/

Thank you!"""

    password_email_body = f"""Good morning,

Please see below for the SFTP Password for {row['Facility']}.

Password: {row['Password']}

Login URL: http://sftp.example.com/

Thank you!"""

    return pd.Series([username_email_body, password_email_body], index=['Username Email Body', 'Password Email Body'])

email_bodies = contacts_w_sftp_info.apply(generate_email_bodies, axis=1)

contacts_w_sftp_info = pd.concat([contacts_w_sftp_info, email_bodies], axis=1)

contacts_w_sftp_info.loc[:, 'Username Email Subject'] = 'Example Company SFTP Username'
contacts_w_sftp_info.loc[:, 'Password Email Subject'] = 'Example Company SFTP Password'

selected_sites_cwsftp = contacts_w_sftp_info_no_macro.merge(select_sites, on='Facility', how='inner')

selected_sites_cwsftp.loc[:, 'EMAILADDRESS'] = 'jane.doe@example.com'

selected_sites_cwsftp.loc[:, 'sent'] = np.nan

selected_sites_cwsftp