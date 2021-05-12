
CREATE DATABASE userData;
use userData;

CREATE TABLE IF NOT EXISTS userTable(
    `id` int AUTO_INCREMENT,
    `username` VARCHAR(100) CHARACTER SET utf8,
    `password` VARCHAR(100) CHARACTER SET utf8,
    `firstname` VARCHAR(100) CHARACTER SET utf8,
    `lastname` VARCHAR(100) CHARACTER SET utf8,
    `isactivate` BOOLEAN,

    PRIMARY KEY (`id`)
);

INSERT INTO userTable (username,password,firstname,lastname,school,department,year,isactivate) VALUES
    ('ks664@njit.edu','1234', 'Kefin', 'Sajan',TRUE),
    ('ab344@njit.edu','0000', 'Adrianna', 'Brzezinska',TRUE);
