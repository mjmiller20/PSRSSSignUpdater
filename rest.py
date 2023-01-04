#rest.py
# A program designed to serve the generated files as the result of a REST API request
# Author: Jarod Miller, 2022

from flask import Flask, make_response
from flask_restful import Resource, Api
from simplexml import dumps

app = Flask(__name__)
#api = Api(app)
api = Api(app, default_mediatype='application/xml')

@api.representation('application/xml')
def output_xml(data, code, headers=None):
	resp = make_response(dumps({'response' : data}), code)
	resp.headers.extend(headers or {})
	return resp

api.representations['application/xml'] = output_xml

class MLB(Resource):

    def get(self):
        f= open('ExportFiles/MLBScore.xml')
        data = f.read()
        return data, 200
    
    pass

class NBA(Resource):
   
    def get(self):
        f= open('ExportFiles/NBAScore.xml')
        data = f.read()
        return data, 200
    
    pass

class NFL(Resource):
    
    def get(self):
        f= open('ExportFiles/NFLScore.xml')
        data = f.read()
        return data, 200
    
    pass

class Stock(Resource):
    
    def get(self):
        f= open('ExportFiles/StockPrice.xml')
        data = f.read()
        return data, 200
    
    pass

api.add_resource(MLB, '/MLB')
api.add_resource(NBA, '/NBA')
api.add_resource(NFL, '/NFL')
api.add_resource(Stock, '/Stock')

if __name__ == '__main__':
    from waitress import serve
    serve(app, host = "192.168.1.224", port = 8080)
    #app.run()