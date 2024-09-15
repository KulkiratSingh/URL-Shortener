DELIMITER //

DROP PROCEDURE IF EXISTS readUser;

CREATE PROCEDURE readUser(IN user varchar(255))
BEGIN
    SELECT * FROM users
    WHERE name = user;	
END //

DELIMITER ;

