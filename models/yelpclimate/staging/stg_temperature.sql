select
{{parse_yyyymmdd('date','date')}}
, min
,max
,normal_min
,normal_max

from {{ source('raw','all_temperature')}}