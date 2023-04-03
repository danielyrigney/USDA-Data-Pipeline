# USDA Nutrient Data Pipeline
### Pulls nutrient data from USDA websites, transforms data, uploads to GCP Datalake and BigQuery, dbt used to create models and finally visualizations created with Power BI. 

### Technologies used:
Containerization: [Docker](https://www.docker.com)  
Infrastructure as Code: [Terraform](https://www.terraform.io)      
Data Transformation: [dbt](https://www.getdbt.com)  
Workflow Orchestration: [Prefect](https://www.prefect.io)   
Data Lake: [Google Cloud Storage](https://cloud.google.com/storage)     
Data Warehouse: [Google BigQuery](https://cloud.google.com/bigquery)    
Visualisation: [Power BI](https://powerbi.microsoft.com/en-us/)     


![alt text](https://github.com/danielyrigney/USDA-Data-Pipeline/blob/cdf8a02ec7ddb54f4dac5368bccf630575e5374a/images/Screen%20Shot%202023-04-02%20at%2012.38.03%20AM.png "Flow Chart")

Problem: Added sugar to processed foods sold in the US and around the world is a significant source of concern to health agency, doctors, and individual consumers. The United States Department of Agriculture's FoodData Central provides information on millions of branded food products. We will use the data provided by the USDA to explore added sugar in the food we eat


STEP 1: Create and Configure virtual environment in Google Cloud Platform
1. Create SSH Key 
    - Follow [instructions](https://www.ssh.com/academy/ssh/keygen) to create an ssh key in your .ssh folder (` cd .ssh/ ` from root directory)
2. Create GCP virtual instance
    - Update VM IP address in ` .ssh/config file ` 
    - Connect to VM with 'ssh <name_of_vm_instance>' 
3. Install Anaconda on virtual machine
4. Install Docker on virtual machine 
5. Install Docker Compose on virtual machine
6. Install [Terraform](https://www.terraform.io/downloads)
7. Google Cloud SDK for Ubuntu
8. Create a Google Cloud Project with ID nutrient-data 
    - Go to IAM and create a Service Account with these roles:
        - BigQuery Admin
        - Storage Admin
        - Storage Object Admin
        - Viewer
    - Download the Service Account credentials, rename it to ` nutrient-data.json ` and store it in ` $HOME/.google/credentials/ `
7. Clone repo into virtual machine 


STEP 2: Initialize Terraform and run the Prefect flows 
1. Initialize Terraform
    - Open variables.tf and modify:
        - variable "project" to your own project id 
        - variable "region" to your project region
        - variable "credentials" to your credentials path
    - From the main directors `cd terraform` and then input the following
        - `terraform init`
        - `terraform plan`
        - `terraform apply`
2. Build and deploy Prefect flows 
    - In the main directory run the following in your terminal: 
        - `prefect deployment build orchestration/flows/web_to_gcs.py:etl_parent_flow -n "Web to GCS"`
        - `prefect deployment apply etl_parent_flow-deployment.yaml`
        - `prefect deployment build orchestration/flows/gcs_to_bq.py:el_parent_gcs_to_bq -n "GCS to BQ"`
        - `prefect deployment apply el_parent_gcs_to_bq-deployment.yaml`
        - `prefect agent start -q 'default`
    - In a terminal, run `prefect orion start`
    - Open the URL that the terminal produces and run the "Web to GCS" flow in the GUI. 
    - Once the flows finish, run the "GCS to BQ" flows. 

STEP 3: Transform the data and visualize 
1. 


2. Power BI 




STEPS: 
1) Create Docker container on GCP cloud instance
    - 4 points: The project is developed in the cloud and IaC tools are used
2) Create a pipeline for processing this dataset and putting it to a datalake
    - 4 points: End-to-end pipeline: multiple steps in the DAG, uploading data to data lake
3) Create a pipeline for moving the data from the lake to a data warehouse
    - 4 points: Tables are partitioned and clustered in a way that makes sense for the upstream queries (with explanation)
    - Tables needed for the DW: 
        - branded_food.csv - has the brand name, #fdc_id is the PK, and the #ingredients 
        - food.csv - has the food name 
        - food_nutrient.csv - this is the fact table that indicates the nutrients in each food. It links #fdc_id with #nutrient_id. We want the "amount" of each nutrient. 
        - nutrient.csv - links #nutrient_id with the name of the nutrient and the unit of measure (#unit_name)
4) Transform the data in the data warehouse: prepare it for the dashboard
    - 4 points: Tranformations are defined with dbt, Spark or similar technologies










