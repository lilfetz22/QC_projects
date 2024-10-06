import pandas as pd
import helper_fx
import create_capbase
from datetime import timedelta, datetime
try:
    today = datetime.today().strftime('%B %d %Y').replace(" 0", " ")
    todays_needs = pd.read_excel(f"Daily Tools/Assignment_Planning_{today}.xlsx", sheet_name='Summary')
except:
    today = (datetime.today()-timedelta(days=1)).strftime('%B %d %Y').replace(" 0", " ")
    todays_needs = pd.read_excel(f"Daily Tools/Assignment_Planning_{today}.xlsx", sheet_name='Summary')


todays_needs_fil = todays_needs[todays_needs['Suggested Resource'].isnull()].copy()
talent_needs = todays_needs_fil[(~todays_needs_fil['Request Name'].isin(requests_to_exclude))].groupby('Project Category')[['Requested Hours']].sum()
talent_needs.loc[:, 'FTE'] = talent_needs['Requested Hours'] / 40
# apply the custom_round function to the 'FTE' column
talent_needs['FTE_rounded'] = talent_needs['FTE'].apply(helper_fx.custom_round_hiring_needs)
talent_needs.to_excel(f'talent_needs/talent_needs_{today}.xlsx')
create_capbase.adjust_workbook_column_widths(f"talent_needs/talent_needs_{today}.xlsx")