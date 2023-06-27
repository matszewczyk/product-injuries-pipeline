{# {{ config(schema='raw') }} #}

with raw_injuries as (
    select * from {{ source('injuries', 'raw_injuries')}}
)

SELECT
    *
FROM
 raw_injuries