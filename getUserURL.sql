DELIMITER //

DROP PROCEDURE IF EXISTS getUserURL;

CREATE PROCEDURE getUserURL(IN url_id_in int, IN user_id_in INT)
BEGIN
    SELECT * FROM urls
    WHERE url_id = url_id_in AND user_id = user_id_in;
END //

DELIMITER ;