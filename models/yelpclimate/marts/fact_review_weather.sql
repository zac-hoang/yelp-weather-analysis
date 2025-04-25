with review as (
    select * from {{ ref('stg_yelp_review') }}
),
business as (
    select * from {{ ref('stg_yelp_business') }}
),
user_dim as (
    select * from {{ ref('stg_yelp_user') }}
),
precip as (
    select * from {{ ref('stg_precipitation') }}
),
temp as (
    select * from {{ ref('stg_temperature') }}
)

select 
    r.review_id,
    r.user_id,
    r.stars,
    r.useful,
    r.review_date,
    
    b.business_name,
    b.business_address,
    b.business_city,
    b.business_stars,
    b.business_review_count,
    b.business_restaurants_delivery,
    b.business_outdoorseating,
    b.business_categories,

    u.user_review_count,
    u.user_yelping_since,
    u.user_useful,
    u.user_fans,
    u.user_elite_years,
    u.user_average_stars,

    case 
        when p.precipitation > 0 then 'Has rain'
        else 'No rain'
    end as has_rain,

    case 
        when p.precipitation = p.precipitation_normal then 'Equal'
        when p.precipitation > p.precipitation_normal then 'More'
        else 'Less'
    end as precipitation_level,

    case 
        when t.min < t.normal_min and t.max > t.normal_max then 'More extreme'
        when t.min > t.normal_min and t.max < t.normal_max then 'Less extreme'
        when t.min = t.normal_min and t.max = t.normal_max then 'Equal'
        when t.min < t.normal_min and t.max <= t.normal_max then 'Cooler'
        when t.min >= t.normal_min and t.max > t.normal_max then 'Hotter'
        else 'Others'
    end as temperature_category

from review r
join business b on r.business_id = b.business_id
join user_dim u on r.user_id = u.user_id
join precip p on r.review_date = p.date
join temp t on r.review_date = t.date
where b.business_categories like '%Restaurants%'
and b.business_state = 'NV'
and r.review_date <= '2021-04-30'

