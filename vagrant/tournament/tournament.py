#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns database connection and cursor."""

    db = psycopg2.connect("dbname=tournament")
    cursor = db.cursor()
    return db, cursor


def deleteMatches():
    """Remove all the match records from the database."""

    db, cursor = connect()
    cursor.execute("delete from matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    cursor.execute("delete from players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered for a tournament.
    """
    db, cursor = connect()
    cursor.execute("select count(*) from players")
    players = cursor.fetchone()[0]
    db.close()
    return players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    db, cursor = connect()
    cursor.execute("insert into players (name) values (%s)", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    db, cursor = connect()
    cursor.execute("select * from v_playerstandings")
    ranks = cursor.fetchall()
    db.close()
    return ranks


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    w_points = 1
    l_points = 0
    db, cursor = connect()
    cursor.execute("insert into matches (winner, loser) values (%s, %s)", (winner, loser,))
    db.commit()
    db.close()


def validPair(player1, player2):
    """Checks if two players have already played against each other
    Args:
        player1: the id number of first player to check
        player2: the id number of potentail paired player
    Return true if valid pair, false if not
    """

    db, cursor = connect()
    cursor.execute("""select count(*)
                    from matches
                    where (winner = %(p1)s and loser = %(p2)s)
                    or (winner = %(p2)s and loser = %(p1)s)""",
                    {'p1': player1, 'p2': player2})
    matches = cursor.fetchone()[0]
    db.close()

    if matches > 0:
        return False
    return True


def checkPairs(ranks, id1, id2):
    """Checks if two players have already had a match against each other.

    Args:
        ranks: list of current ranks from swissPairings()
        id1: player needing a match
        id2: potential matched player
    Returns id of matched player or original match if none are found.
    """
    if id2 >= len(ranks):
        return id1 + 1
    elif validPair(ranks[id1][0], ranks[id2][0]):
        return id2
    else:
        return checkPairs(ranks, id1, (id2 + 1))


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    ranks = playerStandings()
    pairs = []

    while len(ranks) > 1:
        validMatch = checkPairs(ranks, 0, 1)
        player1 = ranks.pop(0)
        player2 = ranks.pop(validMatch - 1)
        pairs.append((player1[0], player1[1], player2[0], player2[1]))

    return pairs