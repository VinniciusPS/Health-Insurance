# Create class and objects

import pickle
import numpy  as np
import pandas as pd

class HealthInsurance(object):
    
    def __init__( self ):
        self.home_path = r'C:\Users\psvin\Documents\repos\portfolio-DS\health_insurance'
        self.annual_premium_scaler =            pickle.load(open(self.home_path + r'\src\features\annual_premium_scaler.pkl'), encoding="utf8")
        self.age_scaler =                       pickle.load(open(self.home_path + r'\src\features\age_scaler.pkl'), encoding="utf8") 
        self.vintage_scaler =                   pickle.load(open(self.home_path + r'\src\features\vintage_scaler.pkl'), encoding="utf8") 
        self.target_encode_gender_scaler =      pickle.load(open(self.home_path + r'\src\features\te_gender_scaler.pkl'), encoding="utf8")
        self.target_encode_region_code_scaler = pickle.load(open(self.home_path + r'\src\features\te_region_code_scaler.pkl'), encoding="utf8")
        self.fe_policy_sales_channel_scaler =   pickle.load(open(self.home_path + r'\src\features\fe_policy_sales_channel_scaler.pkl'), encoding="utf8")
        
    def data_cleaning( self, df1 ):
        # 1.1. Rename Columns
        cols_new = ['id', 'gender', 'age', 'driving_license', 'region_code', 'previously_insured', 'vehicle_age', 
                    'vehicle_damage', 'annual_premium', 'policy_sales_channel', 'vintage', 'response']

        # rename 
        df1.columns = cols_new
        
        return df1 

    
    def feature_engineering( self, df2 ):
        # 2.0. Feature Engineering

        # Vehicle Damage Number
        df2['vehicle_damage'] = df2['vehicle_damage'].apply( lambda x: 1 if x == 'Yes' else 0 )

        # Vehicle Age
        df2['vehicle_age'] =  df2['vehicle_age'].apply( lambda x: 'over_2_years' if x == '> 2 Years' else 'between_1_2_year' if x == '1-2 Year' else 'below_1_year' )
        
        return df2
    
    
    def data_preparation( self, df5 ):
        # anual premium - StandarScaler
        df5['annual_premium'] = self.annual_premium_scaler.transform( df5[['annual_premium']].values )

        # Age - MinMaxScaler
        df5['age'] = self.age_scaler.transform( df5[['age']].values )

        # Vintage - MinMaxScaler
        df5['vintage'] = self.vintage_scaler.transform( df5[['vintage']].values )

        # gender - One Hot Encoding / Target Encoding
        df5.loc[:, 'gender'] = df5['gender'].map( self.target_encode_gender_scaler )

        # region_code - Target Encoding / Frequency Encoding
        df5.loc[:, 'region_code'] = df5['region_code'].map( self.target_encode_region_code_scaler )

        # vehicle_age - One Hot Encoding / Frequency Encoding
        df5 = pd.get_dummies( df5, prefix='vehicle_age', columns=['vehicle_age'] )

        # policy_sales_channel - Target Encoding / Frequency Encoding
        df5.loc[:, 'policy_sales_channel'] = df5['policy_sales_channel'].map( self.fe_policy_sales_channel_scaler )
        
        # Feature Selection
        cols_selected = ['annual_premium', 'vintage', 'age', 'region_code', 'vehicle_damage', 'previously_insured',
                         'policy_sales_channel']
        
        return df5[ cols_selected ]
    
    
    def get_prediction( self, model, original_data, test_data ):
        # model prediction
        pred = model.predict_proba( test_data )
        
        # join prediction into original data
        original_data['prediction'] = pred
        
        return original_data.to_json( orient='records', date_format='iso' )