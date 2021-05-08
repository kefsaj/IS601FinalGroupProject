CREATE DATABASE userData;
use userData;

CREATE TABLE IF NOT EXISTS userTable(
    `id` int AUTO_INCREMENT,
    `username` VARCHAR(100) CHARACTER SET utf8,
    `password` VARCHAR(100) CHARACTER SET utf8,
    `email` VARCHAR(100) CHARACTER SET utf8,
    `isemailed` BOOLEAN,
    PRIMARY KEY (`id`)
);

INSERT INTO userTable (username,password,email,lastname,isemailed) VALUES
    ('ks664@gmail.com','123456', 'kef', 'saj', '1',TRUE),
    ('ksajan16@gmail.com','123456', 'kefin', 'sajan', '1',TRUE);

