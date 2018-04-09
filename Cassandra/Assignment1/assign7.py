# import logging

# log = logging.getLogger()
# log.setLevel('DEBUG')
# handler = logging.StreamHandler()
# handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
# log.addHandler(handler)

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
        # log.info("dropping existing keyspace...")
        session.execute("DROP KEYSPACE " + KEYSPACE)

    # log.info("creating keyspace...")
    session.execute("""
        CREATE KEYSPACE %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % KEYSPACE)

    # log.info("setting keyspace...")
    session.set_keyspace(KEYSPACE)
 
    # this finds our json files
    path_to_json = 'workshop_dataset/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

    # log.info("creating tables...")
    session.execute("""
        CREATE TABLE tweet_table1 (
            tid text,
            author_screen_name text,
            datetime timestamp,
            location text,
            tweet_text text,
            author_id text,
            lang text,
            PRIMARY KEY (author_screen_name, datetime)
        ) WITH CLUSTERING ORDER BY (datetime DESC)
        """)

    session.execute("""
        CREATE TABLE tweet_table2 (
            tid text,
            location text,
            tweet_text text,
            author_id text,
            lang text,
            like_count bigint,
            keyword text,
            PRIMARY KEY (keyword, like_count, tid)
        ) WITH CLUSTERING ORDER BY (like_count DESC, tid DESC)
        """)
    
    session.execute("""
        CREATE TABLE tweet_table3 (
            tid text,
            location text,
            tweet_text text,
            author_id text,
            lang text,
            datetime timestamp,
            hashtag text,
            PRIMARY KEY (hashtag,datetime, tid)
        ) WITH CLUSTERING ORDER BY (datetime DESC, tid DESC)
        """)
    
    session.execute("""
        CREATE TABLE tweet_table4 (
            tid text,
            location text,
            tweet_text text,
            author_id text,
            lang text,
            datetime timestamp,
            mention text,
            PRIMARY KEY (mention, datetime, tid)
        ) WITH CLUSTERING ORDER BY (datetime DESC, tid DESC)
        """)

    session.execute("""
        CREATE TABLE tweet_table5 (
            tid text,
            location text,
            tweet_text text,
            author_id text,
            lang text,
            date date,
            like_count bigint,
            PRIMARY KEY (date, like_count, tid)
        ) WITH CLUSTERING ORDER BY (like_count DESC, tid DESC)
        """)

    session.execute("""
        CREATE TABLE tweet_table6 (
            tid text,
            location text,
            tweet_text text,
            author_id text,
            lang text,
            PRIMARY KEY (location, tid)
        ) WITH CLUSTERING ORDER BY (tid DESC)
        """)
    
    session.execute("""
        CREATE TABLE tweet_table7 (
            tid text,
            hashtags list<text>,
            date date,
            PRIMARY KEY (date,tid)
        )
        """)

    

    index = 0
    filec = 1
    for js in json_files:
        print (filec ," " , js)
        with open(os.path.join(path_to_json, js)) as json_file:
            json_text = json.load(json_file)
            for id in json_text:
                tid = json_text[id]['tid']
                hashtags = json_text[id]['hashtags']    
                datetime = json_text[id]['datetime']
                date = json_text[id]['date']
                like_count = json_text[id]['like_count']
                author = json_text[id]['author']
                location = json_text[id]['location']
                tweet_text = json_text[id]['tweet_text']
                author_screen_name = json_text[id]['author_screen_name']
                author_id = json_text[id]['author_id']
                lang = json_text[id]['lang']
                keywords_processed_list = json_text[id]['keywords_processed_list']        
                mentions = json_text[id]['mentions']
                # quote_count = json_text[id]['quote_count']           
                # reply_count = json_text[id]['reply_count']           
                # verified = json_text[id]['verified']
                # sentiment = json_text[id]['sentiment']
                # retweet_count = json_text[id]['retweet_count']
                # type = json_text[id]['type']
                # media_list = json_text[id]['media_list']
                # quoted_source_id = json_text[id]['quoted_source_id']
                # url_list = json_text[id]['url_list']
                # author_profile_image = json_text[id]['author_profile_image']
                # retweet_source_id = json_text[id]['retweet_source_id']
                # replyto_source_id = json_text[id]['replyto_source_id']
                if location is None:
                    location = 'null' 
                # Query 1
                session.execute(
                """
                INSERT INTO tweet_table1 (tid, author_screen_name, datetime, location, tweet_text, author_id, lang)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (tid,author_screen_name,datetime,location,tweet_text, author_id, lang)
                )
                # Query 2
                if keywords_processed_list :
                    for keyword in keywords_processed_list:
                        if keyword :
                            session.execute(
                            """
                            INSERT INTO tweet_table2 (tid, location, tweet_text, author_id, lang, like_count, keyword)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """,
                            (tid,location,tweet_text, author_id, lang, like_count, keyword)
                            )
                # # Query 3
                if hashtags :
                    for hashtag in hashtags:
                        if hashtag :
                            session.execute(
                            """
                            INSERT INTO tweet_table3 (tid, location, tweet_text, author_id, lang, datetime, hashtag)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """,
                            (tid,location,tweet_text, author_id, lang, datetime, hashtag)
                            )
                # Query 4
                if mentions :
                    for mention in mentions:
                        if mention :
                            session.execute(
                            """
                            INSERT INTO tweet_table4 (tid, location, tweet_text, author_id, lang, datetime, mention)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """,
                            (tid,location,tweet_text, author_id, lang, datetime, mention)
                            )
                # Query 5
                session.execute(
                """
                INSERT INTO tweet_table5 (tid, location, tweet_text, author_id, lang, date, like_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (tid,location,tweet_text, author_id, lang, date, like_count)
                )
                # Query 6
                session.execute(
                """
                INSERT INTO tweet_table6 (tid, location, tweet_text, author_id, lang)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (tid,location,tweet_text, author_id, lang)
                )
                # Query 7
                for i in range(7):
                    session.execute(
                    """
                    INSERT INTO tweet_table7 (tid, hashtags, date)
                    VALUES (%s, %s, %s)
                    """,
                    (tid,hashtags,date)
                    )
                    date = str(dt.strptime(date, "%Y-%m-%d").date()+timedelta(days=1))
                index += 1
        filec = filec+1
        # if filec >= 5:
        #     break
    print ("index :", index)

if __name__ == "__main__":
	main()