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

@app.route("/get_rows/<chromosome>/<int: param_start>/<int: param_end>")
def get_rows(chromosome, param_start, param_end):
	conn = MySQLdb.connect(host= "localhost",
	                  user="root",
	                  passwd="master",
	                  db="genome")
	x = conn.cursor()
	strstart = "'"
	strend = "'"
	chromosome = strstart + chromosome + strend
	param_start = strstart + param_start + strend
	param_end = strstart + param_end + strend
	try:
		x.execute("SELECT * FROM human_genome WHERE chr = %s AND start >= %s AND end < %s " %(chromosome, param_start, param_end))
		data = x.fetchall()
		truedata = json.dumps(data)
		return truedata
	except:
		return 'No Keyword found'

	conn.close()

@app.route("/get_values/<chromosome>/<int: param_start>/<int: param_end>/<any: measurements>")
def get_values(chromosome, param_start, param_end, measurements):
	conn = MySQLdb.connect(host= "localhost",
	                  user="root",
	                  passwd="master",
	                  db="genome")
	x = conn.cursor()

	strstart = "'"
	strend = "'"
	chromosome = strstart + chromosome + strend
	param_start = strstart + param_start + strend
	param_end = strstart + param_end + strend
	truedata = []

	try:
		x.execute("SELECT * FROM advancehumantbl WHERE seqnames = %s AND start >= %s AND end < %s" %(chromosome, param_start, param_end))
		#x.execute("SELECT * FROM advancehumantbl WHERE seqnames = %s AND start >= %s " %(chromosome, param_start))
		data = x.fetchall()

		for row in data:
			if measurement in row[7]:
				truedata.append(row)
		jsonDumped = json.dumps(truedata)
		
		return jsonDumped
	except:
		return 'No Keyword found'

	conn.close()

@app.route("/scale_data/<chromosome>/<int: param_start>/<int: param_end>/<any: measurement>/<int: resolution>")
def scale_data(chromosome, param_start, param_end, measurements, resolution):
	conn = MySQLdb.connect(host= "localhost",
	                  user="root",
	                  passwd="master",
	                  db="genome")
	x = conn.cursor()

	strstart = "'"
	strend = "'"
	chromosome = strstart + chromosome + strend
	param_start = strstart + param_start + strend
	param_end = strstart + param_end + strend
	truedata = []

	final_genome_data = []

	try:
		x.execute("SELECT * FROM advancehumantbl WHERE seqnames = %s AND start >= %s AND end < %s" %(chromosome, param_start, param_end))
		#x.execute("SELECT * FROM advancehumantbl WHERE seqnames = %s AND start >= %s " %(chromosome, param_start))
		data = x.fetchall()

		for row in data:
			if measurement in row[7]:
				truedata.append(row)
		#truedata = data

		if len(truedata) - resolution < 20:
			jsonDumped = json.dumps(truedata)
			return jsonDumped
		else:
			pval = 0.0
			med_diff = 0.0
			med_avg = 0.0
			strand = None
			width = 1
			mimstartarray = []
			mimendarray = []

			counter = 0

			for index in truedata:
				if index[6] != "NA":
					pval += float(index[6])
				med_diff += float(index[7])
				med_avg += float(index[8])
				strand = index[5]
				width = index[4]
				mimstartarray.append(int(index[2]))
				mimendarray.append(int(index[3]))

				if counter % resolution == 0:
					final_genome_data.append( (min(mimstartarray), min(mimendarray), width, strand, pval/300, med_diff/300, med_avg/300))
					pval = 0.0
					med_diff = 0.0
					med_avg = 0.0
					mimstartarray = []
					mimendarray = []

				counter += 1

			jsonDumped = json.dumps(final_genome_data)

			return jsonDumped
	except:
		return 'No Keyword found'

	conn.close()

if __name__ == '__main__':
    app.run()
