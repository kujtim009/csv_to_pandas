from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Api
import urllib
from models.files import (
         ReadCsvFiles,
         Compare_layouts)


app = Flask(__name__)
CORS(app)
api = Api(app)


api.add_resource(ReadCsvFiles, '/read')
api.add_resource(Compare_layouts, '/compare')
# api.add_resource(Record_by_license, '/licence/<int:license>')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
