{{ config(materialized='view') }}
 
with tripdata as 
(
  select *,
    row_number() over(partition by cast(vendorid as STRING), cast(tpep_pickup_datetime as TIMESTAMP)) as rn
  from {{ source('staging','yellow_tripdata') }}
  where vendorid is not null 
)
select
   -- identifiers
    {{ dbt_utils.generate_surrogate_key(['vendorid', 'tpep_pickup_datetime']) }} as tripid,    
    {{ dbt.safe_cast("vendorid", api.Column.translate_type("integer")) }} as vendorid,
    {{ dbt.safe_cast("ratecodeid", api.Column.translate_type("integer")) }} as ratecodeid,
    {{ dbt.safe_cast("pulocationid", api.Column.translate_type("integer")) }} as pickup_locationid,
    {{ dbt.safe_cast("dolocationid", api.Column.translate_type("integer")) }} as dropoff_locationid,

    -- timestamps
    SAFE_CAST(tpep_pickup_datetime as timestamp) as pickup_datetime,
    SAFE_CAST(tpep_dropoff_datetime as timestamp) as dropoff_datetime,
    
    -- trip info
    store_and_fwd_flag,
    SAFE_CAST(passenger_count AS INT64) AS passenger_count,
    CAST(trip_distance AS NUMERIC) AS trip_distance,
    -- yellow cabs are always street-hail
    1 AS trip_type,
    
    -- payment info
    cast(fare_amount as numeric) as fare_amount,
    cast(extra as numeric) as extra,
    cast(mta_tax as numeric) as mta_tax,
    cast(tip_amount as numeric) as tip_amount,
    cast(tolls_amount as numeric) as tolls_amount,
    cast(0 as numeric) as ehail_fee,
    cast(improvement_surcharge as numeric) as improvement_surcharge,
    cast(total_amount as numeric) as total_amount,
    coalesce(safe_cast(payment_type as INT64), 0) as payment_type,
    {{ get_payment_type_description('payment_type') }} as payment_type_description,
    cast(congestion_surcharge as numeric) as congestion_surcharge,

    -- Add Service Type
    'Yellow' AS service_type

from tripdata
where rn = 1

-- dbt build --select <model.sql> --vars '{'is_test_run: false}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}