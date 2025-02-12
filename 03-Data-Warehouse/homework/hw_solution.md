# HW Solution

Create External Table:
```sql
CREATE OR REPLACE EXTERNAL TABLE nodal-empire-447803-h7.hw3_zoomcamp.external_yellow_tripdata
OPTIONS (
  format = 'parquet',
  uris = ['gs://bucket-nodal-empire-447809-h7/yellow_tripdata_2024-*.parquet']
);
```

Create Martialize Table:

```sql
CREATE OR REPLACE TABLE `nodal-empire-447803-h7.hw3_zoomcamp.materialized_yellow_tripdata`
AS 
SELECT * FROM `nodal-empire-447803-h7.hw3_zoomcamp.external_yellow_tripdata`;
```

## Question 1: What is count of records for the 2024 Yellow Taxi Data?
```sql
SELECT COUNT(*) as count FROM `nodal-empire-447803-h7.trip_hw3.external_yellow_tripdata`
```
Result:
Count = 20332093

## Question 2 Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

```sql
SELECT count(distinct PULocationID) FROM `nodal-empire-447803-h7.trip_hw3.external_yellow_tripdata` 

SELECT count(distinct PULocationID) FROM `nodal-empire-447803-h7.trip_hw3.materialize_yellow_tripdata` 
```
result: both table have estimated 155.12 MB read of data

## Question 3 Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?
```sql
SELECT 
  PULocationID, DOLocationID
FROM `nodal-empire-447803-h7.trip_hw3.materialized_yellow_tripdata`
SELECT 
  PULocationID
FROM `nodal-empire-447803-h7.trip_hw3.materialized_yellow_tripdata`
```

BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.


## Question 4 How many records have a fare_amount of 0?
```sql
SELECT COUNT(*) as count_fare_amount FROM `nodal-empire-447803-h7.trip_hw3.materialized_yellow_tripdata` 
WHERE fare_amount = 0 
```
result: 8,333

## Question 5 What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)

Answer: Partition by tpep_dropoff_datetime and Cluster on VendorID
```sql 
CREATE OR REPLACE TABLE `nodal-empire-447803-h7.trip_hw3.yellow_tripdata_optimized`
PARTITION BY DATE(tpep_dropoff_datetime)  -- Partitioning by date
CLUSTER BY VendorID  -- Clustering on VendorID
AS
SELECT * FROM `nodal-empire-447803-h7.trip_hw3.materialized_yellow_tripdata`;

```

## Question 6 Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive) Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?

```sql
SELECT DISTINCT VendorID 
FROM `nodal-empire-447803-h7.trip_hw3.materialized_yellow_tripdata`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```
Result: 310.24 MB

```sql
SELECT DISTINCT VendorID 
FROM `nodal-empire-447803-h7.trip_hw3.yellow_tripdata_optimized`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```
result: 26.84 MB


## Question 7 Where is the data stored in the External Table you created?
Answer: GCP Bucket

## Question 8 It is best practice in Big Query to always cluster your data?
Answer: False

## Question 9: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

```sql
SELECT count(*) FROM `nodal-empire-447803-h7.trip_hw3.materialized_yellow_tripdata` 
```

read bytes: 0  beacuse : The estimated bytes read is 0 because of BigQuery's metadata caching.