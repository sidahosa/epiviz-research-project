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
	truedata = []

	try:
		x.execute("SELECT pval, meth_diff, meth_avg FROM advancehumantbl WHERE seqnames = %s AND pval = %d AND meth_diff = %d AND meth_avg = %d AND start >= %d AND end < %d" %(chromosome, measurement[0], measurement[1], measurement[2], param_start, param_end))
		#x.execute("SELECT * FROM advancehumantbl WHERE seqnames = %s AND start >= %s " %(chromosome, param_start))
		data = x.fetchall()

		jsonDumped = json.dumps(data)
		
		return jsonDumped
	except:
		return 'No Keyword found'

	conn.close()

@app.route("/scale_data/<chromosome>/<int: param_start>/<int: param_end>/<any: measurement>/<int: resolution>")
def scale_data(chromosome, param_start, param_end, measurements, resolution):
	strstart = "'"
	strend = "'"
	chromosome = strstart + chromosome + strend
	seqnames = []

	final_genome_data = []
	db_connection = sql.connect(host='localhost', database='genome', user='root', password='master')
	df = pd.read_sql("SELECT * FROM advancehumantbl WHERE seqnames = %s AND pval = %d AND meth_diff = %d AND meth_avg = %d AND start >= %d AND end < %d" %(chromosome, measurement[0], measurement[1], measurement[2], param_start, param_end), con=db_connection)
	#df = pd.read_sql("SELECT seqnames, start, end, pval, methylation_diff, methylation_avg FROM advancehumantbl", con=db_connection)

	if len(df) - resolution < 20:
			#jsonDumped = json.dumps(df)
			#return jsonDumped
			return df
	else:
		# Gets the min of start position and max of end position in genome
		tempMin = df['start'].min()
		tempMax = df['end'].max()
		# create random index
		rindex =  np.array(sample(xrange(len(df)), resolution))
		seqnames =  df['seqnames'].values[rindex]

		# Calculates the average of the pval, meth_diff, and meth_avg for every resolution
		df = df.groupby(df.index//resolution).mean()

		df['seqnames'] = ""
		for i in range(len(df)):
			df.set_value(i, 'seqnames', seqnames[i])

		df['start'] = tempMin
		df['end'] = tempMax

		#print(df)
		#return jsonDumped
		return df

if __name__ == '__main__':
    app.run()
