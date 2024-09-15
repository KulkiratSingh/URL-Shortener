DELIMITER //

DROP PROCEDURE IF EXISTS deleteURL;

CREATE PROCEDURE deleteURL(IN link_id INT, IN user_id_parm INT)
BEGIN
    DELETE FROM urls
    WHERE url_id = link_id AND user_id = user_id_parm;
END //

DELIMITER ;