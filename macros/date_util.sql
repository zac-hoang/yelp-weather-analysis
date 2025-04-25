{% macro parse_yyyymmdd(date_col, alias='date') %}
    to_date(cast({{ date_col }} as text), 'YYYYMMDD') as {{ alias }}
{% endmacro %}
