WITH max_trip_per_day AS (
    SELECT
        CAST(lpep_pickup_datetime AS DATE) AS pickup_date,
        MAX(trip_distance) AS max_distance
    FROM green_taxi_trips
    GROUP BY CAST(lpep_pickup_datetime AS DATE)
)
SELECT
    pickup_date,
    max_distance
FROM max_trip_per_day
ORDER BY max_distance DESC
LIMIT 1;