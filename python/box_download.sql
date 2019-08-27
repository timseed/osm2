select 'wget -O luzon.osm "https://api.openstreetmap.org/api/0.6/map?bbox="',
       min(LON),
       min(LAT),
       max(LON),
       max(LAT)
from (SELECT path,
             ST_AsText(geom),
             ST_X(ST_TRANSFORM(geom, 4674)) AS LON,
             ST_Y(ST_TRANSFORM(geom, 4674)) AS LAT
      from (
               select (ST_DumpPoints(poly.way)).*
               from planet_osm_polygon poly
               where poly.name = 'Luzon')
               as q1)
         as q2;
