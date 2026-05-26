import os
import logging
import pandas as pd


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[ logging.StreamHandler(), logging.FileHandler("file_logs.log") ])


def transform_data(df):
    
    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        logging.error("Transformation aborted: The incoming data is empty or NoneType!")
        return None
     
    logging.info("Starting data transformation")
     
    try :
          df.drop_duplicates(subset=["id"], inplace=True)
    
          logging.info(f"len of Data after dropping duplicate {len(df)}")
    
          df["date_posted"] = pd.to_datetime(df["date_posted"])
        
          df["organization"] = df["organization"].fillna("unknown")
    
          df["Country_location"] = df["Country_location"].replace({"GB":"UK"})
          
          df.columns = df.columns.str.lower()
    
          df=df.dropna()
    
          logging.info(f"rows len{len(df)} after transformation")
    
          df.to_csv("linkdin_job_data")
    
          logging.info("Data successfully Saved")
          
          logging.info(f"Transformation complete. Rows remaining: {len(df)}")
          
          #print(df)
          
          return df 
      
    except Exception as e:
        
        logging.info(f"Data Tranformation Failed  {e}")


    
    
    
     


