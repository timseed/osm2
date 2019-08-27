from math import sqrt
from utils import get_data
import psycopg2

conn = psycopg2.connect(
    host='0.0.0.0',
    port=54320,
    dbname='gis',
    user='postgres',
)
data = get_data()
cur = conn.cursor()
cur.execute("delete from tour;")
for r in data:
    cur.execute(f"insert into tour (name, geom)   values ('{r[1]} {r[2]}',ST_SetSRID(ST_Point({r[3]},{r[4]}),4326));")
print("ok")