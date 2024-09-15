DELIMITER //

DROP PROCEDURE IF EXISTS insertURLIntoDB;

CREATE PROCEDURE insertURLIntoDB(IN url_in VARCHAR(1024), IN alias_in VARCHAR(100), IN user_id_in INT)
BEGIN
    INSERT INTO urls (url, alias, user_id)
    VALUES (url_in, alias_in, user_id_in);
END //

DELIMITER ;