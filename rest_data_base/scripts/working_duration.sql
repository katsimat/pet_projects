-- 1
SELECT 
    name AS restaurant_name,
    open_time,
    close_time,
    close_time - open_time AS working_duration
FROM 
    db_rest.restaurant;