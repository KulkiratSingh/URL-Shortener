DELIMITER //

DROP PROCEDURE IF EXISTS getUserURLs;

CREATE PROCEDURE getUserURLs(IN user_id_in int)
BEGIN
    SELECT * FROM urls
    WHERE user_id = user_id_in;	
END //

DELIMITER ;

