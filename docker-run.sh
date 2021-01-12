#!/bin/sh

curdir=$(dirname "$(readlink -f ./run-docker.sh)")

docker build -t fx_converter "$curdir"

# docker run \
# 	--env SQLALCHEMY_DATABASE_URI='sqlite:///fx.db' \
# 	-p 5000:5000 \
# 	-t fx_converter:latest

docker run \
	--mount type=bind,source="$curdir/db,target=/mnt/db" \
	--env SQLALCHEMY_DATABASE_URI='sqlite:////mnt/db/fx.db' \
	-p 5000:5000 \
	-t fx_converter:latest
