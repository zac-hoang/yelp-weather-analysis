select business_id
,name as business_name
,address as business_address
,city as business_city
,state as business_state
,stars as business_stars
,review_count as business_review_count
,categories as business_categories
,"attr_RestaurantsDelivery" as business_restaurants_delivery
,"attr_OutdoorSeating" as business_outdoorseating
from {{ source('raw','all_yelp_business')}}