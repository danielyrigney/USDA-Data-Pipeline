{{ config(materialized='table') }}

with food_data as (
    select *
    from {{ ref('stg_food_data') }}
), 

dim_names as (
    select * from {{ ref('dim_food_names') }}
)

dim_nutrients as (
    select * from {{ ref('dim_nutrient_codes') }}
)

dim_brands as (
    select * from {{ ref('dim_brands') }}
)

select 
   
from food_data
inner join dim_zones
on trips_unioned.pickup_locationid = pickup_zone.locationid
inner join dim_zones
on trips_unioned.dropoff_locationid = dropoff_zone.locationid