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


![Flow chart of the technologies used](https://github.com/danielyrigney/USDA-Data-Pipeline/blob/cdf8a02ec7ddb54f4dac5368bccf630575e5374a/images/Screen%20Shot%202023-04-02%20at%2012.38.03%20AM.png "Flow Chart")

Problem: Added sugar to processed foods sold in the US and around the world is a significant source of concern to health agency, doctors, and individual consumers. The United States Department of Agriculture's FoodData Central provides information on millions of branded food products. We will use the data provided by the USDA to explore added sugar in the food we eat


STEP 1: Create and Configure virtual environment in Google Cloud Platform
1. Create a new project in [Google Cloud Platform](https://console.cloud.google.com/) 
2. Create SSH Key 
    - Follow [instructions](https://www.ssh.com/academy/ssh/keygen) to create an ssh key. 
    - Put the private key in your .ssh folder (` cd .ssh/ ` from root directory)
    - Upload the public key to the Google Cloud in the Metadata section of the virtual machine
3. Create GCP virtual instance
    - Update VM IP address in ` .ssh/config file ` 
    - Connect to VM with `ssh <name_of_vm_instance>` 
4. Install [Anaconda](https://www.anaconda.com/products/distribution#Downloads) on virtual machine
5. Install Docker on virtual machine by running `sudo apt-get install docker.io` (Use [Docker without Sudo](https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md)) 
6. Install [Docker Compose](https://github.com/docker/compose/releases) on virtual machine
7. Install [Terraform](https://www.terraform.io/downloads)
8. GCP Setup
    - Setup [service account & authentication](https://cloud.google.com/docs/authentication/getting-started) for this project
        - Grant `Viewer` role to begin with.
        - Download service-account-keys (.json) for auth.
    - Download [SDK](https://cloud.google.com/sdk/docs/quickstart) for local setup
    - Set environment variable to point to your downloaded GCP keys
        ```python
            export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
            
            # Refresh token/session, and verify authentication
            gcloud auth application-default login
        ```
8. GCP Access
    - [IAM Roles](https://cloud.google.com/storage/docs/access-control/iam-roles) for Service account:
        - Go to the *IAM* section of *IAM & Admin* https://console.cloud.google.com/iam-admin/iam
        - Click the *Edit principal* icon for your service account.
        - Add these roles in addition to Viewer: **Storage Admin + Storage Object Admin + BigQuery Admin** 
    - Enable these APIs for your project:
        - https://console.cloud.google.com/apis/library/iam.googleapis.com
        - https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com  
    - Ensure GOOGLE_APPLICATION_CREDENTIALS env-var is set
        ```python 
            export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
        ``` 
11. Clone repo into virtual machine 


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
1. Connect dbt and build and run the models to create the fact tables and analysis 
2. Connect Big Query to Power BI (or any other visualization method) and create the visualizations  

![alt text](https://github.com/danielyrigney/USDA-Data-Pipeline/blob/7b2afb174312d8496b306334c758c2debedd38fa/images/Screen%20Shot%202023-04-02%20at%2012.24.21%20AM.png "Visualization")
