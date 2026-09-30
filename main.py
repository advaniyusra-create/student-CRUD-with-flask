from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

app = Flask(__name__) 

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Student(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String, nullable = False)
    age=db.Column(db.Integer, nullable = True)

class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return "<p>hiiiii, Hello, World!</p>"

@app.route("/students", methods = ["POST"])
def add_student():
  student_details = request.get_json()
  student=Student(name=student_details["name"], age=student_details["age"])
  db.session.add(student)
  db.session.commit()
  return {'Message': 'Succesfully Added yayayy'}

@app.route("/students", methods = ["GET"])
def get_all_students_data():
  students = Student.query.all()
  print('yusra')
  return students_schema.dump(students)

@app.route("/students/<int:student_id>", methods = ["GET"])
def get_student(student_id):
  student = Student.query.all(student_id)
  return student_schema.dump(student)

@app.route("/students/<int:student_id>", methods = ["PUT"])
def update_student(student_id):
    student = Student.query.get(student_id)

    updated_details = request.get_json()
    if updated_details.get("name"):
        student.name = updated_details.get("name")

    if updated_details.get("age"):
        student.age = updated_details.get("age")

    db.session.commit()
    
    return {'Message': 'Succesfully Updated yayyy'}

@app.route("/students/<int:student_id>", methods = ["DELETE"])
def delete_student(student_id):
    student = Student.query.get(student_id)

    db.session.delete(student)
    db.session.commit()
    
    return {'Message': 'Succesfully Deleted yayyy'}

if __name__=="__main__":
    app.run(debug = True)