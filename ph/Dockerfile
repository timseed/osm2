FROM overv/openstreetmap-tile-server

# Set up environment
ENV TZ=UTC
ENV AUTOVACUUM=on
ENV UPDATES=disabled
ENV THREADS=20

run apt-get update && apt-get install -y vim net-tools postgresql-10-pgrouting libpqxx-dev osmctools &&\
    echo "listen_addresses = \'*\'"       >> /etc/postgresql/10/main/postgresql.custom.conf && \
    echo "host all all 0.0.0.0/0 trust"   >> /etc/postgresql/10/main/pg_hba.conf

# Start running
USER root
COPY run.sh /
COPY indexes.sql /
COPY ph.pbf /data.osm.pbf
WORKDIR /home/renderer/src
COPY osm2pgrouting /home/renderer/src/osm2pgrouting/
RUN  ls /home/renderer/src  && sleep 10s && cd osm2pgrouting && \
    cmake -H. -Bbuild && \
    cd build/ &&\
    make &&\
    make install 
ENTRYPOINT ["/run.sh","import"]
CMD []

