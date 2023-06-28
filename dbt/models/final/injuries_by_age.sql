with injuries as (
    select * from {{ ref("injuries_enriched")}}
)


select
    age,
    count(1) as no_of_accidents
from injuries
group by age