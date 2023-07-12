SELECT
    o.name AS table_name,
    c.name AS column_name,
    t.name AS data_type
FROM
    sysobjects o
JOIN
    syscolumns c ON o.id = c.id
JOIN
    systypes t ON c.usertype = t.usertype
WHERE
    o.type = 'U'  -- User-defined tables only
    AND t.name IN ('date', 'datetime', 'smalldatetime', 'varbinary')
