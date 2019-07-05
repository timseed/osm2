docker run -v /Users/tseed/Dev/Docker/openstreetmap-tile-server/hong-kong_china.osm.pbf:/data.osm.pbf  -v openstreetmap-data:/var/lib/postgresql/10/main  overv/openstreetmap-tile-server import

docker run -p 80:80 \
               -v openstreetmap-data:/var/lib/postgresql/10/main \
               -d overv/openstreetmap-tile-server \
               run

docker volume create openstreetmap-rendered-tiles
    docker run -p 80:80 \
               -v openstreetmap-data:/var/lib/postgresql/10/main \
               -v openstreetmap-rendered-tiles:/var/lib/mod_tile \
               -d overv/openstreetmap-tile-server \
               run
