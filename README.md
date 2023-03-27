# FDA Nutrient Data Pipeline
### Pulls nutrient data from FDA websites, transforms data, uploads to GCP Datalake and BigQuery, dbt used to create models and finally visualizations created with Power BI. 

###Technologies used:
Containerization: Docker, Docker Compose  
Infrastructure as Code: Terraform
Data Transformation: Pandas
Workflow Orchestration: Prefect
Data Lake: Google Cloud Storage
Data Warehouse: Google BigQuery
Visualisation: Power BI

Problem: Added sugar to processed foods sold in the US and around the world is a significant source of concern to health agency, doctors, and individual consumers. The Food and Drug Administrations FoodData Central provides information on millions of branded food products. We will use the data provided by the FDA to determine: (1) Percentage of branded food that has sugar as one of the first 5 ingredients in the ingredients list overall and overtime and (2) Determine total grams of sugar 


STEP 1: Create and Configure virtual environment in Google Cloud Platform
1. Create SSH Key 
    - Follow instructions at https://www.ssh.com/academy/ssh/keygen to create an ssh key in your .ssh folder (` cd .ssh/ ` from root directory)
2. Create GCP virtual instance
    - Update VM IP address in ` .ssh/config file ` 
    - Connect to VM with 'ssh <name_of_vm_instance>' 
3. Install Anaconda on virtual machine
4. Install Docker on virtual machine 
5. Install Docker Compose on virtual machine
6. Install Terraform
7. Google Cloud SDK for Ubuntu
8. Create a Google Cloud Project with ID nutrient-data 
    - Go to IAM and create a Service Account with these roles:
        - BigQuery Admin
        - Storage Admin
        - Storage Object Admin
        - Viewer
    - Download the Service Account credentials, rename it to ` nutrient-data.json ` and store it in ` $HOME/.google/credentials/ `
7. Clone repo into virtual machine 


STEP 2: 



Download the Service Account credentials, rename it to de-r-stocks.json and store it in $HOME/.google/credentials/.
On the Google console, enable the following APIs:
IAM API
IAM Service Account Credentials API
Cloud Dataproc API
Compute Engine API
Set up the infrastructure on Google Cloud with Terraform

I recommend executing the following on VSCode.

Using VSCode + WSL, open the project folder de_r-stocks.

Open variables.tf and modify:

variable "project" to your own project id (I think may not be necessary)
variable "region" to your project region
variable "credentials" to your credentials path
Open the VSCode terminal and change directory to the terraform folder, e.g. cd terraform.

Initialise Terraform: terraform init

Plan the infrastructure: terraform plan

Apply the changes: terraform apply

If everything goes right, you now have a bucket on Google Cloud Storage called 'datalake_de-r-stocks' and a dataset on BigQuery called 'stocks_data'.







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
5) Create dashboard
    - 4 points: A dashboard with 2 tiles
6) Solid readme 
    - 4 points: Instructions are clear, it's easy to run the code, and the code works
7) Bonus: tests, use make, add CI/CD pipeline









