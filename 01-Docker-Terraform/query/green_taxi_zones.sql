SELECT 
z."Zone",SUM(total_amount) AS ta
FROM green_taxi_trips g
JOIN zones z ON z."LocationID" = g."PULocationID"
WHERE CAST(g.lpep_pickup_datetime AS DATE) = '2019-10-18'
GROUP BY z."Zone"
HAVING SUM(total_amount) > 13000
ORDER BY ta DESC