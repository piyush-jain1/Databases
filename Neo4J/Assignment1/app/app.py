from flask import Flask,request,render_template,redirect, url_for
from flask import jsonify
import requests, os, json
from py2neo import Graph, Node, Relationship

app = Flask(__name__)

url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username = 'neo4j'
password = 'neo4jpiyush'
graph = Graph(url + '/db/data/', username=username, password=password)

#  Dahsboard Page
@app.route('/', methods=['GET'])
def dashboard():
	if request.method == 'GET':
		return render_template('lab.html',query_title='Dashboard')

# Query 1
@app.route('/q1', methods=['GET','POST'])
def q1():
	if request.method == 'GET':
		return render_template('lab.html',flag=0)
	elif request.method == 'POST':
		mention = request.form['mention']
		print (mention)

		query = '''
        MATCH (a1:Author)-[:TWEETED]->(t:Tweet)-[:MENTIONS]->(a2:Author)
		WHERE a2.author_screen_name={mention}
		RETURN a1.author_screen_name, COLLECT(t.tid) AS tweets, COUNT(a1.author_screen_name) AS mention_count
		ORDER BY (COUNT(a1.author_screen_name)) DESC LIMIT 2
        '''
		rows = graph.run(query, mention=mention)
		result = []
		k = 0
		for r in rows:
			print (r['t'])
			k += 1
			temp = []
			temp.append(r['a1']['author_screen_name'])
			temp.append(r['tweets']['tweet_text'])
			temp.append(r['mention_count'])
			# print("Temp : ", temp)
			result.append(temp)
		
		# print (k)
		return render_template('lab.html',result=result,flag=1, query_title='Query 1')

# Query 2
@app.route('/q2', methods=['GET','POST'])
def q2():
	if request.method == 'GET':
		return render_template('q2.html',flag=0)
	elif request.method == 'POST':
		hashtag = request.form['hashtag']
		print (hashtag)

		query = '''
		MATCH (a:Author)-[:TWEETED]->(t:Tweet)-[:MENTIONS]->(m:Author)
		WHERE a.author_screen_name={hashtag}
		RETURN m
        '''
		rows = graph.run(query, hashtag=hashtag)
		result = []
		k = 0
		for r in rows:
			print (r['m'])
			k += 1
			temp = []
			temp.append(r['m']['author_screen_name'])
			print("Temp : ", temp)
			result.append(temp)
		
		print (k)
		return render_template('q2.html',result=result, author_name= author_name, count=k,flag=1, query_title='Query 2')

# Query 3
@app.route('/q3', methods=['GET','POST'])
def q3():
	if request.method == 'GET':
		query = '''
        MATCH (h1:Hashtag)<-[:CONTAINS_HASHTAG]-(t:Tweet)-[:CONTAINS_HASHTAG]->(h2:Hashtag)
		WHERE h1.value < h2.value
		RETURN h1.value,h2.value, COUNT([h1,h2]) AS frequency
		ORDER BY COUNT([h1,h2]) DESC LIMIT 20
        '''
		rows = graph.run(query)
		result = []
		for r in rows:
			temp = []
			temp.append([r['h1.value'],r['h2.value']])
			temp.append(r['frequency'])
			print("Temp : ", temp)
			result.append(temp)
		
		return render_template('q3.html',result=result,flag=1, query_title='Query 3')

# Query 4
@app.route('/q4', methods=['GET','POST'])
def q4():
	if request.method == 'GET':
		return render_template('q4.html',flag=0, query_title='Query 4')
	elif request.method == 'POST':
		hashtag = request.form['hashtag']
		# print (hashtag)

		query = '''
        MATCH (m:Author)<-[:MENTIONS]-(t:Tweet)-[:CONTAINS_HASHTAG]->(h:Hashtag)
		WHERE h.value={hashtag}
		RETURN m.author_screen_name, COUNT([m,h]) AS frequency
		ORDER BY COUNT([m,h]) DESC LIMIT 20
        '''
		rows = graph.run(query,hashtag=hashtag)
		result = []
		for r in rows:
			temp = []
			temp.append(r['m.author_screen_name'])
			temp.append(r['frequency'])
			print("Temp : ", temp)
			result.append(temp)
		
		return render_template('q4.html',result=result,flag=1, query_title='Query 4', hashtag=hashtag)

# Query 5
@app.route('/q5', methods=['GET','POST'])
def q5():
	if request.method == 'GET':
		return render_template('q5.html',flag=0, query_title='Query 5')
	elif request.method == 'POST':
		location = request.form['location']
		# print (location)

		query = '''
        MATCH (l:Location)<-[:TWEETED_FROM]-(t:Tweet)-[:CONTAINS_HASHTAG]->(h:Hashtag)
		WHERE l.value={location}
		RETURN DISTINCT h.value
        '''
		rows = graph.run(query, location=location)
		result = []
		k = 0
		for r in rows:
			k += 1
			result.append(r['h.value'])
		
		print (k)
		return render_template('q5.html',result=result,flag=1, query_title='Query 5',location=location,count=k)

# Query 6
@app.route('/q6', methods=['GET','POST'])
def q6():
	if request.method == 'GET':
		query = '''
        MATCH (a1:Author)-[:TWEETED]->(t1:Tweet)-[:RETWEET_OF]->(t2:Tweet)<-[:TWEETED]-(a2:Author)
		RETURN a1.author_screen_name,a2.author_screen_name, COUNT([a1.author_screen_name,a2.author_screen_name]) AS frequency
		ORDER BY COUNT([a1.author_screen_name,a2.author_screen_name]) DESC LIMIT 5
        '''
		rows = graph.run(query)
		result = []
		for r in rows:
			temp = []
			temp.append([r['a1.author_screen_name'],r['a2.author_screen_name']])
			temp.append(r['frequency'])
			print("Temp : ", temp)
			result.append(temp)
		return render_template('q6.html',result=result,flag=1, query_title='Query 6')

# Query 7
@app.route('/q7', methods=['GET','POST'])
def q7():
	if request.method == 'GET':
		query = '''
        MATCH (a1:Author)-[:TWEETED]->(t1:Tweet)-[:REPLY_OF]->(t2:Tweet)<-[:TWEETED]-(a2:Author)
		RETURN a1.author_screen_name,a2.author_screen_name, COUNT([a1.author_screen_name,a2.author_screen_name]) AS frequency
		ORDER BY COUNT([a1.author_screen_name,a2.author_screen_name]) DESC LIMIT 5
        '''
		rows = graph.run(query)
		result = []
		for r in rows:
			temp = []
			temp.append([r['a1.author_screen_name'],r['a2.author_screen_name']])
			temp.append(r['frequency'])
			print("Temp : ", temp)
			result.append(temp)
		return render_template('q7.html',result=result,flag=1, query_title='Query 7')

# Query 8
@app.route('/q8', methods=['GET','POST'])
def q8():
	print ("request.method = ",request.method)
	if request.method == 'GET':
		return render_template('q8.html', flag=0, query_title='Query 8')
	elif request.method == 'POST':
		author_name = request.form['author_name']
		# print (author_name)

		query = '''
        MATCH (t:Tweet)<-[:TWEETED]-(a:Author)
		WHERE a.author_screen_name={author_name}
		DETACH DELETE t
        '''
		graph.run(query, author_name=author_name)
		
		return render_template('q8.html', flag=1, query_title='Query 8', author_name=author_name)


if __name__ == '__main__':
	app.run(host='127.0.0.1',port=5000,debug=True)