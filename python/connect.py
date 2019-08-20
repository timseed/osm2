import psycopg2

conn = psycopg2.connect(
    host='0.0.0.0',
    port=54320,
    dbname='gis',
    user='postgres',
)
cur = conn.cursor()
luzon_capital="""
select  pt.osm_id,
       pt.tags->'is_in:state' as state,
       pt.name as name,ST_X(ST_TRANSFORM(pt.way,4674)) AS LONG,
       ST_Y(ST_TRANSFORM(pt.way,4674)) AS LAT from planet_osm_point pt ,
       planet_osm_polygon poly
where defined(pt.tags,'capital') and
      poly.name='Luzon' and
      ST_Contains(poly.way, pt.way)
        order by lat,long;
"""
cur.execute(luzon_capital)
for row in cur:
    print(row)

conn.commit()
cur.close()
conn.close()
