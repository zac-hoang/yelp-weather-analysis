select
{{parse_yyyymmdd('date','date')}}
, case when precipitation is null or precipitation = 'T' then 0.0
    else cast(precipitation as double precision)
    end as precipitation
, precipitation_normal

from {{ source('raw','all_lv_precipitation')}}