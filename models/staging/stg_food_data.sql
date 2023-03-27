{{ config(materialized='view') }}

-- stg_food_data.sql

-- Define the stg_food_data model
-- This model selects all columns from the my_table source table
-- and casts the appropriate data types for each column
-- The model also adds a 'loaded_at' column to track when data was loaded
SELECT
  id,
  fdc_id,
  nutrient_id,
  amount,
  data_points,
  derivation_id,
  min,
  max,
  median,
  loq,
  footnote,
  min_year_acquired,
FROM {{ source('staging', 'food_nutrients') }}