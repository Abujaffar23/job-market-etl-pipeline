import os
import requests 
import logging
import pandas as pd


logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[ logging.StreamHandler(), logging.FileHandler("file_logs.log")])


logging.info("ETL Pipeline Started")

def extract_data():
    
      try : 
    
           #url="https://linkedin-job-search-api.p.rapidapi.com/active-jb-6m"
    
          # Api_keys={"x-rapidapi-key" : os.getenv("job_Api"),  "x-rapidapi-host": "linkedin-job-search-api.p.rapidapi.com","Content-Type": "application/json"}
    
          # querystring = {"offset":"100","title_filter":"\"Data Engineer\" OR \"Data Analyst\"","location_filter":"\"United States\" OR \"United Kingdom\"","description_type":"text"}
    
          # response=requests.get(url,   headers=Api_keys,   params=querystring)
           
          # if response.status_code == 200:
               
              # logging.info("Api request successfully")
               
              # data = response.json()
               
          # else:
               
              # logging.error(f"Api request Failed with status code {response.status_code}")
              # return None
            
            
          # records=[]
       
         #  for job in data:
               
          #     try: 
                   
           #        records.append({
            #       "id":job["id"],
             #      "Title":job["title"],
              #     "data_posted":job["date_created"],
               #    "date_validthrough":job['date_validthrough'],
                #   "Organization":job['organization'],
                 #  "Organization_url":job['organization_url'],
                  # "Country_Location":job['locations_raw'][0]['address']['addressCountry'],
                  #"AddressLocality":job['locations_raw'][0]['address']['addressLocality'],
                  # "Employment_type":job["employment_type"][0]
                  #})
                   
               #except (KeyError, IndexError) as item_error:
                   
                #logging.warning(f"Skipping a job record due to missing key: {item_error}")
                
                #continue
            
           df = pd.read_csv("Linkdin_data_engineer_job.csv")
           
           logging.info(f"len of Data before Tranformation is {len(df)}")
           
           return df
           
           
      except Exception as e:
        
        logging.info(f"Extraction Failed {e}")
        
raw_dataframe = extract_data()


               
               
               
            
               

    

