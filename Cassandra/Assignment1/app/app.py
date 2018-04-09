from flask import Flask,request,render_template,redirect, url_for
from flask import jsonify
import requests
from cassandra.cluster import Cluster
from collections import OrderedDict

app = Flask(__name__)

KEYSPACE = "twitterkeyspace"

#  Dahsboard Page
@app.route('/', methods=['GET'])
def dashboard():
	if request.method == 'GET':
		return render_template('dashboard.html')

# Query 1
@app.route('/q1', methods=['GET','POST'])
def q1():
	if request.method == 'GET':
		return render_template('q1.html',flag=0)
	elif request.method == 'POST':
		author_name = request.form['author_name']
		# print (author_name)

		# Connecting cassandra session
		cluster = Cluster(['127.0.0.1'])
		session = cluster.connect()
		session.default_timeout = 60
		session.set_keyspace(KEYSPACE)

		query = "SELECT * FROM tweet_table1 WHERE author_screen_name = "+ "'{}'".format(author_name)
		rows = session.execute(query)
		result = []
		k = 1
		for row in rows:
			temp = []
			temp.append(k)
			temp.append(row.tid)
			temp.append(row.tweet_text)
			temp.append(row.author_id)
			temp.append(row.location)
			temp.append(row.lang)
			temp.append(row.datetime)
			result.append(temp)
			k += 1
		return render_template('q1.html',result=result,flag=1)

# Query 2
@app.route('/q2', methods=['GET','POST'])
def q2():
	if request.method == 'GET':
		return render_template('q2.html',flag=0)
	elif request.method == 'POST':
		keyword = request.form['keyword']
		# print (keyword)

		# Connecting cassandra session
		cluster = Cluster(['127.0.0.1'])
		session = cluster.connect()
		session.default_timeout = 60
		session.set_keyspace(KEYSPACE)

		query = "SELECT * FROM tweet_table2 WHERE keyword = '{}'".format(keyword)
		rows = session.execute(query)
		result = []
		k = 1
		for row in rows:
			temp = []
			temp.append(k)
			temp.append(row.tid)
			temp.append(row.tweet_text)
			temp.append(row.author_id)
			temp.append(row.location)
			temp.append(row.lang)
			temp.append(row.like_count)
			result.append(temp)
			k += 1
		return render_template('q2.html',result=result,flag=1)

# Query 3
@app.route('/q3', methods=['GET','POST'])
def q3():
	if request.method == 'GET':
		return render_template('q3.html',flag=0)
	elif request.method == 'POST':
		hashtag = request.form['hashtag']
		# print (hashtag)

		# Connecting cassandra session
		cluster = Cluster(['127.0.0.1'])
		session = cluster.connect()
		session.default_timeout = 60
		session.set_keyspace(KEYSPACE)

		query = "SELECT * FROM tweet_table3 WHERE hashtag = '{}'".format(hashtag)
		rows = session.execute(query)
		result = []
		k = 1
		for row in rows:
			temp = []
			temp.append(k)
			temp.append(row.tid)
			temp.append(row.tweet_text)
			temp.append(row.author_id)
			temp.append(row.location)
			temp.append(row.lang)
			temp.append(row.datetime)
			result.append(temp)
			k += 1
		return render_template('q3.html',result=result,flag=1)

# Query 4
@app.route('/q4', methods=['GET','POST'])
def q4():
	if request.method == 'GET':
		return render_template('q4.html',flag=0)
	elif request.method == 'POST':
		author_name = request.form['author_name']
		# print (author_name)

		# Connecting cassandra session
		cluster = Cluster(['127.0.0.1'])
		session = cluster.connect()
		session.default_timeout = 60
		session.set_keyspace(KEYSPACE)

		query = "SELECT * FROM tweet_table4 WHERE mention = '{}'".format(author_name)
		rows = session.execute(query)
		result = []
		k = 1
		for row in rows:
			temp = []
			temp.append(k)
			temp.append(row.tid)
			temp.append(row.tweet_text)
			temp.append(row.author_id)
			temp.append(row.location)
			temp.append(row.lang)
			temp.append(row.datetime)
			result.append(temp)
			k += 1
		return render_template('q4.html',result=result,flag=1)

# Query 5
@app.route('/q5', methods=['GET','POST'])
def q5():
	if request.method == 'GET':
		return render_template('q5.html',flag=0)
	elif request.method == 'POST':
		date = request.form['date']
		# print (date)

		# Connecting cassandra session
		cluster = Cluster(['127.0.0.1'])
		session = cluster.connect()
		session.default_timeout = 60
		session.set_keyspace(KEYSPACE)

		query = "SELECT * FROM tweet_table5 WHERE date = "+ "'{}'".format(date)
		rows = session.execute(query)
		result = []
		k = 1
		for row in rows:
			temp = []
			temp.append(k)
			temp.append(row.tid)
			temp.append(row.tweet_text)
			temp.append(row.author_id)
			temp.append(row.location)
			temp.append(row.lang)
			temp.append(row.like_count)
			result.append(temp)
			k += 1
		return render_template('q5.html',result=result,flag=1)

