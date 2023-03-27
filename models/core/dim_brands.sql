{{ config(materialized='table') }}

select 
    fdc_id,			
    brand_owner,				
    brand_name,			
    subbrand_name,				
    ingredients,			
    not_a_significant_source_of,				
    serving_size,			
    serving_size_unit,				
    household_serving_fulltext,				
    branded_food_category,				
    data_source,				
    package_weight,				
    modified_date,				
    available_date,				
    market_country,				
    discontinued_date	
from {{ source('core', 'branded_df') }}