from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra.policies import DCAwareRoundRobinPolicy

import os, json
import pandas as pd
from datetime import datetime as dt, timedelta

KEYSPACE = "twitterkeyspace"

def main():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.default_timeout = 60
    rows = session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
    if KEYSPACE in [row[0] for row in rows]:
        # Dropping Existing Keyspace
        session.execute("DROP KEYSPACE " + KEYSPACE)

    # Creating Keyspace
    session.execute("""
        CREATE KEYSPACE %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % KEYSPACE)

    # Settinig Keyspace
    session.set_keyspace(KEYSPACE)
 

    # Creating tables
    session.execute("""
        CREATE TABLE tweet_table1 (
            tid text,
            author_id text,
            date date,
            PRIMARY KEY (date, tid)
        ) WITH CLUSTERING ORDER BY (tid DESC)
        """)

    session.execute("""
        CREATE TABLE tweet_table2 (
            tid text,
            hashtag text,
            location text,
            date date,
            PRIMARY KEY (date, tid)
        ) WITH CLUSTERING ORDER BY (tid DESC)
        """)
    
    # Finding list of json files
    path_to_json = 'workshop_dataset/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

    index = 0
    filec = 1
    for js in json_files:
        print (filec ," " , js)
        with open(os.path.join(path_to_json, js)) as json_file:
            json_text = json.load(json_file)
            for id in json_text:
                tid = json_text[id]['tid']
                hashtags = json_text[id]['hashtags']    
                date = json_text[id]['date']
                location = json_text[id]['location']
                author_id = json_text[id]['author_id']

                # Query 1 (Ques 4)
                session.execute(
                """
                INSERT INTO tweet_table1 (tid, author_id, date)
                VALUES (%s, %s, %s)
                """,
                (tid,author_id,date)
                )
                # Query 1 (Ques 10)
                if hashtags :
                    for hashtag in hashtags:
                        if hashtag :
                            session.execute(
                            """
                            INSERT INTO tweet_table2 (tid, hashtag, location, date)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (tid, hashtag, location, date)
                            )
                index += 1
        filec = filec+1
    

if __name__ == "__main__":
    main()