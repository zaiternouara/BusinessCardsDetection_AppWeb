
import os
import h5py
import numpy as np
from bson import ObjectId, binary
from bson.json_util import dumps

from dotenv import load_dotenv
from flask import Flask, flash, request, redirect, url_for, Response
from flask_restful import Api
from matplotlib import pyplot as plt
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
import json
import pixellib
from pixellib.instance import custom_segmentation
app = Flask(__name__)
api = Api(app)
load_dotenv()
app.config['SESSION_TYPE'] = 'filesystem'
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
ALLOWED_EXTENSIONS = set(os.getenv("ALLOWED_EXTENSIONS").split(","))
DB_NAME = os.getenv("DB_NAME")
client = MongoClient(DATABASE_URL)
DB_INSTANCE = client[DB_NAME]
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = SECRET_KEY
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
model_path  = os.getenv("model_path ")
@app.route('/all', methods=['GET'])
@cross_origin(supports_credentials=True)
def listCompanies():
    companies = DB_INSTANCE[COLLECTION_NAME].find()
    comps = list(companies)

    return Response(dumps(comps), mimetype='application/json'), 200


@app.route('/add', methods=['POST'])
@cross_origin(supports_credentials=True)
def addCompany():
    inserted = DB_INSTANCE[COLLECTION_NAME].insert_one(request.json).inserted_id
    return Response(dumps({"success ": inserted}), mimetype='application/json'), 200


@app.route('/update/<id>', methods=['PUT'])
@cross_origin(supports_credentials=True)
def updateCompany(id):
    P = request.data.decode("UTF-8")

    body = request.json
    if('company_name' in body):
             company_name = body['company_name']
    else:
         company_name=''

    if ('phone_number' in body):
        phone_number= body['phone_number']
    else:
        phone_number = ''

    if ('fax' in body):
        fax = body['fax']
    else:
        fax = ''

    if ('email' in body):
        email= body['email']
    else:
        email= ''

    if ('website' in body):
        website= body['website']
    else:
        website = ''

    if ('adresse' in body):
        adresse= body['adresse']
    else:
        adresse = ''

    if ('fix' in body):
        fix= body['fix']
    else:
        fix = ''

    if ('propriaitaire' in body):
        propriaitaire= body['propriaitaire']
    else:
        propriaitaire= ''



    inserted = DB_INSTANCE[COLLECTION_NAME].update({"_id": ObjectId(id)}, {
                "$set": {
                    "company_name":company_name,
                    "phone_number":phone_number,
                    "fax": fax,
                    "email": email,
                    "website": website,
                    "adresse": adresse,
                    "fix": fix,
                    "propriaitaire":propriaitaire,
                }
            })
    return Response(dumps({"success ": inserted}), mimetype='application/json'), 200


@app.route('/remove/<id>', methods=['DELETE'])
def removeCompany(id):
    a = ObjectId(request.data.decode("UTF-8"))
    removed = DB_INSTANCE[COLLECTION_NAME].delete_one({"_id": a}).deleted_count
    return Response(dumps({"Deleted_count": removed}), mimetype='application/json'), 200


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part

        if 'file' not in request.files:
            flash('No file part')
            print("went1")
            return Response(json.dumps({"msg": "something went wrong"}), mimetype='application/json'), 400

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')

            return Response(json.dumps({"msg": "something went wron"}), mimetype='application/json'), 400
        if file and file.filename.split(".")[1] in ALLOWED_EXTENSIONS:

            filename = secure_filename(file.filename)

            file.save(os.path.join(UPLOAD_FOLDER, filename))

            print(os.path.join(UPLOAD_FOLDER, filename))

            """image_path = os.path.join(UPLOAD_FOLDER, filename)
            output_path = os.path.join(UPLOAD_FOLDER, filename)
            print({filename})
            print(output_path)
            segment_image = custom_segmentation()
            segment_image.inferConfig(num_classes=1, class_names=["BG", "card"])
            segment_image.load_model(model_path)
            print("1")
            segmask, output = segment_image.segmentImage(image_path, extract_segmented_objects=True, show_bboxes=True, output_image_name=output_path)
            sg = segmask['extracted_objects'].astype('int')
            print("2")
            a3 = np.array([sg], dtype=np.int32)
            print(a3.shape)
            if (a3.shape[1] > 0):
                # print(a3.shape[1])
                newarr = a3.reshape(a3.shape[2], a3.shape[3], a3.shape[4])
                newarr = newarr.astype(np.uint8)
                print(newarr.shape)
                print("13")
                plt.imsave("uploads/{filename}", newarr)"""

            os.system(
                f'python yolov4-custom-functions/detect.py --weights yolov4 --size 416 --model yolov4 --images uploads/{filename} --ocr')
            # return Response(json.dumps({"msg":"ok ", "file Name :": str(filename)}), mimetype='application/json'), 200
            print("wen")

            fil, file_extension = os.path.splitext(str(filename))
            test = r"C:\Users\Z T R\PycharmProjects\BusinessCardsDetection_AppWeb\backend\detections"
            print(os.path.join(test, fil))
            f = 'Detection.json'
            j = os.path.join(test, fil)
            print(os.path.join(j, f))
            with open(os.path.join(j, f)) as jsonFile:
                jsonObject: object = json.load(jsonFile)

                jsonFile.close()
            return Response(dumps(jsonObject), mimetype='application/json'), 200


if __name__ == '__main__':
    app.run(debug=True)
