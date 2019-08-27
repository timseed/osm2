"""
OSM pbf to routing loader.
Because I am running on a docker and there are lots of loads in the map - I run out of memory.
So this is an attempt to automate the loading by splitting the map into "chunks" of equal sizes
and then loading the map piece by piece.

Things to note. This will drop all previous data per load. If this behavior is not wanted, look
for the "--clean" command. I will add a command line switch at some stage.

osmosis --read-pbf file=/data.osm.pbf --bounding-box  top=18.65 left=119.75 bottom=16.610999999999997 right=121.23266666666666 --write-pbf file=luzon_part.pbf
osmconvert  luzon_part.pbf --drop-author --drop-version --out-osm -o=load.osm
osm2pgrouting -f load.osm --conf /home/renderer/src/osm2pgrouting/mapconfig.xml  --dbname gis --addnodes -h localhost -p 5432  -W tim -U postgres --clean
echo "1 of 8"
osmosis --read-pbf file=/data.osm.pbf --bounding-box  top=18.65 left=121.23266666666666 bottom=16.610999999999997 right=122.71533333333333 --write-pbf file=luzon_part.pbf
osmconvert  luzon_part.pbf --drop-author --drop-version --out-osm -o=load.osm
osm2pgrouting -f load.osm --conf /home/renderer/src/osm2pgrouting/mapconfig.xml  --dbname gis --addnodes -h localhost -p 5432  -W tim -U postgres
echo "2 of 8"
osmosis --read-pbf file=/data.osm.pbf --bounding-box  top=18.65 left=122.71533333333333 bottom=16.610999999999997 right=124.198 --write-pbf file=luzon_part.pbf
osmconvert  luzon_part.pbf --drop-author --drop-version --out-osm -o=load.osm
osm2pgrouting -f load.osm --conf /home/renderer/src/osm2pgrouting/mapconfig.xml  --dbname gis --addnodes -h localhost -p 5432  -W tim -U postgres
echo "3 of 8"
osmosis --read-pbf file=/data.osm.pbf --bounding-box  top=16.610999999999997 left=119.75 bottom=14.572 right=121.23266666666666 --write-pbf file=luzon_part.pbf
osmconvert  luzon_part.pbf --drop-author --drop-version --out-osm -o=load.osm
osm2pgrouting -f load.osm --conf /home/renderer/src/osm2pgrouting/mapconfig.xml  --dbname gis --addnodes -h localhost -p 5432  -W tim -U postgres
echo "4 of 8"
osmosis --read-pbf file=/data.osm.pbf --bounding-box  top=16.610999999999997 left=121.23266666666666 bottom=14.572 right=122.71533333333333 --write-pbf file=luzon_part.pbf
osmconvert  luzon_part.pbf --drop-author --drop-version --out-osm -o=load.osm
osm2pgrouting -f load.osm --conf /home/renderer/src/osm2pgrouting/mapconfig.xml  --dbname gis --addnodes -h localhost -p 5432  -W tim -U postgres
echo "5 of 8"
osmosis --read-pbf file=/data.osm.pbf --bounding-box  top=16.610999999999997 left=122.71533333333333 bottom=14.572 right=124.198 --write-pbf file=luzon_part.pbf
osmconvert  luzon_part.pbf --drop-author --drop-version --out-osm -o=load.osm
osm2pgrouting -f load.osm --conf /home/renderer/src/osm2pgrouting/mapconfig.xml  --dbname gis --addnodes -h localhost -p 5432  -W tim -U postgres
echo "6 of 8"
osmosis --read-pbf file=/data.osm.pbf --bounding-box  top=14.572 left=119.75 bottom=12.533 right=121.23266666666666 --write-pbf file=luzon_part.pbf
osmconvert  luzon_part.pbf --drop-author --drop-version --out-osm -o=load.osm
osm2pgrouting -f load.osm --conf /home/renderer/src/osm2pgrouting/mapconfig.xml  --dbname gis --addnodes -h localhost -p 5432  -W tim -U postgres
echo "7 of 8"
osmosis --read-pbf file=/data.osm.pbf --bounding-box  top=14.572 left=121.23266666666666 bottom=12.533 right=122.71533333333333 --write-pbf file=luzon_part.pbf
osmconvert  luzon_part.pbf --drop-author --drop-version --out-osm -o=load.osm
osm2pgrouting -f load.osm --conf /home/renderer/src/osm2pgrouting/mapconfig.xml  --dbname gis --addnodes -h localhost -p 5432  -W tim -U postgres
echo "8 of 8"
osmosis --read-pbf file=/data.osm.pbf --bounding-box  top=14.572 left=122.71533333333333 bottom=12.533 right=124.198 --write-pbf file=luzon_part.pbf
osmconvert  luzon_part.pbf --drop-author --drop-version --out-osm -o=load.osm
osm2pgrouting -f load.osm --conf /home/renderer/src/osm2pgrouting/mapconfig.xml  --dbname gis --addnodes -h localhost -p 5432  -W tim -U postgres
echo "9 of 8"
# TODO add Command line switch to do --clean on load
# TODO Get dimensions of the whole pbf file. Useful if you want to load the whole pbf file in pieces.

"""



top = 18.65
left = 119.75
bottom = 12.533
right = 124.198
parts = 3
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
        print("{} {}".format(route, "--clean" if (x == 0 and y == 0) else " "))
        print(f"echo \"{1+x * parts + y } of {parts * parts -1}\"")



