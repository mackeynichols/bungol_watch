from flask import Flask
from flask import jsonify
from flask_mail import Mail, Message
import utils
import os
import datetime
import json

app = Flask(__name__)



@app.route('/<input_address>')
def index(input_address):
	# skip garbage calls
	if input_address.upper() == "FAVICON.ICO":
		quit()

	# grab the payload
	bs = utils.BungolScraper( input_address )
	this_call_results = bs.get_address_payload() 
	print("Payload received")

	# if last payload file doesnt exist, make it and bypass this check process
	if not os.path.exists( input_address+".json" ):
		file = open( input_address+".json", "w" )
		json.dump( this_call_results, file) 
		file.close()
		print("New file created")


	else:

		# read old file
		last_call_file = open( input_address+".json", "r" ) 
		last_call_results =  json.load( last_call_file )
		last_call_file.close()
		print("Old file read")



		if last_call_results == this_call_results : 
			print("This call and the last calls' results are the same")

		else:
			print("There is a change between this call and the last one!")
			
			# Send an alert here
			

			# write new file
			file = open( input_address+".json", "w+" )
			json.dump( this_call_results, file)
			file.close()
			print("Payload written to new file")


	return jsonify( this_call_results )