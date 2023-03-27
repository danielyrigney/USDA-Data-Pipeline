{{ config(materialized='table') }}

select 
    fdc_id,
    data_type, 
    description, 
    food_category_id,
    publication_date
from {{ source('core', 'food_df') }}