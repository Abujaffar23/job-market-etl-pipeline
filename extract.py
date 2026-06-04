import os
import requests 
import logging
import pandas as pd


logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[ logging.StreamHandler(), logging.FileHandler("file_logs.log")])


logging.info("ETL Pipeline Started")

def extract_data():
    
     try : 
    
           url="https://linkedin-job-search-api.p.rapidapi.com/active-jb-6m"
           
           
           Api_keys={"x-rapidapi-key" : os.getenv("Api_key"), 'x-rapidapi-host': "linkedin-job-search-api.p.rapidapi.com",
                    'Content-Type': "application/json"}
    
           querystring = {"limit":"100","title_filter":"\"Data Engineer\" OR \"Data Analyst\"","location_filter":"\"United States\" OR \"United Kingdom\"","description_type":"text"}
    
           response=requests.get(url,   headers=Api_keys,   params=querystring)
           
           if response.status_code == 200:
               
               logging.info(f"Api request successfully {response.status_code}")
               
               data = response.json()
               
           else:
               
               logging.error(f"Api request Failed with status code {response.status_code}")
               
               return None
            
            
           records = []

           for job in data:
               
            try:
               
                locations = job.get("locations_raw") or []
                if locations and isinstance(locations, list):
                    address = locations[0].get("address") or {}
                    country = address.get("addressCountry")
                    locality = address.get("addressLocality")
                else:
                    country = None
                    locality = None

                employment_types = job.get("employment_type") or []
                emp_type = employment_types[0] if employment_types else None

                records.append({
                    "id": job.get("id"),
                    "Title": job.get("title"),
                    "date_posted": job.get("date_created"),
                    "date_validthrough": job.get("date_validthrough"),
                    "organization": job.get("organization"),
                    "organization_url": job.get("organization_url"),
                    "Country_Location": country,
                    "AddressLocality": locality,
                    "Employment_type": emp_type
                    })
                   
            except (KeyError, IndexError) as item_error:
                   
                    logging.warning(f"Skipping a job record due to missing key: {item_error}")
                    continue
            
           df = pd.DataFrame(records)
           
           logging.info(f"len of Data before Tranformation is {len(df)}")
           
           return df 
           
           
     except Exception as e:
        
        logging.error(f"Extraction Failed {e}")
        return None
        
raw_dataframe = extract_data()
 


               
               
               
            
               

    