# Query 6
@app.route('/q6', methods=['GET','POST'])
def q6():
	if request.method == 'GET':
		return render_template('q6.html',flag=0)
	elif request.method == 'POST':
		location = request.form['location']
		# print (location)

		# Connecting cassandra session
		cluster = Cluster(['127.0.0.1'])
		session = cluster.connect()
		session.default_timeout = 60
		session.set_keyspace(KEYSPACE)

		query = "SELECT * FROM tweet_table6 WHERE location = "+ "'{}'".format(location)
		rows = session.execute(query)
		result = []
		k = 1
		for row in rows:
			temp = []
			temp.append(k)
			temp.append(row.tid)
			temp.append(row.tweet_text)
			temp.append(row.author_id)
			temp.append(row.lang)
			result.append(temp)
			k += 1
		return render_template('q6.html',result=result,flag=1)

# Query 7
@app.route('/q7', methods=['GET','POST'])
def q7():
	if request.method == 'GET':
		return render_template('q7.html',flag=0)
	elif request.method == 'POST':
		date = request.form['date']
		# print (date)

		# Connecting cassandra session
		cluster = Cluster(['127.0.0.1'])
		session = cluster.connect()
		session.default_timeout = 60
		session.set_keyspace(KEYSPACE)

		query = "SELECT hashtags FROM tweet_table7 WHERE date = '{}'".format(date)
		rows = session.execute(query)
		session.execute("DROP TABLE IF EXISTS tweet_table_hashtag_popularity")
		session.execute("""
        CREATE TABLE tweet_table_hashtag_popularity (
            hashtag text,
            popularity_count counter,
            PRIMARY KEY (hashtag)
        )
        """)
		for row in rows:
			if row.hashtags:
				for tag in row.hashtags:
					# print(tag)
					query = "UPDATE tweet_table_hashtag_popularity SET popularity_count = popularity_count + 1 WHERE hashtag = '{}'".format(tag)
					session.execute(query)
		rows = session.execute("SELECT * FROM tweet_table_hashtag_popularity")
		pop = {}
		for row in rows:
			pop.update({row.hashtag : row.popularity_count})
		res = sorted(pop,key=pop.get,reverse=True)
		result = []
		k = 1
		for r in res:
			temp = []
			temp.append(k)
			temp.append(r)
			temp.append(pop[r])
			result.append(temp)
			k += 1
			if k > 20:
				break
		return render_template('q7.html',result=result,flag=1)

# Query 8
@app.route('/q8', methods=['GET','POST'])
def q8():
	print ("request.method = ",request.method)
	if request.method == 'GET':
		return render_template('q8.html', flag=0)
	elif request.method == 'POST':
		date = request.form['date']
		# print (date)
		result = []
		result.append(date)

		# Connecting cassandra session
		cluster = Cluster(['127.0.0.1'])
		session = cluster.connect()
		session.default_timeout = 60
		session.set_keyspace(KEYSPACE)

		query = "SELECT COUNT(*) FROM tweet_table5"
		r = session.execute(query)
		for row in r:
			r1 = row.count
		query = "DELETE FROM tweet_table5 WHERE date = "+ "'{}'".format(date)
		session.execute(query)
		query = "SELECT COUNT(*) FROM tweet_table5"
		r = session.execute(query)
		for row in r:
			r2 = row.count
		result.append(r1-r2)
		return render_template('q8.html', result=result, flag=1)

# Lab Queries
@app.route('/labquery', methods=['GET','POST'])
def labquery():
	if request.method == 'GET':
		return render_template('lab.html',flag=0)
	elif request.method == 'POST':
		query_num = request.form['query_num']
		if query_num == 1:
			author_name = request.form['author_name']
			# print (author_name)

			# Connecting cassandra session
			cluster = Cluster(['127.0.0.1'])
			session = cluster.connect()
			session.default_timeout = 60
			session.set_keyspace(KEYSPACE)

			query = "SELECT * FROM tweet_table1 WHERE author_screen_name = "+ "'{}'".format(author_name)
			rows = session.execute(query)
			result = []
			k = 1
			for row in rows:
				temp = []
				temp.append(k)
				temp.append(row.tid)
				temp.append(row.tweet_text)
				temp.append(row.author_id)
				temp.append(row.location)
				temp.append(row.lang)
				temp.append(row.datetime)
				result.append(temp)
				k += 1
			return render_template('lab.html',result=result,flag=1)
		elif query_num == 2:
			author_name = request.form['author_name']
			# print (author_name)

			# Connecting cassandra session
			cluster = Cluster(['127.0.0.1'])
			session = cluster.connect()
			session.default_timeout = 60
			session.set_keyspace(KEYSPACE)

			query = "SELECT * FROM tweet_table1 WHERE author_screen_name = "+ "'{}'".format(author_name)
			rows = session.execute(query)
			result = []
			k = 1
			for row in rows:
				temp = []
				temp.append(k)
				temp.append(row.tid)
				temp.append(row.tweet_text)
				temp.append(row.author_id)
				temp.append(row.location)
				temp.append(row.lang)
				temp.append(row.datetime)
				result.append(temp)
				k += 1
			return render_template('lab.html',result=result,flag=2)

if __name__ == '__main__':
	app.run(host='127.0.0.1',port=5000,debug=True)