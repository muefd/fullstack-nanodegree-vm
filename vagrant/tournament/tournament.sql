-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Drop existing database
drop database if exists tournament;

-- Create a database
create database tournament;

-- Connect to the database
\c tournament

-- Create table to store players data
create table players (
    id serial primary key, 
    name text
);

-- Create table to store mathes data
create table matches ( 
    matchid serial primary key, 
    winner integer references players(id) on delete cascade, 
    loser integer references players(id) on delete cascade
);

-- Create view to simplify 'playerStandings' function
create view v_playerStandings as
select p.id, p.name, (select count(m.winner)
                      from matches as m
                      where m.winner = p.id) as wins,
                      (select count(m.matchid)
                      from matches as m
                      where m.winner = p.id or m.loser = p.id) as matches
from players as p
order by wins;