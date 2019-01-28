from flask_restful import Resource, Api
from InstagramAPI import InstagramAPI
from flask import Flask, request

app = Flask(__name__)
api = Api(app)


API = InstagramAPI("","")

class login(Resource):
    def put(self):
        global API
        data = request.get_json()
        API = InstagramAPI(data['username'],data['password'])
        API.login()
        #print(API.LastJson)
        if 'invalid_credentials' in API.LastJson :
            return {'login' : False,'message' : API.LastJson['message']}
        return {'login' : True }
class userFeed(Resource):
    def put(self):
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

class userInfo(Resource):
    def get(Self):
        global Api
        API.getProfileData()
        js1 = API.LastJson
        user_Id = js1['user']['pk']
        API.getUsernameInfo(user_Id)
        js2 = API.LastJson
        return {'userData':js1['user'],'userType':js2['user']['category']}

class logOut(Resource):
    def get(Self):
        global API
        API.logout()
        return {"logout":True}

api.add_resource(analyseComments,"/analysecomments")
api.add_resource(getComments,"/getcomments")
api.add_resource(login,"/login")
api.add_resource(userFeed,"/userfeed")
api.add_resource(logOut,"/logout")
api.add_resource(userInfo,"/userinfo")

if __name__ == '__main__':
     app.run(host='127.0.0.1',port=2000)
