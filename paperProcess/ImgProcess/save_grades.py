# -*-coding:utf-8-*-
import requests
import json
def saveGrades(coursesId,teacherNum,grades):
	r = requests.post(
		url='http://localhost/paper/SaveAIGrades',
		headers={"Content-Type": "application/x-www-form-urlencoded"},
		data={'courseId': coursesId,'teacherNum':teacherNum,'grades':json.dumps(grades)})
	return r.text