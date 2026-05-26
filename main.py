import logging 
from extract import extract_data
from transform import transform_data
from load import load_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[ logging.StreamHandler(), logging.FileHandler("file_logs.log") ])


def run_pipeline():
    
    logging.info("--- PIPELINE STARTING ----")
    
    
    raw_df = extract_data()
    if raw_df is None:
        logging.error("Pipeline Aborted: Extraction phase returned nothing.")
        return  
        
    
    cleaned_df = transform_data(raw_df)
    if cleaned_df is None:
        logging.error("Pipeline Aborted: Transformation phase failed.")
        return  
        
    
    load_success = load_data(cleaned_df)
    if load_success:
        logging.info("Pipeline executed successfully from end-to-end!")
        
if __name__ == "__main__":
 run_pipeline()
            