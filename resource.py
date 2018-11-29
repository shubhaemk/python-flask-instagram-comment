from flask_restful import Resource, Api
from InstagramAPI import InstagramAPI
from flask import Flask, request
import urllib.request as ur
import json


app = Flask(__name__)
api = Api(app)


API = InstagramAPI("","")

class login(Resource):
    def put(self):
        global API
        data = request.get_json()
        API = InstagramAPI(data['username'],data['password'])
        if API.login():
            return {"login":"true"}
        else:
            return {"login":"false"}

class userFeed(Resource):
    def get(self):
        global API
        data = request.get_json()
        max_id = data["max_id"]
        API.getSelfUserFeed(maxid=max_id)
        if API.LastJson['more_available'] is not True:
            hmp = False
        else:
            hmp = True
        max_id = API.LastJson.get('next_max_id','')
        return {"feed": API.LastJson['items'],"hmp":hmp,"max_id":max_id}


class getComments(Resource):
    def get(self):
        global API
        data = request.get_json()
        media_id = data["media_id"]
        comment_count = data["comment_count"]
        API.getMediaComments(media_id,comment_count)
        return API.LastJson

class analyseComments(Resource):
    def get(self):
        global API
        data = request.get_json()
        media_id = data["media_id"]
        comment_count = data["comment_count"]
        API.getMediaComments(media_id,comment_count)
        #API.LastJson holds the json data to analyse


api.add_resource(analyseComments,"/analysecomments")
api.add_resource(getComments,"/getcomments")
api.add_resource(login,"/login")
api.add_resource(userFeed,"/userfeed")

if __name__ == '__main__':
     app.run(host='0.0.0.0',port=80)
