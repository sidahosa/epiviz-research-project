from flask import Flask
import json
import MySQLdb
import pandas as pd
import numpy as np
from random import sample
import mysql.connector as sql
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

@app.route("/get_rows/<chromosome>/<int:param_start>/<int:param_end>")
def get_rows(chromosome, param_start, param_end):
	conn = MySQLdb.connect(host= "localhost",
	                  user="root",
	                  passwd="master",
	                  db="genome")
	x = conn.cursor()
	strstart = "'"
	strend = "'"
	chromosome = strstart + chromosome + strend
	try:
		x.execute("SELECT * FROM human_genome WHERE chr = %s AND start >= %d AND end < %d " %(chromosome, param_start, param_end))
		data = x.fetchall()
		truedata = json.dumps(data)
		return truedata
	except:
		return 'No Keyword found'

	conn.close()

@app.route("/get_values/<chromosome>/<int:param_start>/<int:param_end>/<any:measurements>")
def get_values(chromosome, param_start, param_end, measurements):
	conn = MySQLdb.connect(host= "localhost",
	                  user="root",
	                  passwd="master",
	                  db="genome")
	x = conn.cursor()

	strstart = "'"
	strend = "'"
	chromosome = strstart + chromosome + strend
	columnNames = ",".join(measurement)
	columnNames += ", chr, start, end"
	truedata = []

	try:
		x.execute("SELECT %s FROM chromosomes_sample WHERE chr = %s AND start >= %d AND end < %d" %(columnNames, chromosome, param_start, param_end))
		data = x.fetchall()
		jsonDumped = json.dumps(data)
		
		return jsonDumped
	except:
		return 'No Keyword found'

	conn.close()

@app.route("/scale_data/<chromosome>/<int:param_start>/<int:param_end>/<int:resolution>/<path:measurement>")
def scale_data(chromosome, param_start, param_end, resolution, measurement):
	strstart = "'"
	strend = "'"
	chromosome = strstart + chromosome + strend
	seqnames = []

	measurement = measurement.split("/")
	columnNames = ",".join(measurement)
	columnNames += ", chr, start, end"

	final_genome_data = []
	db_connection = sql.connect(host='localhost', database='genome', user='root', password='master')
	df = pd.read_sql("SELECT %s FROM chromosomes_sample WHERE chr = %s AND start >= %d AND end < %d" %(columnNames, chromosome, param_start, param_end), con=db_connection)

	if len(df) - resolution < 20:
			return df
	else:
		# Gets the min of start position and max of end position in genome
		tempMin = df['start'].min()
		tempMax = df['end'].max()
		
		new_res = len(df)/resolution

		# create random index
		rindex =  np.array(sample(xrange(len(df)), len(df)/new_res+1))
		seqnames =  df['chr'].values[rindex]

		#print("Before scaling")
		#print(len(df))

		# Calculates the average of the pval, meth_diff, and meth_avg for every resolution
		df = df.groupby(df.index//new_res).mean()

		#print("After scaling")
		#print(len(df))

		df['chr'] = ""
		for i in range(len(df)):
		 	df.set_value(i, 'chr', seqnames[i])

		df['start'] = tempMin
		df['end'] = tempMax

		print(df)
		#return jsonDumped
		return df
		#return "This works!"

	db_connection.close()

if __name__ == '__main__':
    app.run(threaded=True)
