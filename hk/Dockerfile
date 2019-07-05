FROM overv/openstreetmap-tile-server

# Set up environment
ENV TZ=UTC
ENV AUTOVACUUM=on
ENV UPDATES=disabled
ENV THREADS=20


# Start running
USER root
COPY run.sh /
COPY indexes.sql /
COPY hk_ph.pbf /data.osm.pbf
ENTRYPOINT ["/run.sh","import"]
CMD []

