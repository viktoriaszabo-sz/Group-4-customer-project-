-- u have to run this command in powershell: 
-- docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=password -e MYSQL-ROOT-HOST='%' -p 3306:3306 -d mysql:latest
-- this should create a container in docker, that should be running, when testing the backend of our code 
-- the container will be called "mysql-container" on port 3306:3306

create database learnwelltrial;
use learnwelltrial;

--creating the table that the original survey also has in sql

CREATE TABLE LearnWell(
    scope VARCHAR(255) DEFAULT 'PeerGroup4',
    semester VARCHAR(255) DEFAULT '2023 Autumn',

    -- Learning Process
    LP101 INT, LP102 INT, LP103 INT, LP104 INT, LP105 INT, LP106 INT,
    LP107 INT, LP108 INT, LP109 INT, LP110 INT, LP11 INT, LP12 INT,
    -- Learning Events
    LE101 INT, LE102 INT, LE103 INT, LE104 INT, LE105 INT, LE106 INT,
    LE107 INT, LE108 INT, LE109 INT, LE110 INT, LE111 INT, LE112 INT,
    LE113 INT, LE114 INT, LE115 INT, LE116 INT, LE201 INT, LE202 INT,
    LE203 INT, LE204 INT, LE205 INT, LE206 INT, LE207 INT, LE208 INT,
    LE209 INT, LE210 INT, LE211 INT, LE301 INT, LE302 INT, LE303 INT,
    LE304 INT, LE305 INT, LE306 INT,
    -- Performance Ratings
    PR101 INT, PR102 INT, PR103 INT,
    -- Course Details
    CD101 INT, CD102 INT, CD103 INT, CD104 INT, CD105 INT, CD106 INT,
    CD107 INT, CD108 INT, CD201 INT, CD202 INT, CD203 INT, CD204 INT,
    CD205 INT, CD206 INT, CD207 INT,
    -- Curriculum Progress
    CP101 INT, CP102 INT, CP103 INT, CP104 INT,
    -- Entrepreneurship
    EN101 INT,
    -- Social Development
    SD101 INT, SD102 INT,
    -- Community Outreach
    CO101 INT, CO102 INT,
    -- Data Science
    DS101 INT, DS102 INT, DS103 INT,
    -- Internationality
    IN101 INT, IN102 INT,
    -- Well-being
    WB101 INT, WB102 INT, WB103 INT, WB104 INT, WB105 INT, WB106 INT,
    WB107 INT, WB108 INT, WB109 INT, WB201 INT, WB202 INT, WB203 INT,
    WB204 INT, WB205 INT, WB206 INT, WB207 INT, WB301 INT, WB302 INT,
    WB303 INT, WB304 INT, WB305 INT, WB401 INT, WB402 INT, WB403 INT,
    WB404 INT, WB405 INT, WB406 INT
);

INSERT INTO LearnWell (LP101, LP102, LP103, LP104, LP105, LP106, LP107, LP108, LP109, LP110, LP11, LP12, LE101, LE102, LE103, LE104, LE105, LE106, LE107, LE108, LE109, LE110, LE111, LE112, LE113, LE114, LE115, LE116, LE201, LE202, LE203, LE204, LE205, LE206, LE207, LE208, LE209, LE210, LE211, LE301, LE302, LE303, LE304, LE305, LE306, PR101, PR102, PR103, CD101, CD102, CD103, CD104, CD105, CD106, CD107, CD108, CD201, CD202, CD203, CD204, CD205, CD206, CD207, CP101, CP102, CP103, CP104, EN101, SD101, SD102, CO101, CO102, DS101, DS102, DS103, IN101, IN102, WB101, WB102, WB103, WB104, WB105, WB106, WB107, WB108, WB109, WB201, WB202, WB203, WB204, WB205, WB206, WB207, WB301, WB302, WB303, WB304, WB305, WB401, WB402, WB403, WB404, WB405, WB406)
VALUES (3, 1, 3, 1, 1, 4, 2, 5, 5, 5, 5, 3, 5, 5, 3, 1, 2, 3, 2, 2, 4, 4, 4, 4, 3, 3, 3, 5, 1, 1, 2, 5, 3, 2, 4, 2, 5, 3, 5, 3, 5, 5, 5, 3, 1, 4, 4, 2, 1, 5, 5, 1, 1, 2, 5, 1, 4, 3, 2, 1, 3, 5, 5, 1, 1, 4, 2, 4, 5, 2, 2, 4, 2, 4, 1, 2, 1, 3, 4, 2, 4, 2, 5, 1, 4, 5, 3, 2, 4, 4, 1, 5, 5, 3, 2, 3, 3, 4, 4, 2, 4, 3, 4, 3);

create table sums (
    sumofgood INT,
    sumofbad INT
);

--extra table to create the 2 sum columns 
--this is gonna be the base for the personal feedback 






