import pandas as pd
import numpy as np
from simple_salesforce import Salesforce
import re

class SfQueries:
    """
    A class to interact with Salesforce API for fetching and processing data pulled from Salesforce.
    
    Attributes:
        sf (Salesforce): An instance of Salesforce connection initialized with username, password, and security token.
    """

    def __init__(self, username, password, security_token):
        """
        Initializes the Salesforce connection.
        
        Args:
            username (str): Salesforce username.
            password (str): Salesforce password.
            security_token (str): Security token for Salesforce login which you can find in your Salesforce profile.
        """
        self.sf = Salesforce(username=username, password=password, security_token=security_token)
        
    def convert_salesforce_data_to_df(self, data):
        """
        Converts Salesforce data records into a Pandas DataFrame, expanding nested dictionaries into columns.

        Parameters:
        - data (dict): The raw data returned from a Salesforce query, expected to contain a 'records' key.
        
        Returns:
        - DataFrame: A Pandas DataFrame with flattened nested dictionaries into separate columns.
        """
        # Convert the records part of the data into a DataFrame, dropping the 'attributes' column
        df = pd.DataFrame(data["records"]).drop("attributes", axis=1)
        
        # Initialize a list to keep track of all unique column names
        list_columns = list(df.columns)
        
        # Process nested dictionaries within columns
        for col in list_columns:
            # Check if any value in the column is a dictionary
            if any(
                isinstance(df[col].values[i], dict) for i in range(len(df[col].values))
            ):
                # Expand the nested dictionary into separate columns
                expanded_cols = df[col].apply(pd.Series, dtype=df[col].dtype).drop("attributes", axis=1).add_prefix(col + ".")
                df = pd.concat([df.drop(columns=[col]), expanded_cols], axis=1)
                
                # Update the list of column names with the newly added ones
                new_columns = np.setdiff1d(df.columns, list_columns)
                list_columns.extend(new_columns)
        
        return df
    
    def create_query(self, columns: str, table: str, conditions: dict):
        """
        Creates a SOQL query string based on specified columns and conditions.

        Args:
            columns (str): Comma-separated list of columns to select.
            conditions (dict): Conditions for the WHERE clause, where keys are column names
                               and values are the desired values.

        Returns:
            str: The constructed SOQL query string.
        """
        # Input validation
        if not isinstance(columns, str):
            raise ValueError("Columns must be a string")
        if not isinstance(conditions, dict):
            raise ValueError("Conditions must be a dictionary")
        
        # def sanitize_value(value):
        #     return value.replace("'", "\\'")
        
        # Ensure columns are properly formatted for the query
        columns = ", ".join(columns.split(","))

        # Start building the query with the SELECT clause
        query = f"SELECT {columns} FROM {table} WHERE "
        
        query_conditions = []
        for key, value in conditions.items():
            if type(value) == str:
                query_conditions.append(f"{key}= '{value}'")
            else:
                query_conditions.append(f"{key}= {value}")

        query += " AND ".join(query_conditions)#sanitize_value(value)

        return query
    
    def get_abstractor_assignments(self, contact_id=None, team_id=None):
        """
        Fetches abstractor assignments from Salesforce and processes the data.
        
        Args:
            contact_id (str, optional): Contact ID to filter assignments. Defaults to None.
            team_id (str, optional): Team ID to filter assignments. Defaults to None.
            
        Returns:
            DataFrame: DataFrame containing processed abstractor assignments.
        """
        # Validate that either contact_id or team_id is provided
        if contact_id is None and team_id is None:
            raise ValueError('Either contact_id or team_id must be provided.')
        
        # Handle empty strings explicitly
        if (contact_id is None or not contact_id.strip()) and (team_id is None or not team_id.strip()):
            raise ValueError("Either contact_id or team_id must be provided and must not be an empty string.")
        
        # Construct the WHERE clause based on whether a contact_id or team_id is provided
        conditions = {}
        if team_id is None:
            conditions['Id'] = contact_id
        else:
            conditions['ID__c'] = team_id
            
        conditions['Status__c !'] = 'Closed'
        # conditions['Team_Position__c'] = 'Abstractor'
        
        cols = """                        
                    Id,
                    Other_specific_column_names__c,
                    """
        
        # Execute the SOQL query and fetch the results
        query_result = self.sf.query(self.create_query(columns=cols, table='Assignment__c', conditions=conditions))
        # Process the fetched data into a DataFrame
        return self.convert_salesforce_data_to_df(query_result)
    
    def get_contact_id_from_CBIZ_Name(self, CBIZ_Name):
        if "'" in CBIZ_Name:
            CBIZ_Name = CBIZ_Name.replace("'", "\\'")
        try: 
            name_of_abstractor = CBIZ_Name.split(' - ')[0]
            cbiz_of_abstractor = int(CBIZ_Name.split(' - ')[1])
            conditions = {"AccountId": "Only_Abstractors",
                                            "Name": f"{name_of_abstractor}",
                                            "ID__c": cbiz_of_abstractor}
        except:
            try:
                CBIZ_Name = int(CBIZ_Name)
                conditions = {"AccountId": "Only_Abstractors",
                                "External_Employee_ID__c": CBIZ_Name}
            except:
                conditions = {"AccountId": "Only_Abstractors",
                                                "Name": f"{CBIZ_Name}"}
        result = pd.DataFrame(self.sf.query(self.create_query(columns="Name,External_Employee_ID__c,Id", 
                                                                                        table="Contact", 
                                conditions=conditions))['records']).drop(['attributes'],axis=1)
        if len(result) > 1:
            raise Exception(f"Multiple contacts found with the name {CBIZ_Name}. Please specify the CBIZ ID")
        elif len(result) == 0:
            raise Exception(f"No contact found with the name {CBIZ_Name}. Please specify the CBIZ ID")
        return result.Id.values[0]
    
    def get_ticket_id_from_number(self, ticket_number):
        return pd.DataFrame(self.sf.query(self.create_query(columns="Id,Number_of_Hours__c,Comments", table="Case", 
                                    conditions={"OwnerId": "specific_owner_id",
                                                "CaseNumber": f"000{ticket_number}",                                                
                                                "Status !": "Closed"}))['records']).drop(['attributes'],axis=1)
    
    def get_sr_from_request_name(self, request_name):
        return self.convert_salesforce_data_to_df(self.sf.query(self.create_query(columns="Id,other_column_names__c", 
                                                                                  table="Staffing_Request__c", 
                                conditions={"Name": f"{request_name}"})))
    
    def get_team_id_from_name(self, team_name):
        if team_name.startswith('a6i'):
            print('already an Id')
            return team_name
        result = pd.DataFrame(self.sf.query(self.create_query(columns="Name,Case_Safe_ID__c", table="QC_Team__c", 
                                    conditions={"Active__c": True,
                                                "Name": f"{team_name}"}))['records']).drop(['attributes'],axis=1)
        if len(result) > 1:
            raise Exception(f"Multiple teams found with the name {team_name}. Please specify the Case_Safe_ID__c")
        elif len(result) == 0:
            raise Exception(f"No team found with the name {team_name}. Please specify the Case_Safe_ID__c")
        
        return result.Case_Safe_ID__c.values[0]
    
    def get_sm_from_team_or_abs_id(self, name):
        # if name ends in '- ###' where ### could be any length of digits, then it is a CBIZ_Name otherwise it is a team name
        # if re.search(r'- \d+$', name) is not None:
        try:
            id = self.get_contact_id_from_CBIZ_Name(name)
            return self.convert_salesforce_data_to_df(self.sf.query(self.create_query(columns="ReportsTo.Email", table="Contact",
                                                                conditions={"Id": f"{id}"})))['ReportsTo.Email'].values[0]
        # else:
        except:
            id = self.get_team_id_from_name(name)
            return self.convert_salesforce_data_to_df(self.sf.query(self.create_query(columns="Senior_Manager__r.Email", table="QC_Team__c",
                                    conditions={"Case_Safe_ID__c": f"{id}"})))['Senior_Manager__r.Email'].values[0] #.drop(['attributes'],axis=1)
            
        
    def get_all_assignments(self, df, col_name):
        # loop through the CBIZ_Name column
        for _, row in df.iterrows():
            # get the assignments for the CBIZ_Name
            if col_name == 'CBIZ_Name':
                assignments = self.get_abstractor_assignments(
                    contact_id=self.get_contact_id_from_CBIZ_Name(row[col_name]))
            else:
                assignments = self.get_abstractor_assignments(
                    team_id=self.get_team_id_from_name(row[col_name]))
            # add the assignments to the all_assignments dataframe
            try:
                all_assignments = pd.concat([all_assignments, assignments])
            except:
                all_assignments = assignments
        return all_assignments