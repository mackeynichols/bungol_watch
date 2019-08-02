from flask import Flask
from flask import jsonify
import utils

app = Flask(__name__)

@app.route('/')
def index():
	bs = utils.BungolScraper("55 EAST LIBERTY ST")
	return jsonify(bs.get_address_payload())