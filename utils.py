#! python3
# utils.py - a series of tools for the bungol_watch scraper

import requests, json

class BungolScraper:

	# set starting variables, specific to 150 sudbury and its environs
	def __init__(self, address):	
		
		self.address = address.upper()
		print( "Received address: " + self.address)

		# grab the token you need to make requests to the site
		self.req = requests.Session()
		self.csrf_token = self.req.post("https://www.bungol.ca/map").headers['Set-Cookie'].split('=')[1].split(';')[0]

		# assign headers we'll need to make requests
		self.req_headers = {
			"Host":"www.bungol.ca",
			"Connection":"keep-alive",
			"Content-Length":"267",
			"Origin":"https://www.bungol.ca",
			"X-CSRFToken": "\""+self.csrf_token+"\"",
			"X-Requested-With":"XMLHttpRequest",
			"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
			"Content-Type":"multipart/form-data; boundary=----WebKitFormBoundarymi2ryGhPham8qInY",
			"Accept":"*/*",
			"Referer":"https://www.bungol.ca/",
			"Accept-Encoding":"gzip, deflate, br",
			"Accept-Language":"en-US,en;q=0.9",
			"Cookie":"csrftoken="+self.csrf_token+"; sessionid=9ajyy5gwpn86xbltydeutty9zyyty6fh; __utmmobile=d44f220a-b9e5-4e1d-9ba1-4f038a62698f"
		}

		# latitude and longitude object for our input address
		self.address_coordinates = self.get_address_coordinates()


		# build request URL for the input address
		self.base_api_url = "https://www.bungol.ca/api/f/?min-lat="+self.address_coordinates["latitude"]+"&max-lat="+self.address_coordinates["latitude"]+"&min-lng="+self.address_coordinates["longitude"]+"&max-lng="+self.address_coordinates["longitude"]+"&sitl=730&low=0&high=0&show-active=true&show-sold=true&show-ended=false&transaction-type=Sale&list-view-activated=n&school-id=undefined&sb-activated=false&dom-range=x&screen-width=787&pt1=false&pt2=false&pt3=false&pt4=false&pt5=false&pt9=false&bed-0=false&bed-1=false&bed-1plus=false&bed-2=false&bed-3=false&bed-4=false&bed-5=false&bed-6=false&bath-1=false&bath-2=false&bath-3=false&bath-4=false&bath-5=false&bath-6=false&park0=false&park1=false&park2=false&park3=false&oh=false"

  		# get CSRF token
		self.req = requests.Session()
		self.csrf_token = self.req.post("https://www.bungol.ca/map").headers['Set-Cookie'].split('=')[1].split(';')[0]


	def get_address_coordinates(self):

		# get coordinates for input address
		login_payload = {"csrfmiddlewaretoken" : self.csrf_token}
		coordinates_response =  json.loads(self.req.get( "https://www.bungol.ca/api/property-search-autocomplete/?value="+self.address.replace(" ", "%20"), data = json.dumps(login_payload), headers = self.req_headers ).text )

		return { "latitude" : coordinates_response["addresses"][0]['la'], "longitude" : coordinates_response["addresses"][0]['lo'] }


	def get_address_payload(self):
		
		# use the token to get a data payload for a specific address
		response_payload = []
		login_payload = {"csrfmiddlewaretoken" : self.csrf_token}	

		# get basic pricing information for self.address
		pricing_response = self.req.get( self.base_api_url, data = json.dumps(login_payload), headers = self.req_headers ) 
		pricing_response_payload = [ result for result in json.loads(pricing_response.text)["results"] if result['street'].upper() ==  self.address.upper() ]

		# get more detailed listing data (unit amenities, size details, etc)
		for unit in pricing_response_payload:
			address_listing_details_response = self.req.get( "https://www.bungol.ca/api/get-listing-data/"+unit['mls_number']+"-"+str(unit['id']), data = json.dumps(login_payload), headers = self.req_headers ) 
			unit['listing_details'] = json.loads(address_listing_details_response.text)
			response_payload.append( unit )


		return response_payload


	def return_parsed_payload(self):
		self.get_address_payload()


if __name__ == "__main__":
	bs = BungolScraper("55 EAST LIBERTY ST")
	print( bs.get_address_payload() )

