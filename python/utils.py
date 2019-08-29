from dataclasses import dataclass
from math import sqrt

import psycopg2
from psycopgr import PgrNode

@dataclass
class Province:
    id: int
    state: str
    name: str
    lon: float
    lat: float


def distance(lng1: float, lat1: float, lng2: float, lat2: float) -> float:
    # All distances are in Units of 60
    x_dist = abs(lng1 - lng2)
    y_dist = abs(lat1 - lat2)
    return sqrt(abs((x_dist * x_dist) - (y_dist * y_dist))) * 60.0


def get_data() -> list:
    rv = []
    conn = psycopg2.connect(
        host='0.0.0.0',
        port=54320,
        dbname='gis',
        user='postgres',
    )
    cur = conn.cursor()
    luzon_capital = """
    select  pt.osm_id,
       pt.tags->'is_in:state' as state,
       pt.name as name,ST_X(ST_TRANSFORM(pt.way,4674)) AS LONG,
       ST_Y(ST_TRANSFORM(pt.way,4674)) AS LAT from planet_osm_point pt ,
       planet_osm_polygon poly
       where defined(pt.tags,'capital') and  
       defined(pt.tags,'is_in:state') and  
       poly.name='Luzon' and
      ST_Contains(poly.way, pt.way)
        order by name;
    """
    cur.execute(luzon_capital)
    for row in cur:
        # print(row)
        rv.append(Province(*row))

    conn.commit()
    cur.close()
    conn.close()
    return rv


def findName(list_of_postgres_nodes: list, node_name: str) -> tuple or None:
    """
    Find the matching Namefrom a list of Geo Objects.
    Warning returns the 1st object found

    [(30917648, 'Tarlac', 'Tarlac City', 120.589556, 15.4859970004507),
    (198491046, 'Cagayan', 'Tuguegarao', 121.7327065, 17.6125761007424)....]
    :param list_of_postgres_nodes: [(osm_id, Area, Name, Long, Lat),,,,,]
    :param node_name: Name
    :return: Compete Tuple or None
    """
    for item in list_of_postgres_nodes:
        if item[2] == node_name:
            return item
    return None


def findArea(list_of_postgres_nodes: list, area_name: str) -> tuple or None:
    """
        Find the matching Area from a list of Geo Objects
        Warning returns the 1st object found

       [(30917648, 'Tarlac', 'Tarlac City', 120.589556, 15.4859970004507),
       (198491046, 'Cagayan', 'Tuguegarao', 121.7327065, 17.6125761007424)....]
       :param list_of_postgres_nodes: [(osm_id, Area, Name, Long, Lat),,,,,]
       :param node_name: Name
       :return: Compete Tuple or None
       """
    for item in list_of_postgres_nodes:
        if item[1] == area_name:
            return item
    return None


def toPgrNode(row: tuple) -> PgrNode:
    """
    Convert from (osm_id, Area, Name, Long, Lat) to
                (Name,Long,Lat)
    :param row: PgrNode(Area+Name, Long, Lat)
    :return: (Name,Long,Lat)
    """
    return PgrNode(row[1] + ' ' + row[2], lon=row[3], lat=row[4])
