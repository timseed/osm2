top = 18.65
left = 119.75
bottom = 12.533
right = 124.198
parts = 8
source_file = "/data.osm.pbf"

width = (right - left) / parts
height = (top - bottom) / parts
cmd = f"osmosis --read-pbf file={source_file} --bounding-box "
cmd2 = "--write-pbf file=luzon_part.pbf"
cmd3 = "osmconvert  luzon_part.pbf --drop-author --drop-version --out-osm -o=load.osm"

route = "osm2pgrouting -f load.osm --conf /home/renderer/src/osm2pgrouting/mapconfig.xml  --dbname gis --addnodes -h localhost -p 5432  -W tim -U postgres"
for x in range(0, int(parts)):
    for y in range(0, int(parts)):
        print(
            f"{cmd} top={top + -x * height} left={left + y * width} bottom={top - ((1 + x) * height)} right={left + ((1 + y) * width)} {cmd2}")
        print(f"{cmd3}")
        print("{} {}".format(route, "__clean" if (x == 0 and y == 0) else " "))
        print(f"{1+x * parts + y } of {parts * parts -1}")



