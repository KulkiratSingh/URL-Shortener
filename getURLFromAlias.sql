DELIMITER //

DROP PROCEDURE IF EXISTS getURLFromAlias;

CREATE PROCEDURE getURLFromAlias(IN alias_in varchar(100))
BEGIN
    SELECT * FROM urls
    WHERE alias = alias_in;
END //

DELIMITER ;