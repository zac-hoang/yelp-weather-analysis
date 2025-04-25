select review_id
,business_id
,user_id
,stars
,useful
, cast(date_trunc('day',cast(date as timestamp)) as date) as review_date
 from {{ source('raw','all_yelp_review')}}