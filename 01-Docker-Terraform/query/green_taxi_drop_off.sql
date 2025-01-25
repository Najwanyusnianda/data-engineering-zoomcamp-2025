SELECT
    zdo."Zone",
    SUM(g.tip_amount) AS tips
FROM green_taxi_trips g
JOIN zones zdo ON zdo."LocationID" = g."DOLocationID"
JOIN zones zpu ON zpu."LocationID" = g."DOLocationID"
WHERE CAST(g.lpep_dropoff_datetime AS DATE) >= '2019-10-01'
  AND CAST(g.lpep_dropoff_datetime AS DATE) <= '2019-10-31'
  AND g."PULocationID"='74'
GROUP BY zdo."Zone"
ORDER BY tips DESC;