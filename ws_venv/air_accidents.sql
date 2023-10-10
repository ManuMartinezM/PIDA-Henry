CREATE DATABASE air_accidents;

USE air_accidents;

SHOW VARIABLES LIKE "secure_file_priv";

CREATE TABLE air_accidents(
    Date DATE,
    DeclaredTime TIME,
    Location VARCHAR(255),
    Operator VARCHAR(255),
    Route VARCHAR(255),
    Aircraft VARCHAR(255),
    TotalOnBoard INT,
    PassengersAboard INT,
    CrewAboard INT,
    Fatalities INT,
    PassengerFatalities INT,
    CrewFatalities INT,
    Ground INT,
    Summary TEXT,
    TotalFatalities INT,
    Survived INT,
    SurvivalRate DECIMAL(5, 2),
    IsMilitary VARCHAR(5),
    LocationCountry VARCHAR(255),
    CrewSurvivors INT,
    CrewSurvivalRate DECIMAL(5, 2) NULL,
    `2002-2011` VARCHAR(5),
    `2012-2021` VARCHAR(5)
)CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

DROP TABLE air_accidents;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Air_Accidents.csv'
INTO TABLE air_accidents
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SHOW VARIABLES LIKE 'character_set_server';

SELECT * FROM air_accidents;
