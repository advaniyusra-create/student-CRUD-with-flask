from flask import Flask, jsonify, request

app = Flask(__name__)

students = [
    {"id":1,"name":"Sarfraz", "age":30},
    {"id":2,"name":"Afsar", "age":25},
    {"id":3,"name":"Ali", "age":26}
]

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/students", methods=["GET"])
def get_all_students_data():
    return jsonify(students)

@app.route("/students/<int:student_id>", methods = ["GET"])
def get_student(student_id):
  for details in students:
    if details['id'] == student_id:
      return details
  return 'Student not found'

@app.route("/students", methods = ["POST"])
def add_student():
  student_details = request.get_json()
  new_student_id = students[-1]['id']+1
  student_details['id'] = new_student_id
  students.append(student_details)
  return 'Student data successfully added'

@app.route("/students/<int:student_id>", methods = ["PUT"])
def update_student(student_id):
  update_student_details=request.get_json()
  for details in students:
    if details['id'] == student_id:
      if update_student_details.get('name'):
        details['name'] = update_student_details.get("name")
      if update_student_details.get("age"):
        details['age'] = update_student_details.get("age")
      return 'Student data successfully updated'

  return 'Student not found'

@app.route("/students/<int:student_id>", methods = ["DELETE"])
def delete_student_data(student_id):
  for details in students:
    if details['id'] == student_id:
      students.remove(details)
      return 'Succesfully Deleted'
  return 'Student not found'

if __name__=="__main__":
    app.run(debug = True)