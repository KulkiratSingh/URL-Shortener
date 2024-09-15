DELIMITER //

DROP PROCEDURE IF EXISTS incrementCounter;

CREATE PROCEDURE incrementCounter(IN url_id_in INT)
BEGIN
    UPDATE urls
    SET visit_counter = visit_counter + 1
    WHERE url_id = url_id_in;
END //

DELIMITER ;