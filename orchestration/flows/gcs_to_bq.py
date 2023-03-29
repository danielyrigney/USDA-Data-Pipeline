from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(year: int, month: int, label: str) -> Path:
    """Download  data from GCS"""
    concat = f"{year}-{month:02}-28"
    gcs_path = f"data/{concat}-{label}.parquet"
    gcs_block = GcsBucket.load("zoom-gas")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"../data/{gcs_path}")


@task()
def read(path: Path) -> pd.DataFrame:
    """read the data into pandas"""
    df = pd.read_parquet(path)
    return df


@task()
def write_bq(df: pd.DataFrame, label: str) -> int:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    df.to_gbq(
        destination_table=f"dezoomcamp.{label}",
        project_id="thinking-prism-375117",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )
    return len(df)


@flow()
def el_gcs_to_bq(year: int, month: int, label: str) -> None:
    """Main ETL flow to load data into Big Query"""

    path = extract_from_gcs(year, month, label)
    df = read(path)
    row_count = write_bq(df, label)
    return row_count


@flow(log_prints=True)
def el_parent_gcs_to_bq(
    months: list[int] = [4, 10], year: int = 2021, labels: list[str] = ["branded_df", "food_df"]
):
    """Main EL flow to load data into Big Query"""

    for month in months:
        for label in labels:
            el_gcs_to_bq(year, month, label)



if __name__ == "__main__":
    el_parent_gcs_to_bq(months=[4, 10], year=2021, labels=["branded_df", "food_df"])





