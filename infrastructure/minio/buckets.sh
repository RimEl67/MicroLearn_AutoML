#!/bin/sh

mc alias set local http://minio:9000 minioadmin minioadmin123

mc mb local/raw-datasets
mc mb local/processed-datasets
mc mb local/models
mc mb local/reports
