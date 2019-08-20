FROM overv/openstreetmap-tile-server

# Set up environment
ENV TZ=UTC
ENV AUTOVACUUM=on
ENV UPDATES=disabled
ENV THREADS=20

run apt-get update && apt-get install -y vim net-tools &&\
    echo "listen_addresses = \'*\'"       >> /etc/postgresql/10/main/postgresql.custom.conf && \
    echo "host all all 0.0.0.0/0 trust"   >> /etc/postgresql/10/main/pg_hba.conf

# Start running
USER root
COPY run.sh /
COPY indexes.sql /
COPY ph.pbf /data.osm.pbf
ENTRYPOINT ["/run.sh","import"]
CMD []

