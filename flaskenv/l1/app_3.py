from flask import Flask,jsonify,request
from flask_restful import Resource,Api

app = Flask(__name__)
api = Api(app)


class Helloworld(Resource):
    def get(self):
        return {'about':'hello world'}

    def post(self):
        Some_json = request.get_json()
        return {'you sent ':Some_json},201


class Multi(Resource):
    def get(self,name:str):
        return {'your name is ':name}


api.add_resource(Helloworld,'/')
api.add_resource(Multi,'/multi/<string:name>')


if __name__ == '__main__':
    app.run(debug=True)
