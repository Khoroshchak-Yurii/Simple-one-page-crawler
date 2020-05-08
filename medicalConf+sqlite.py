from bs4 import BeautifulSoup
import requests
import sqlite3

conn = sqlite3.connect('ldb.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Artist;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title    TEXT UNIQUE,
    city    TEXT UNIQUE,
    time    TEXT UNIQUE,
    link    TEXT UNIQUE
)
''')

source = requests.get('https://www.omicsonline.org/medical-conferences.php').text
soup = BeautifulSoup(source, 'lxml')



for li in soup.find_all('li'):
    title = li.a.text
    city = li.small.em.text
    time = li.time.text
    lnk = li.a['href']

    cur.execute('''INSERT OR IGNORE INTO Artist (title, city, time, link)
        VALUES ( ?,?,?,? )''', ( title, city, time, lnk ) )


    conn.commit()
