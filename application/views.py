from flask import render_template, jsonify, request, Blueprint, url_for, redirect
from flask.views import MethodView
from application.models import Student
from flask_mongoengine.wtf import model_form
import requests
import datetime

surveys = Blueprint('surveys', __name__, template_folder='templates')
cloud = Blueprint('cloud', __name__, template_folder='templates')

class SubmitView(MethodView):

    def get(self):
        StudentForm = model_form(Student, field_args={'sex': {'radio': True}})
        form = StudentForm()
        for field in form:
            print(field)
        return render_template('surveys/submit.html'
                               form=form)

    def post(self):
        StudentForm = model_form(Student, field_args={'sex': {'radio': True}})
        data = request.get_json()
        data['birthday'] = datetime.datetime.strptime(data['birthday'], '%Y-%m-%d')
        if not data:
            response = jsonify({"message": "Expected data to be \
                formated as JSON"})
            response.staus_code = 400
            return response
        else:
            form = StudentForm(**data)
            # for field in form:
            #     print(field)
            if form.validate():
                student = Student(**data)
                student.save()
                response = jsonify(student)
                response.staus_code = 201
                response.headers['Location'] = '/surveyResults/' + \
                    str(student.id)
                return response
            print(form.errors)
            return(jsonify({'message': 'hello'}))



class ListView(MethodView):
    def get(self):
        students = Student.objects()
        return render_template('surveys/list.html',
                               documents=students)


class EditView(MethodView):
    def get(self, _id):
        student = models.Student.objects.get(id=_id)
        return render_template('surveys/edit.html',
                               document=student)


surveys.add_url_rule('/', view_func=SubmitView.as_view('submit'))
surveys.add_url_rule('/surveyResults', view_func=ListView.as_view('list'))
surveys.add_url_rule('/surveyResults/<_id>', view_func=EditView.as_view('edit'))


class CloudView(MethodView):
    def get(self):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        result1 = requests.get('http://api.wunderground.com/api/8dab10257277cb6e/conditions/q/OR/Corvallis.json')
        result2 = requests.get('http://api.wunderground.com/api/8dab10257277cb6e/forecast/q/OR/Corvallis.json')
        weather = result1.json()
        weather.update(result2.json())
        return render_template('cloud.html',
                               time=time,
                               weather=weather)


cloud.add_url_rule('/cloud', view_func=CloudView.as_view('cloud'))
