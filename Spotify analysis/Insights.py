import json
import sqlite3 as sql
import pandas as pd


con = sql.connect('data.db')
cur = con.cursor()

cur.executescript(''' Drop table if exists Data;
            
            Create Table Data(
                Songtitle text,
                Artist  text,
                Date text,
                msplayed integer
                );
            
            ''')

streamhist0 = open("StreamingHistory0.json", encoding = "utf-8")
streamhist1 = open("StreamingHistory1.json", encoding = "utf-8")

js = [json.load(streamhist0),json.load(streamhist1)]

for data in js:
    for item in data:
        Date = item['endTime']
        Artist = item['artistName']
        Songtitle = item['trackName']
        msplayed = item['msPlayed']
        cur.execute('''
                     Insert into Data (Songtitle,Artist,Date,msplayed)
                     values(?,?,?,?)
                     ''' , (Songtitle,Artist, Date, msplayed))
    con.commit()
 
string = '''
SELECT  Songtitle,count(*) as Repeatplays
FROM Data
GROUP by Songtitle
ORDER by count(*) DESC
LIMIT 5'''
top10 = pd.read_sql(string, con, 'Songtitle')

print(top10.plot.pie(y= 'Repeatplays' ))
    
sqlstr = '''Select Day, playedthatday/averageplaytime as normal
From (SELECT substr(Date,0,11) As Day, sum(msplayed) AS playedthatday
FROM Data
Group by Day) join( SELECT avg(msplayed) as averageplaytime
From Data);'''

playtime = pd.read_sql(sqlstr, con, 'Day')
print(playtime.plot.bar(figsize=(60,20)))
