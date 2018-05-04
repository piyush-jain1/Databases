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
		RETURN a1, COLLECT(t.tid) AS tweets, COUNT(a1.author_screen_name) AS mention_count
		ORDER BY (COUNT(a1.author_screen_name)) DESC LIMIT 2
        '''
		rows = graph.run(query, mention=mention)
		
		# with open('query6.json','w') as output:
		# 	print(rows.data(), file=output)

		# print (rows)

		result = []
		for r in rows:
			print (r)
			temp = []
			temp.append(r['a1']['author_screen_name'])
			temp.append(r['tweets'])
			temp.append(r['mention_count'])
			print("Temp : ", temp)
			result.append(temp)
		
		return render_template('lab.html',result=result,flag=1, mention=mention, query_title='Query 1')

# Query 2
@app.route('/q2', methods=['GET','POST'])
def q2():
	if request.method == 'GET':
		return render_template('lab.html',flag=0)
	elif request.method == 'POST':
		hashtag = request.form['hashtag']
		print (hashtag)

		query = '''
		MATCH (a:Author)-[:TWEETED]->(t:Tweet)-[:CONTAINS_HASHTAG]->(h:Hashtag)
		WHERE h.value={hashtag} AND t.type='Tweet'
		RETURN a, COLLECT(t.tid) AS tweets , COUNT(a.author_screen_name) AS tweet_count
		ORDER BY (COUNT(a.author_screen_name)) DESC LIMIT 3
        '''
		rows = graph.run(query, hashtag=hashtag)

		# with open('query8.json','w') as output:
		# 	print(rows.data(), file=output)

		result = []
		for r in rows:
			temp = []
			temp.append(r['a']['author_screen_name'])
			temp.append(r['tweets'])
			temp.append(r['tweet_count'])			
			print("Temp : ", temp)
			result.append(temp)
		
		return render_template('lab.html',result=result, hashtag= hashtag, flag=2, query_title='Query 2')

if __name__ == '__main__':
	app.run(host='127.0.0.1',port=5000,debug=True)