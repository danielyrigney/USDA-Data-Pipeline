{{ config(materialized='table') }}

with food_data as (
    select *
    from {{ ref('stg_food_data') }}
), 

dim_names as (
    select * 
    from {{ ref('dim_food_names') }}
),

dim_nutrients as (
    select * 
    from {{ ref('dim_nutrient_codes') }}
),

dim_brands as (
    select * 
    from {{ ref('dim_brands') }}
)

select 
food_data.fdc_id, 
dim_names.description,
dim_brands.brand_owner,
dim_brands.brand_name,   
dim_nutrients.name, 
food_data.amount,
dim_nutrients.unit_name


   
from food_data
inner join dim_names
on food_data.fdc_id = dim_names.fdc_id
inner join dim_nutrients
on food_data.nutrient_id = dim_nutrients.id
inner join dim_brands
on food_data.fdc_id = dim_brands.fdc_id
