DELIMITER //

DROP PROCEDURE IF EXISTS readURLID;

CREATE PROCEDURE readURLID(IN short_in varchar(100))
BEGIN
    SELECT url_id FROM urls
    WHERE short = short_in;
END //

DELIMITER ;

