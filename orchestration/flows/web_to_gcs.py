
from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect.tasks import task_input_hash
from datetime import timedelta
import os
import zipfile
import urllib.request


@task(retries=3)
def fetch(dataset_url: str, dataset_file: str) -> list:
    """Read nutrition data from web into pandas a list of DataFrames"""


    file_name = f"FoodData_Central_csv_{dataset_file}.zip"
    path = os.path.join(os.path.expanduser("~"), "Desktop/de_project_nutrient_data/data/", file_name)
    
    urllib.request.urlretrieve(dataset_url, path)

    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall("/Users/danielrigney/Desktop/de_project_nutrient_data/data/")

    # Define the filenames of the 3 files you want to read into a pandas dataframe
    file1_name = 'branded_food.csv'
    file2_name = 'food.csv'
    file3_name = 'food_nutrient.csv'

    path = f"/Users/danielrigney/Desktop/de_project_nutrient_data/data/FoodData_Central_csv_{dataset_file}"
    
    # Read the 3 files into pandas dataframes
    branded_df = pd.read_csv(os.path.join(path, file1_name))
    food_df = pd.read_csv(os.path.join(path, file2_name))
    nutrient_df = pd.read_csv(os.path.join(path, file3_name))

    df_list = [branded_df, food_df, nutrient_df]

    return df_list


@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = Path(f"data/{dataset_file}-{df.name}.parquet")
    df.to_parquet(path, compression="gzip")
    return path

@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gas")
    gcs_block.upload_from_path(from_path=path, to_path=path, timeout=600)
    return

@flow()
def etl_web_to_gcs(year: int, month: int) -> None: 
    """The main ETL function"""
    dataset_file = f"{year}-{month}-28"
    dataset_url = f"https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_csv_{dataset_file}.zip"

    list = fetch(dataset_url, dataset_file) # this will be a local file path 


    for x, df in enumerate(list):
        if x == 0:
            df.drop('gtin_upc', axis=1, inplace=True)
            df.name = "branded_df"
        if x == 1:
            df.name = "food_df"   
        if x == 2:
            df.name = "nutrient_df"
       
        path = write_local(df, dataset_file)
        write_gcs(path)

@flow()
def etl_parent_flow(
    months: list[int] = [10], year: int = 2021
):
    for month in months:
        etl_web_to_gcs(year, month)


if __name__ == "__main__":
    months = [10]
    year = 2021
    etl_parent_flow(months, year)
