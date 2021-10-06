import base64
import json
import os
from bson import ObjectId, binary
from bson.json_util import dumps

from dotenv import load_dotenv
from flask import Flask, flash, request, redirect, url_for, Response
from flask_restful import Api
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
api = Api(app)
load_dotenv()
app.config['SESSION_TYPE'] = 'filesystem'
SECRET_KEY= os.getenv("SECRET_KEY")
DATABASE_URL=os.getenv("DATABASE_URL")
UPLOAD_FOLDER=os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = set(os.getenv("ALLOWED_EXTENSIONS").split(","))
DB_NAME=os.getenv("DB_NAME")
client =MongoClient(DATABASE_URL)
DB_INSTANCE = client[DB_NAME]
COLLECTION_NAME=os.getenv("COLLECTION_NAME")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key=SECRET_KEY

@app.route('/all', methods=['GET'])
def listCompanies():
    companies = DB_INSTANCE[COLLECTION_NAME].find()
    comps = list(companies)
    return Response(dumps(comps), mimetype='application/json'), 200

@app.route('/add', methods=['POST'])
def addCompany():

    inserted = DB_INSTANCE[COLLECTION_NAME].insert_one(request.json).inserted_id
    return Response(dumps({"success ":inserted}), mimetype='application/json'), 200


@app.route('/remove/<id>', methods=['DELETE'])
def removeCompany(id):

    a= ObjectId(request.data.decode("UTF-8"))
    removed = DB_INSTANCE[COLLECTION_NAME].delete_one({"_id":a}).deleted_count
    return Response(dumps({"Deleted_count":removed}), mimetype='application/json'), 200


@app.route('/upload', methods=["GET",'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            print("went1")
            return Response(json.dumps({"msg":"something went wron"}), mimetype='application/json'), 400

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            print("went2")
            return Response(json.dumps({"msg":"something went wron"}), mimetype='application/json'), 400
        if file and file.filename.split(".")[1] in ALLOWED_EXTENSIONS:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            print("went3")
            os.system(f'python yolov4-custom-functions/detect.py --weights yolov4 --size 416 --model yolov4 --images {UPLOAD_FOLDER}/{filename} --ocr')
            # return Response(json.dumps({"msg":"ok ", "file Name :": str(filename)}), mimetype='application/json'), 200

            with open(detections / {filename} / Detection.json) as jsonFile:
                jsonObject = json.load(jsonFile)
                jsonFile.close()
            return Response(dumps(jsonObject), mimetype='application/json'), 200
if __name__ == '__main__':
    app.run(debug=True)