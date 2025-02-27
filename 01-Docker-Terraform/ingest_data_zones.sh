#   python ingest_data.py \
# 	--user=root \
# 	--password=root \
# 	--host=localhost \
# 	--port=5432 \
# 	--db=ny_taxi \
# 	--table_name=yellow_taxi_trips \
# 	--url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"


docker run -it \
  --network=01-docker-terraform_default \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=zones \
    --url=${URL}