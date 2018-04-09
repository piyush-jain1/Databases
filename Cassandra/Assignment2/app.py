from flask import Flask,request,render_template,redirect, url_for
from flask import jsonify
import requests
from cassandra.cluster import Cluster
from collections import OrderedDict

app = Flask(__name__)

KEYSPACE = "twitterkeyspace"

@app.route('/', methods=['GET'])
def home():
	if request.method == 'GET':
		return render_template('lab.html',flag=0)

# Lab Query 1
@app.route('/labquery1', methods=['GET','POST'])
def labquery1():
	if request.method == 'GET':
		return render_template('lab.html',flag=0)
	elif request.method == 'POST':
		date = request.form['date1']
		# print (date)

		# Connecting cassandra session
		cluster = Cluster(['127.0.0.1'])
		session = cluster.connect()
		session.default_timeout = 60
		session.set_keyspace(KEYSPACE)

		query = "SELECT author_id FROM tweet_table1 WHERE date = '{}'".format(date)
		rows = session.execute(query)
		session.execute("DROP TABLE IF EXISTS tweet_table_author_frequency")
		session.execute("""
        CREATE TABLE tweet_table_author_frequency (
            author_id text,
            frequency counter,
            PRIMARY KEY (author_id)
        )
        """)
		for row in rows:
			if row.author_id:
				query = "UPDATE tweet_table_author_frequency SET frequency = frequency + 1 WHERE author_id = '{}'".format(row.author_id)
				session.execute(query)
		rows = session.execute("SELECT * FROM tweet_table_author_frequency")
		pop = {}
		for row in rows:
			pop.update({row.author_id : row.frequency})
		res = sorted(pop,key=pop.get,reverse=True)
		result = []
		k = 0
		for r in res:
			temp = []
			temp.append(date)
			temp.append(r)
			temp.append(pop[r])
			result.append(temp)
			k += 1
			print (temp)
		return render_template('lab.html',result=result,count=k,flag=1)

# Lab Query 2
@app.route('/labquery2', methods=['GET','POST'])
def labquery2():
	if request.method == 'GET':
		return render_template('lab.html',flag=0)
	elif request.method == 'POST':
		date = request.form['date2']
		# print (date)

		# Connecting cassandra session
		cluster = Cluster(['127.0.0.1'])
		session = cluster.connect()
		session.default_timeout = 60
		session.set_keyspace(KEYSPACE)

		query = "SELECT hashtag, location FROM tweet_table2 WHERE date = '{}'".format(date)
		rows = session.execute(query)
		session.execute("DROP TABLE IF EXISTS tweet_table_hashtag_location")
		session.execute("""
        CREATE TABLE tweet_table_hashtag_location (
            hashtag text,
            location text,
            frequency counter,
            PRIMARY KEY ((hashtag,location))
        )
        """)
		for row in rows:
			if row.hashtag and row.location:
				print (row.hashtag,row.location)					
				query = "UPDATE tweet_table_hashtag_location SET frequency = frequency + 1 WHERE hashtag = '{}'".format(row.hashtag) + "AND location = '{}'".format(row.location)
				session.execute(query)
		rows = session.execute("SELECT * FROM tweet_table_hashtag_location")
		pop = {}
		for row in rows:
			pop.update({(row.hashtag,row.location) : row.frequency})
		res = sorted(pop,key=pop.get,reverse=True)
		result = []
		k = 0
		for r in res:
			temp = []
			temp.append(date)
			temp.append(r[0])
			temp.append(r[1])
			temp.append(pop[r])
			result.append(temp)
			print (temp)
			k += 1
		return render_template('lab.html',result=result,count=k,flag=2)
	else:
		return render_template('lab.html',flag=0)
	

if __name__ == '__main__':
	app.run(host='127.0.0.1',port=5000,debug=True)