with raw_injuries as (
    select * from {{ source('injuries', 'raw_products')}}
)

SELECT
    *
FROM
 raw_injuries