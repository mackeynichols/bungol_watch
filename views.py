from flask import Flask
from flask import jsonify
import utils

app = Flask(__name__)

@app.route('/<input_address>')
def index(input_address):
	bs = utils.BungolScraper( input_address )
	return jsonify( bs.get_address_payload() )