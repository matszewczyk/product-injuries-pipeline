{{ config(schema='staging')}}

with flattened_data as (
	{{ flatten_json(
		model_name = ref('raw_products'),
		json_column = '_airbyte_data'
	)}}
)

select
	code,
	product_title
from flattened_data