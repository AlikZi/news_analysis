#python 3.6
#Log Analysis Project made by Aleksandr Zonis

from flask import Flask

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

ARTICLES = '''<li>article name - views</li>'''
AUTHORS = '''<li>author name - number</li>'''
BAD_REQUESTS = '''<li>day - percentage</li>'''

@app.route('/', methods=['GET'])
def main():
	'''main page of news'''
	html = HTML_WRAP % (ARTICLES, AUTHORS, BAD_REQUESTS)
	return html

if __name__=='__main__':
	app.run(host='0.0.0.0', port=8000)
















