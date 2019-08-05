from flask import Flask
from flask import jsonify
import utils
import os
import datetime
import json

app = Flask(__name__)

@app.route('/<input_address>')
def index(input_address):

	# grab the payload
	bs = utils.BungolScraper( input_address )
	this_call_results = bs.get_address_payload() 

	# if last payload file doesnt exist, make it and bypass this check process
	if not os.path.exists( input_address+".json" ):
		file = open( input_address+".json", "w" )
		json.dump( this_call_results, file) 
		file.close()

	else:

		# if last call (stored in file) 's contents match new call's contents, dont send alert
		last_call_file = open( input_address+".json", "r" ) 
		last_call_results =  json.load( last_call_file )
		last_call_file.close()


		if last_call_results == this_call_results : 
			print("This call and the last calls' results are the same")

		else:
			print("There is a change between this call and the last one!")
			# Send an alert here
			file = open( input_address+".json", "w+" )
			json.dump( this_call_results, file)
			file.close()


	return jsonify( this_call_results )