-=Overall goal of this README - someone who has set up a GCP account, and nothing else, should be able to follow the instructions to get the files uploaded into BQ and the models created=- 


Problem: Added sugar to processed foods sold in the US and around the world is a significant source of concern to health agency, doctors, and individual consumers. The Food and Drug Administrations FoodData Central provides information on millions of branded food products. We will use the data provided by the FDA to determine: (1) Percentage of branded food that has sugar as one of the first 5 ingredients in the ingredients list overall and overtime and (2) Determine total grams of sugar 

Instructions can be completed from 

STEP 1: Create virtual environment in Google Cloud Platform
    - Create SSH Key 
        Follow instructions at https://www.ssh.com/academy/ssh/keygen to create an ssh key in your .ssh folder ('cd .ssh/' from root directory)
    - Create GCP virtual instance
        - Update VM IP address in .ssh/config file 
        - Connect to VM with 'ssh <name_of_vm_instance>' 
    - Install Anaconda on virtual machine
        [Add ]
    - Install Docker on virtual machine 
    - Install Docker Compose on virtual machine
    - Install Terraform 
    - Clone repo into virtual machine 

https://fdc.nal.usda.gov/download-datasets.html

https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_csv_2021-04-28.zip
https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_csv_2021-10-28.zip
https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_csv_2022-04-28.zip
https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_csv_2022-10-28.zip

base URI = https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_csv_{year}-{month}-28.zip
(year will only be 2022 and 2021, for now; month will only be '04' or '10') 

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









