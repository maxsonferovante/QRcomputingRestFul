#!flask/bin/python
from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__, static_url_path="")
api = Api(app )
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'mferovante':

        return 'd06fe49d20cb218e662fd0e034ef8387'

    return None

@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

students = [
    {
        "id": 1,
        "name":u"Maxson Almeida Ferovante",
        "done":False
    },
    {
        "id": 2,
        "name":u"Ariane Cristina Sanches Ladeira",
        "done":False
    },
    {
        "id":3,
        "name":u"Alan Dias Almeida",
        "done":False
    },
    {
        "id":4,
        "name":u"Rafael Almeida Campos",
        "done":False
    },
    {
        "id":5,
        "name":u"Vinicius Almeida Campos",
        "done":False
    },
    {
        "id":6,
        "name":u"Richard Mauro Siqueira",
        "done":False
    },
    {
        "id":7,
        "name":u"Felipe Pereira Ramos",
        "done":False
    }
]

student_fields = {
    "name":fields.String,
    'done': fields.Boolean,
    "uri" : fields.Url("student")
}

class StudentListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='name for your student.',
                                   location='json')

        super(StudentListAPI, self).__init__()

    def get(self):
        return jsonify([marshal(student,student_fields) for student in students])


    def post(self):
        args = self.reqparse.parse_args()
        student = {
            "id" :students[-1]["id"] + 1,
            "name" : args["name"],
            "done" : False

        }
        students.append(student)
        return {'student': marshal(student, student_fields)}, 201

class StudentAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str,
                                   help = "name for your student.",
                                   location='json')
        self.reqparse.add_argument('done', type=bool, location='json')

        super(StudentAPI, self).__init__()

    def get(self,id):
        student = [student for student in students if student["id"] == id]
        if len(student) == 0:
            abort(404)
        return {'student':marshal(student[0], student_fields)}

    def put(self, id):
        student= [student for student in students if student['id'] == id]
        if len(student) == 0:
            abort(404)
        student = student[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                student[k] = v
        return {'student': marshal(student, student_fields)}

    def delete(self, id):
        student = [student for student in students if student['id'] == id]
        if len(student) == 0:
            abort(404)
        students.remove(student[0])
        return {'result': True}

class Welcome(Resource):
    def get(self):
        return "Welcome WebService QR Computing"

api.add_resource(Welcome,"/")
api.add_resource(StudentListAPI,'/computing/api/v1.0/students', endpoint ="students")
api.add_resource(StudentAPI,'/computing/api/v1.0/students/<int:id>', endpoint ="student")


if __name__ == '__main__':
    app.run(host = "192.168.1.6", port ="5000")
