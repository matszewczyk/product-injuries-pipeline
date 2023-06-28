with injuries as (
    select * from {{ ref("injuries_enriched")}}
)


select
    *
from injuries