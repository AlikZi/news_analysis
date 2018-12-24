# python 3.6
# Log Analysis Project made by Aleksandr Zonis

from flask import Flask
import psycopg2

app = Flask(__name__)

# HTML tepmlate for the news page
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
        h1{
            text-align: center;
            margin-bottom: 20px;
        }
        h3{
            text-align: left;
        }
        li{
            line-height: 1.5em;
        }
    </style>
</head>
<body>
    <h1>Log analysis results</h1>
    <h3>Three most popular articles:</h3>
    <!-- article content will go here -->
    <ol>
        %s
    </ol>
    <h3>The most popular article authors:</h3>
    <!-- authors content will go here -->
    <ul>
        %s
    </ul>
    <h3>Days when more than 1%% of requests lead to errors:</h3>
    <!-- bad requests content will go here -->
    <ul>
        %s
    </ul>
</body>
</html>
'''

ARTICLE = '''<li>"%s" - %d views</li>'''
AUTHOR = '''<li>%s - %d views</li>'''
BAD_REQUEST = '''<li>%s - %s%%</li>'''


def get_articles():
    # returns most popular articles that were accessed from news database
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


def get_authors():
    ''' returns most popular authors by articles that were
    accessed from news database'''
    db = psycopg2.connect("dbname=news")
    cur = db.cursor()
    cur.execute("select authors.name, count(*) as views"
                + " from log, articles, authors"
                + " where authors.id=articles.author and "
                + " substring(log.path from 10)=articles.slug"
                + " group by authors.name"
                + " order by views desc;")
    return cur.fetchall()
    db.close()


def get_errordays():
    # returns days when requests lead to errors more than 1%
    db = psycopg2.connect("dbname=news")
    cur = db.cursor()
    cur.execute("select to_char(tlogs.date, 'Mon DD, YYYY'),"
                + " round((cast(errors.num as DECIMAL(7,2))/cast(tlogs.num"
                + " as DECIMAL(7,2))*100),2) as percentage"
                + " from (select time::timestamp::date as date,"
                + " count(*) as num from log group by date) as tlogs,"
                + "(select time::timestamp::date as date,"
                + " count(*) as num from log"
                + " where status like '%%404%%' group by date) as errors"
                + " where tlogs.date=errors.date and"
                + " (cast(errors.num as DECIMAL(7,2))/cast(tlogs.num"
                + " as DECIMAL(7,2))*100)>1;")
    return cur.fetchall()
    db.close()


@app.route('/', methods=['GET'])
def main():
    # main page of news
    articles = "".join(ARTICLE % (title, views)
                       for (title, views) in get_articles())
    authors = "".join(AUTHOR % (name, views)
                      for (name, views) in get_authors())
    bad_requests = "".join(BAD_REQUEST % (day, num)
                           for (day, num) in get_errordays())
    html = HTML_WRAP % (articles, authors, bad_requests)
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
