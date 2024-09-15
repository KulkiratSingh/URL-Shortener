DELIMITER //

DROP PROCEDURE IF EXISTS updateShort;

CREATE PROCEDURE updateShort(IN url_id_in INT, In user_id_in INT, IN new_alias varchar(100))
BEGIN
    UPDATE urls
    SET alias = new_alias
    WHERE url_id = url_id_in AND user_id = user_id_in;
END //

DELIMITER ;