{{ config(schema='staging')}}

with flattened_data as (
	{{ flatten_json(
		model_name = ref('raw_injuries'),
		json_column = '_airbyte_data'
	)}}
)

select
	casenumber,
	cast(age as int),
	bodypart,
	diagnosis,
	disposition,
	location,
	product,
	race,
	sex,
	cast(statweight as float),
	stratum,
	cast(treatmentdate as date)
from flattened_data