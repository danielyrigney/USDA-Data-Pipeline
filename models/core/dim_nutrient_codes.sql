{{ config(materialized='table') }}

select 
    id, 
    name, 
    unit_name, 
    nutrient_nbr
from {{ source('core', 'nutrient_df') }}


