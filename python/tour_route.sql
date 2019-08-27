SELECT DISTINCT ON
    (LEAST(X.name || Y.name, Y.name || X.name))
    dense_rank()
        OVER(ORDER BY LEAST(X.name || Y.name, Y.name || X.name))::INTEGER AS id,
    X.name AS name_1,
    Y.name AS name_2,
    ST_MakeLine(X.geom, Y.geom)::GEOMETRY(LineString,4326) AS geom,
    ROUND(ST_Distance(X.geom::GEOGRAPHY, Y.geom::GEOGRAPHY)/1000) AS distance,
    X.id AS source,
    Y.id AS target
INTO
    tour_routes
FROM
    tour X CROSS JOIN tour Y
WHERE
    X.name <> Y.name;

-- select name_1,name_2, distance from tour_routes;