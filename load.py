import os
import pandas as pd 
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[ logging.StreamHandler(), logging.FileHandler("file_logs.log") ])


engine=create_engine(os.getenv("db_connection"))


from sqlalchemy import text
import pandas as pd
import logging

def upsert_table(df, table_name, connection):
    unique_ids = tuple(df['id'].tolist())
    
    if not unique_ids:
        return

    try:
        # 1. Mute safety checks on the current active connection channel
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        
        # 2. Execute the Delete stage safely
        if len(unique_ids) == 1:
            delete_query = text(f"DELETE FROM {table_name} WHERE id = :id_vals")
            connection.execute(delete_query, {"id_vals": unique_ids[0]})
        else:
            delete_query = text(f"DELETE FROM {table_name} WHERE id IN :id_vals")
            connection.execute(delete_query, {"id_vals": unique_ids})
        
        # 3. FIX: Pass 'con=connection' instead of 'connection.engine'
        # This keeps pandas trapped inside our zero-constraint transaction block!
        df.to_sql(table_name, con=connection, if_exists='append', index=False)
        
    finally:
        # 4. Turn checks back on safely
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        
        
def load_data(df):
    if df is None or df.empty:
        logging.warning("No data passed to the Load phase.")
        return False
        
    logging.info("Starting safe Upsert (Load) phase into Database...")
    
    with engine.begin() as connection:
        try:
            
            job_date_df = df[["id", "title", "date_posted", "date_validthrough"]].drop_duplicates(subset=['id']).copy()
            
            job_date_df.rename(columns={ "title": "Title", "date_posted": "date_posted",   "date_validthrough": "date_validthrough"}, inplace=True)
            upsert_table(job_date_df, "Job_Date", connection)
            
            logging.info("Loading Data into Job_Date Table Successful")
            
            org_df = df[["id", "organization", "organization_url"]].drop_duplicates(subset=['id']).copy()
            upsert_table(org_df, "Organization", connection)
            
            logging.info("Loading Data into organixayion Table Successful")
            
            location_df = df[["id", "country_location", 'address_locality']].drop_duplicates(subset=['id']).copy()
            
            location_df.rename(columns={"country_location": "Country_Location", "address_locality":"address_locality" }, inplace=True)
            upsert_table(location_df, "Job_location", connection)
            
            logging.info("Loading Data into Job_location Table Successful")
            
            logging.info("All data successfully synced to the database!")
            return True
             
        except Exception as e:
            logging.exception(f"Loading failed. Transaction rolled back. Error: {e}")
            return False