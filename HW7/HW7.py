
# Your name: Sarafina Chea
# Your student id: 80843471
# Your email: sarafina@umich.edu
# List who you have worked with on this project:

import unittest
import sqlite3
import json
import os

def read_data(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def make_positions_table(data, cur, conn):
    positions = []
    for player in data['squad']:
        position = player['position']
        if position not in positions:
            positions.append(position)
    cur.execute("CREATE TABLE IF NOT EXISTS Positions (id INTEGER PRIMARY KEY, position TEXT UNIQUE)")
    for i in range(len(positions)):
        cur.execute("INSERT OR IGNORE INTO Positions (id, position) VALUES (?,?)",(i, positions[i]))
    conn.commit()

def make_players_table(data, cur, conn):
    d_query = "drop table players"
    cur.execute(d_query)
    tab_query = """CREATE TABLE players(id int PRIMARY KEY,name text,position_id int, birthyear int, nationality text);"""

    cur.execute(tab_query)

    for player in data['squad']:
        id = player['id']
        name = player['name']
        position = player['position']
        birthyear = player['dateOfBirth']
        nationality = player['nationality']


        qury = f"select id from positions where position = '{position}'"
        cur.execute(qury)
        result = cur.fetchall()
        position_id = result[0][0]

        insert_qury = f"INSERT INTO players (id, name, position_id, birthyear, nationality) VALUES({id}, '{name}', {position_id}, {birthyear}, '{nationality}')"
        print(player)
        print(insert_qury)
        cur.execute(insert_qury)
    conn.commit()


def nationality_search(countries, cur, conn):
    listy = []
    for country in countries:
        select_q = f"select name, position_id, nationality, from players where nationality = '{country}'"
        cur.execute(select_q)
        result = cur.fetchall()
        for player in result:
            listy.append(player)
    return listy



def birthyear_nationality_search(age, country, cur, conn):
    curr_yr = 2023
    yr_cutoff = curr_yr - age
    select_q = f"SELECT name, nationality, birthyear FROM players WHERE nationality = '{country}' AND birthyear < {yr_cutoff}"
    cur.execute(select_q)
    result = cur.fetchall()
    return result

def position_birth_search(position, age, cur, conn):
       new_tup = []
       birth_year = 2023 - age
       select_q = f"SELECT players.name, positions.position, players.birthyear FROM players JOIN position ON players.position_id = positions.id WHERE positions.position = '{position}' AND players.birthyear > '{birth_year}'"
       cur.execute(select_q)
       result = cur.fetchall()
       for player in result:
           new_tup.append(player)
       return result

def make_winners_table(data, cur, conn):
    pass

def make_seasons_table(data, cur, conn):
    pass

def winners_since_search(year, cur, conn):
    pass


class TestAllMethods(unittest.TestCase):
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(path+'/'+'Football.db')
        self.cur = self.conn.cursor()
        self.conn2 = sqlite3.connect(path+'/'+'Football_seasons.db')
        self.cur2 = self.conn2.cursor()

    def test_players_table(self):
        self.cur.execute('SELECT * from Players')
        players_list = self.cur.fetchall()

        self.assertEqual(len(players_list), 30)
        self.assertEqual(len(players_list[0]),5)
        self.assertIs(type(players_list[0][0]), int)
        self.assertIs(type(players_list[0][1]), str)
        self.assertIs(type(players_list[0][2]), int)
        self.assertIs(type(players_list[0][3]), int)
        self.assertIs(type(players_list[0][4]), str)

    def test_nationality_search(self):
        x = sorted(nationality_search(['England'], self.cur, self.conn))
        self.assertEqual(len(x), 11)
        self.assertEqual(len(x[0]), 3)
        self.assertEqual(x[0][0], "Aaron Wan-Bissaka")

        y = sorted(nationality_search(['Brazil'], self.cur, self.conn))
        self.assertEqual(len(y), 3)
        self.assertEqual(y[2],('Fred', 2, 'Brazil'))
        self.assertEqual(y[0][1], 3)

    def test_birthyear_nationality_search(self):

        a = birthyear_nationality_search(24, 'England', self.cur, self.conn)
        self.assertEqual(len(a), 11)
        self.assertEqual(a[0][1], 'England')
        self.assertEqual(a[3][2], 1992)
        self.assertEqual(len(a[1]), 3)

    def test_type_speed_defense_search(self):
        b = sorted(position_birth_search('Goalkeeper', 35, self.cur, self.conn))
        self.assertEqual(len(b), 2)
        self.assertEqual(type(b[0][0]), str)
        self.assertEqual(type(b[1][1]), str)
        self.assertEqual(len(b[1]), 3) 
        self.assertEqual(b[1], ('Jack Butland', 'Goalkeeper', 1993)) 

        c = sorted(position_birth_search("Defence", 23, self.cur, self.conn))
        self.assertEqual(len(c), 1)
        self.assertEqual(c, [('Teden Mengi', 'Defence', 2002)])
    
    # test extra credit
    def test_make_winners_table(self):
        self.cur2.execute('SELECT * from Winners')
        winners_list = self.cur2.fetchall()

        pass

    def test_make_seasons_table(self):
        self.cur2.execute('SELECT * from Seasons')
        seasons_list = self.cur2.fetchall()

        pass

    def test_winners_since_search(self):

        pass


def main():

    #### FEEL FREE TO USE THIS SPACE TO TEST OUT YOUR FUNCTIONS

    json_data = read_data('football.json')
    cur, conn = open_database('Football.db')
    make_positions_table(json_data, cur, conn)
    make_players_table(json_data, cur, conn)
    conn.close()


    seasons_json_data = read_data('football_PL.json')
    cur2, conn2 = open_database('Football_seasons.db')
    make_winners_table(seasons_json_data, cur2, conn2)
    make_seasons_table(seasons_json_data, cur2, conn2)
    conn2.close()


if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)
