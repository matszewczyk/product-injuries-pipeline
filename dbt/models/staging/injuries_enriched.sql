{{ config(
    materialized='table'
)}}

with injuries as (
    select * from {{ ref("injuries_flattened")}}    
),
products as (
    select *from {{ ref("products_flattened")}}
)

select 
    casenumber, 
    age, 
    bodypart, 
    diagnosis, 
    disposition, 
    location, 
    race, 
    sex, 
    statweight, 
    stratum,
    treatmentdate,
    code, 
    product_title as product
from injuries
join products on injuries.product = products.code