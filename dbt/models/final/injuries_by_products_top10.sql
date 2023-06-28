with injuries as (
    select * from {{ ref("injuries_enriched")}}
)

select
    product,
    count(1) as no_of_accidents
from injuries
group by product
order by count(1) desc
limit 10