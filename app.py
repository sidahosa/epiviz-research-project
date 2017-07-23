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

@app.route("/search")
def search(keyword, number):
	conn = MySQLdb.connect(host= "localhost",
	                  user="root",
	                  passwd="master",
	                  db="genome")
	x = conn.cursor()
	strstart = "'%"
	strend = "%'"
	keyword = strstart + keyword + strend
	genomeList = []
	try:
		x.execute("SELECT chr, start, end FROM human_genome WHERE gene LIKE %s LIMIT %d " %(keyword, number))
		data = x.fetchall()
		truedata = json.dumps(data)
		return truedata
	except:
		return 'No Keyword found'

	conn.close()

@app.route("/get_rows")
def get_rows(chromosome, param_start, param_end):
	conn = MySQLdb.connect(host= "localhost",
	                  user="root",
	                  passwd="master",
	                  db="genome")
	x = conn.cursor()
	strstart = "'%"
	strend = "%'"
	keyword = strstart + keyword + strend
	try:
		x.execute("SELECT %s FROM human_genome WHERE start >= %d AND end < %d " %(chromosome, param_start, param_end))
		data = x.fetchall()
		truedata = json.dumps(data)
		return truedata
	except:
		return 'No Keyword found'

	conn.close()

if __name__ == '__main__':
    app.run()
