from py2neo import Graph, Node, Relationship
from datetime import datetime
import os, json
import uuid

url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username = 'neo4j'
password = 'neo4jpiyush'

graph = Graph(url + '/db/data/', username=username, password=password)

def main():
    path_to_json = 'workshop_dataset/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    
    index = 0
    filec = 1
    flag = 0;

    # tx = graph.begin()
    # tx.run("CREATE CONSTRAINT ON (a:Author) ASSERT a.author_screen_name IS UNIQUE;")
    # tx.run("CREATE CONSTRAINT ON (t:Tweet) ASSERT t.tid IS UNIQUE;")
    # tx.run("CREATE CONSTRAINT ON (l:Location) ASSERT l.value IS UNIQUE;")
    # tx.run("CREATE CONSTRAINT ON (h:Hashtag) ASSERT h.value IS UNIQUE;")
    # tx.run("CREATE CONSTRAINT ON (k:Keyword) ASSERT k.value IS UNIQUE;")
    # tx.commit()
    
    tx = graph.begin()
    tx.run("CREATE (a:Author{author_id:'dummy',author_screen_name:'dummy'})")
    tx.run("CREATE (t:Tweet{tid:'dummy',tweet_text:'dummy',lang:'dummy',type:'dummy'})")
    tx.run("CREATE (l:Location{value:'dummy'})")
    tx.run("CREATE (h:Hashtag{value:'dummy'})")
    tx.run("CREATE (r:Keyword{value:'dummy'})")
    tx.commit()

    tx = graph.begin()
    tx.run("CREATE INDEX ON :Author(author_screen_name)")
    tx.run("CREATE INDEX ON :Tweet(tid)")
    tx.run("CREATE INDEX ON :Location(value)")
    tx.run("CREATE INDEX ON :Hashtag(value)")
    tx.run("CREATE INDEX ON :Keyword(value)")
    tx.commit()


    for js in json_files:
        print (filec ," " , js)
        with open(os.path.join(path_to_json, js)) as json_file:
            json_text = json.load(json_file)
            tx = graph.begin()
            for id in json_text:
                tid = json_text[id]['tid']
                # quote_count = json_text[id]['quote_count']           
                # reply_count = json_text[id]['reply_count']           
                hashtags = json_text[id]['hashtags']    
                # datetime = json_text[id]['datetime']
                # date = json_text[id]['date']
                # like_count = json_text[id]['like_count']
                # verified = json_text[id]['verified']
                # sentiment = json_text[id]['sentiment']
                author = json_text[id]['author']
                location = json_text[id]['location']
                # retweet_count = json_text[id]['retweet_count']
                type = json_text[id]['type']
                # media_list = json_text[id]['media_list']
                # quoted_source_id = json_text[id]['quoted_source_id']
                # url_list = json_text[id]['url_list']
                tweet_text = json_text[id]['tweet_text']
                author_profile_image = json_text[id]['author_profile_image']
                author_screen_name = json_text[id]['author_screen_name']
                author_id = json_text[id]['author_id']
                lang = json_text[id]['lang']
                keywords_processed_list = json_text[id]['keywords_processed_list']        
                retweet_source_id = json_text[id]['retweet_source_id']
                mentions = json_text[id]['mentions']
                replyto_source_id = json_text[id]['replyto_source_id']

                # print("A ",index)
                tx.run("MERGE (a:Author{author_id:{author_id},author_screen_name:{author_screen_name}})", author_id=author_id, author_screen_name=author_screen_name)

                # print("B ",index)
                tx.run("MERGE (t:Tweet{tid:{tid},tweet_text:{tweet_text},lang:{lang},type:{type}})",tid=tid,tweet_text=tweet_text,lang=lang,type=type)
                rel = """
                MATCH (t:Tweet),(a:Author)
                WHERE t.tid={tid} AND a.author_screen_name={author_screen_name}
                CREATE (a)-[:TWEETED]->



                (t)
                """
                tx.run(rel,tid=tid,author_screen_name=author_screen_name)

                # print("C ",index)
                if location is not None:
                    tx.run("MERGE (l:Location{value:{location}})",location=location)
                    # graph.merge(location)
                    rel = """
                    MATCH (t:Tweet),(l:Location)
                    WHERE t.tid={tid} AND l.value={location}
                    CREATE (t)-[:TWEETED_FROM]->(l)
                    """
                    tx.run(rel,tid=tid,location=location)

                # print("D ",index)
                if hashtags is not None:
                    for hashtag in hashtags:
                        if hashtag is not None:
                            tx.run("MERGE (h:Hashtag{value:{hashtag}})",hashtag=hashtag)
                            rel = """
                            MATCH (t:Tweet),(h:Hashtag)
                            WHERE t.tid={tid} AND h.value={hashtag}
                            CREATE (t)-[:CONTAINS_HASHTAG]->(h)
                            """
                            tx.run(rel,tid=tid,hashtag=hashtag)

                # print("E ",index)
                if retweet_source_id is not None:
                    query = """
                    MATCH (t:tweet)
                    WHERE t.tid={tid}
                    RETURN t
                    """
                    val = None
                    val = tx.evaluate(query,tid=retweet_source_id)
                    # print (val, val is None)
                    if val is None:
                        tx.run("CREATE (t:Tweet{tid:{tid}})",tid=retweet_source_id)
                    rel = """
                    MATCH (t1:Tweet),(t2:Tweet)
                    WHERE t1.tid={tid} AND t2.tid={retweet_source_id}
                    CREATE (t1)-[:RETWEET_OF]->(t2)
                    """
                    tx.run(rel,tid=tid,retweet_source_id=retweet_source_id)

                # print("F ",index)
                if mentions is not None:
                    for mention in mentions:
                        if mention is not None:
                            query = """
                            MATCH (a:Author)
                            WHERE a.author_screen_name={mention}
                            RETURN a
                            """
                            val = None
                            val = tx.evaluate(query,mention=mention)
                            # print (val, val is None)
                            if val is None:
                                tx.run("CREATE (a:Author{author_screen_name:{mention}})",mention=mention)
                            rel = """
                            MATCH (t:Tweet),(a:Author)
                            WHERE t.tid={tid} AND a.author_screen_name={mention}
                            CREATE (t)-[:MENTIONS]->(a)
                            """
                            tx.run(rel,tid=tid,mention=mention)

                # print("G ",index)
                if replyto_source_id is not None:
                    query = """
                    MATCH (t:tweet)
                    WHERE t.tid={tid}
                    RETURN t
                    """
                    val = None
                    val = tx.evaluate(query,tid=replyto_source_id)
                    # print (val, val is None)
                    if val is None:
                        tx.run("CREATE (t:Tweet{tid:{tid}})",tid=replyto_source_id)
                    rel = """
                    MATCH (t1:Tweet),(t2:Tweet)
                    WHERE t1.tid={tid} AND t2.tid={replyto_source_id}
                    CREATE (t1)-[:REPLY_OF]->(t2)
                    """
                    tx.run(rel,tid=tid,replyto_source_id=replyto_source_id)

                # print("H ",index)
                if keywords_processed_list is not None:
                    for keyword in keywords_processed_list:
                        if keyword is not None:
                            tx.run("MERGE (k:Keyword{value:{keyword}})",keyword=keyword)
                            rel = """
                            MATCH (t:Tweet),(k:keyword)
                            WHERE t.tid={tid} AND k.value={keyword}
                            CREATE (t)-[:CONTAINS_KEYWORD]->(h)
                            """
                            tx.run(rel,tid=tid,keyword=keyword)
                index += 1
            tx.commit()
        filec = filec+1
        # break

if __name__ == "__main__":
    main()
