import flask
from flask_cors import CORS, cross_origin
import json
import requests

from flask import request

app = flask.Flask(__name__)

CORS_ALLOW_ORIGIN="*,*"
CORS_EXPOSE_HEADERS="*,*"
CORS_ALLOW_HEADERS="content-type,*"
cors = CORS(app, origins=CORS_ALLOW_ORIGIN.split(","), allow_headers=CORS_ALLOW_HEADERS.split(",") , expose_headers= CORS_EXPOSE_HEADERS.split(","),   supports_credentials = True)

app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading </h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

CORS_ALLOW_ORIGIN="*,*"
CORS_EXPOSE_HEADERS="*,*"
CORS_ALLOW_HEADERS="content-type,*"
cors = CORS(app, origins=CORS_ALLOW_ORIGIN.split(","), allow_headers=CORS_ALLOW_HEADERS.split(",") , expose_headers= CORS_EXPOSE_HEADERS.split(","),   supports_credentials = True)

app.config["DEBUG"] = True
@app.route('/storeData', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    userName = record['userName']

    status = "user already exist"
    str_to_insert = record['userName']+"\t"+record['password']+"\t"+record['name']+"\t"+record['phone']+"\n"
    if(check_username_exist(userName) == False):
        add_user_to_file(str_to_insert)
        status = "success"
    print(record)

    return({"status":status})


def check_username_exist(userName):
    f = open("./users.txt", "r")
    current_data = f.readlines()
    status = False
    f.close()
    for i in current_data:
        if(i.split("\t")[0] == userName):
            status = True
            break
    return status

def check_password(userName,password):
    f = open("./users.txt", "r")
    current_data = f.readlines()
    status = False
    f.close()
    for i in current_data:
        if(i.split("\t")[0] == userName and i.split("\t")[1] == password):
            status = True
            break
        elif(i.split("\t")[0] == userName and i.split("\t")[1] != password):
            status = "PWD WRONG"
    return status

def add_user_to_file(s):
    f = open("./users.txt","a")
    f.write(s)
    f.close()

@app.route('/checkData', methods=['POST'])
def check_record():
    record = json.loads(request.data)
    userName = record['userName']
    password = record['password']

    status = "no user found"
    pwdmatch= check_password(userName,password)
    if(pwdmatch == True):
        status = "success"
    elif(pwdmatch == "PWD WRONG"):
        status = "password wrong"
    print(record)

    return({"status":status})

@app.route('/storeLinks', methods=['POST'])
def add_userdetails_to_file():
    record = json.loads(request.data)
    # print(record.data)
    str_to_insert = record['username']+"\t"+record['linkedin']+"\t"+record['twitter']+"\t"+record['git']+"\t"+record['facebook']+"\t"+record['instagram']+"\n"
    f = open("./links.txt","a")
    f.write(str_to_insert)
    f.close()
    print("Inserted")
    return({"status":"success"})

app.run()
