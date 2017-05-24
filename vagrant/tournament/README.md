## Project Specification

Develop a database schema to store details of matches between players.
Then write a Python module to rank the players and pair them up in matches in a tournament.

## Files

**tournament.py**

Contains the implementation for the Swiss tournament

**tournament.sql**

Contains the SQL queries to create the database, tables and views

**tournament_test.py**

Contains the test cases for tournament.py

## Prerequisites

The latest vagrant build for the Udacity tournament project.

## Instructions

1. Start Vagrant
  - Open Terminal or cmd and browse to the vagrant folder
  - Type 'vagrant up'
2. SSH in to the vagrant VM
  - In the same terminal type 'vagrant ssh'
3. Change to the correct folder
  - Type 'cd /vagrant/tournament'
4. Open PSQL and run the tournament.sql 
  - Type command 'psql'
  - Then type '\i tournament.sql'
  - Press Ctrl+D to close psql 
5. Run the tests
  - In the terminal type `python tournament_test.py`

## Expected Outcome

```
$ python tournament_test.py
1. countPlayers() returns 0 after initial deletePlayers() execution.
2. countPlayers() returns 1 after one player is registered.
3. countPlayers() returns 2 after two players are registered.
4. countPlayers() returns zero after registered players are deleted.
5. Player records successfully deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After match deletion, player standings are properly reset.
9. Matches are properly deleted.
10. After one match, players with one win are properly paired.
Success!  All tests pass!
```