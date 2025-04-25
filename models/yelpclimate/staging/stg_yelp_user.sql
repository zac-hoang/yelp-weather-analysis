select user_id
,review_count as user_review_count
,yelping_since as user_yelping_since
, useful as user_useful
,fans as user_fans
,elite as user_elite
,case
        when elite is null or elite = '' then 0
        else array_length(string_to_array(elite, ','), 1)
    end as user_elite_years
,average_stars as user_average_stars
from {{ source('raw','all_yelp_user')}}