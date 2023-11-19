import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "Student.sqlite3")
db = SQLAlchemy(app)
class Student(db.Model):
  __tablename__ = 'Student'
  student_id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
  full_name = db.Column(db.String(50))
  age = db.Column(db.Integer)
  dateofbirth = db.Column(db.String(50))
  stuclass = db.Column(db.String(50))
  percentage = db.Column(db.Integer)
  grade=db.Column(db.String(50))
  def __init__(self,student_id,full_name, age, dateofbirth, stuclass, percentage,grade):
    self.student_id=student_id
    self.full_name = full_name
    self.age = age
    self.dateofbirth = dateofbirth
    self.stuclass = stuclass
    self.percentage = percentage
    self.grade=grade
class Course(db.Model):
  __tablename__='Marks'
  student_id=db.Column(db.Integer(),primary_key=True)
  maths=db.Column(db.Integer)
  english=db.Column(db.Integer)
  tamil=db.Column(db.Integer)
  science=db.Column(db.Integer)
  social=db.Column(db.Integer)
  def __init__(self, student_id, maths, english, tamil, science, social):
    self.student_id = student_id
    self.maths = maths
    self.english = english
    self.tamil = tamil
    self.science = science
    self.social = social
#home page
@app.route("/", methods=["GET", "POST"])
def main():
  astudent = Student.query.filter_by(stuclass="A").all()
  bstudent = Student.query.filter_by(stuclass="B").all()
  cstudent = Student.query.filter_by(stuclass="C").all()
  if len(astudent) != 0 or len(bstudent) != 0 or len(cstudent) != 0:
    return render_template("home.html",astudent=astudent,bstudent=bstudent,cstudent=cstudent)
  else:
    return render_template("empty.html")
#getting and recording the details
@app.route("/form", methods=["GET", "POST"])
def form():
  if request.method == "GET":
    return render_template("form.html")
  elif request.method == "POST":
    studid=request.form["sid"]
    name = request.form["name"]
    age = request.form["age"]
    dob=request.form["dob"]
    stuclass=request.form["stuclass"]
    mathsmark = request.form["maths"]
    englishmark=request.form["english"]
    sciencemark=request.form["science"]
    socialmark=request.form["social"]
    tamilmark=request.form["tamil"]
    percentage=(int(mathsmark)+int(englishmark)+int(sciencemark)+int(socialmark)+int(tamilmark))/5
    grade="A+" if percentage>90 else "A" if percentage>80 else "B" if percentage>70 else "c" if percentage>60 else "D" if percentage>50 else "F" 
    a = Student.query.filter_by(student_id=studid).first()

    if a  is None:
      squidward = Student(student_id=studid,full_name=name,age=age,dateofbirth=dob,
                          stuclass=stuclass,percentage=percentage,grade=grade)
      squidward2=Course(student_id=studid,maths=mathsmark,english=englishmark,science=sciencemark,tamil=tamilmark,social=socialmark)
      db.session.add(squidward)
      db.session.add(squidward2)
      db.session.commit()
      astudent = Student.query.filter_by(stuclass="A").all()
      bstudent = Student.query.filter_by(stuclass="B").all()
      cstudent = Student.query.filter_by(stuclass="C").all()
      return render_template("home.html",astudent=astudent,bstudent=bstudent,cstudent=cstudent) 
    else:
      return render_template("alreadyexisit.html")
#display each individual profile
@app.route("/student/<int:student_id>",methods=["GET"])
def studentdetail(student_id):
  student=Student.query.filter_by(student_id=student_id).first()
  return render_template("studentdetail.html",student=student)
#display each individual mark
@app.route("/mark/<int:student_id>",methods=["GET"])
def markdetail(student_id):
  mark=Course.query.filter_by(student_id=student_id).first()
  return render_template("markdetail.html",mark=mark)
#Deleting a record
@app.route("/student/<int:student_id>/delete",methods=["GET"])
def delete(student_id):
  s=Student.query.filter_by(student_id=student_id).first()
  c=Course.query.filter_by(student_id=student_id).first()
  db.session.delete(s)
  db.session.delete(c)
  db.session.commit()
  astudent = Student.query.filter_by(stuclass="A").all()
  bstudent = Student.query.filter_by(stuclass="B").all()
  cstudent = Student.query.filter_by(stuclass="C").all()
  return render_template("home.html",astudent=astudent,bstudent=bstudent,cstudent=cstudent)
#update details
@app.route("/student/<int:student_id>/update",methods=["GET","POST"])
def update(student_id):
  if request.method == "GET":
    student=Student.query.filter_by(student_id=student_id).first()
    return render_template("update.html",student=student)
  elif request.method == "POST":
    student=Student.query.filter_by(student_id=student_id).first()
    student.full_name=request.form["name"]
    student.age=request.form["age"]
    student.dateofbirth=request.form["dob"]
    student.stuclass=request.form["stuclass"]
    
    course=Course.query.filter_by(student_id=student_id).first()
    course.maths=request.form["maths"]
    course.english=request.form["english"]
    course.science=request.form["science"]
    course.social=request.form["social"]
    course.tamil=request.form["tamil"]
    percentage=(int(course.maths)+int(course.english)+int(course.science)+int(course.social)+int(course.tamil))/5
    student.percentage=percentage
    student.grade="A+" if percentage>90 else "A" if percentage>80 else "B" if percentage>70 else "c" if percentage>60 else "D" if percentage>50 else "F" 
    db.session.commit()
    astudent = Student.query.filter_by(stuclass="A").all()
    bstudent = Student.query.filter_by(stuclass="B").all()
    cstudent = Student.query.filter_by(stuclass="C").all()
    return render_template("home.html",astudent=astudent,bstudent=bstudent,cstudent=cstudent)
#filtering by class
@app.route("/classa/filter",methods=["GET","POST"])
def filtera():
  astudent = Student.query.filter_by(stuclass="A").all()
  return render_template("home.html",astudent=astudent)
@app.route("/classb/filter",methods=["GET","POST"])
def filterb():
  bstudent = Student.query.filter_by(stuclass="B").all()
  return render_template("home.html",bstudent=bstudent)
@app.route("/classc/filter",methods=["GET","POST"])
def filterc():
  cstudent = Student.query.filter_by(stuclass="C").all()
  return render_template("home.html",cstudent=cstudent)
@app.route("/student/search",methods=["GET"])
def search():
  search=request.args.get("search")
  cstudent = Student.query.filter_by(full_name=search).first()
  if cstudent.stuclass=="A":
    return render_template("home.html",astudent=cstudent)
  elif cstudent.stuclass=="B":
    return render_template("home.html",bstudent=cstudent)
  else:
    temp=[cstudent]
    return render_template("home.html",cstudent=temp)

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81,debug=True)
