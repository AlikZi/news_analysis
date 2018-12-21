#python 3.6
#Log Analysis Project made by Aleksandr Zonis

from flask import Flask
import psycopg2

app = Flask(__name__)

#HTML tepmlate for the news page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Log Analysis</title>
    <style>
      body{
      	width: 90%%;
      	margin: auto;
      }
      h1{ text-align: center; }
      h3{
      	text-align: left;
      }
    
    </style>
  </head>
  <body>
    <h1>Log analysis results</h1>
    <h3>Three most popular articles:</h2>
    <!-- article content will go here -->
    <ol>
    	%s
    </ol>
    <h3>The most popular article authors:</h2>
    <!-- authors content will go here -->
    <ul>
    	%s
    </ul>
    <h3>Days when more than 1%% of requests lead to errors:</h2>
    <!-- bad requests content will go here -->
    <ul>
    	%s
    </ul>
  </body>
</html>
'''

ARTICLE = '''<li>"%s" - %d views</li>'''
AUTHORS = '''<li>author name - number</li>'''
BAD_REQUESTS = '''<li>day - percentage</li>'''

def get_articles():
	db = psycopg2.connect("dbname=news")
	cur = db.cursor()
	cur.execute("select articles.title, count(*) as views" 
				 + " from log, articles" 
				 + " where substring(log.path from 10)=articles.slug" 
				 + " group by articles.title" 
				 + " order by views desc"
 				 + " limit 3;")
	return cur.fetchall()
	db.close()


@app.route('/', methods=['GET'])
def main():
	'''main page of news'''
	articles = "".join(ARTICLE % (title, views) for (title, views) in get_articles())
	html = HTML_WRAP % (articles, AUTHORS, BAD_REQUESTS)
	return html

if __name__=='__main__':
	app.run(host='0.0.0.0', port=8000)
















