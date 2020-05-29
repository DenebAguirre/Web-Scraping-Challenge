from flask import Flask
from scrape_mars import scrape
import pymongo

app = Flask(__name__)

@app.route("/scrape")
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.marsdb
    db.mars_today.insert(scrape())


@app.route("/")







if __name__ == '__main__':
    app.run(debug=True)