{% macro flatten_json(model_name, json_column) %}

{# Find all the keys in the embedded json #}
{% set json_col_query %}
SELECT DISTINCT json.key AS col_name
FROM {{ model_name }} t, 
    jsonb_each(t.{{ json_column }}) json
{% endset %}

{# Run the above query #}
{% set results = run_query(json_col_query) %}

{# Save the distinct column names into an array #}
{% if execute %}
{# Return the first column #}
{% set results_list = results.columns[0].values() %}
{% else %}
{% set results_list = [] %}
{% endif %}

{# Loop over an array to prepare the query #}
select
{% for col_name in results_list %}
    {% if col_name != '' %}
    {# [TODO]: Dynamic type detection #}
    {{ json_column }}::json->>'{{ col_name  }}' as {{ col_name  }}
    {% if not loop.last %},{% endif %}
    {% endif %}
{% endfor %}
from {{ model_name }}

{% endmacro %}