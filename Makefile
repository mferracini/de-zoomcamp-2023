
docker_insert_data:
	docker run -it \
	--network=de-zoomcamp-2023_de-zoomcamp-postgres \
		de-zoomcamp-insert_data \
		--user=root \
		--password=root \
		--host=pg-database \
		--port=5432 \
		--db=ny_taxi \
		--table_name=yellow_taxi_data\
		--url=trips \
		--if_exist=append 

local_insert_data:
	python src/pipeline.py --password=root \
		--host=localhost \
		--user=root \
		--port=5432 \
		--db=ny_taxi \
		--table_name=yellow_taxi_data\
		--url=trips \
		--if_exist=append 