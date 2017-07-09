from flask import Flask
import json
import MySQLdb
app = Flask(__name__)

@app.route("/")
def getSeqInfo(genome): 
	conn = MySQLdb.connect(host= "localhost",
	                  user="root",
	                  passwd="master",
	                  db="genome")
	x = conn.cursor()
	try:
		x.execute("SELECT * FROM " + genome)
		data = x.fetchall()
		truedata = json.dumps(data)
		return truedata
	except:
		return "No Table Found"

	conn.close()

if __name__ == '__main__':
    app.run()