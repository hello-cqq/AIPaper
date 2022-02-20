# -*-coding:utf-8-*-
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import os
from ImgProcess import grade,save_grades
from paperProcess import settings
# Create your views here.

def getPaperImg(request):
    try:
        img = request.FILES.get('file')
        imgPath = settings.MEDIA_ROOT + '/paper/' + \
            request.POST.get('imgPath') + '/origin/' + img.name
        if not os.path.exists(imgPath):
            default_storage.save(imgPath, ContentFile(img.read()))
        return HttpResponse(json.dumps({'status': 'success'}))
    except:
        return HttpResponse(json.dumps({'status': 'error'}))


def startImgProcess(request):
    try:
        # 'D:/workspace/pycharm/paperProcess/media/paper/'
        uploadImgDir = settings.MEDIA_ROOT + '/paper/' + request.POST.get('uploadPath')+'/origin'
        processedImgDir = settings.MEDIA_ROOT + '/paper/' + request.POST.get('uploadPath')+'/processed'
        courseId = request.POST.get('courseId')
        teacherNum = request.POST.get('teacherNum')
        grades = grade.getGrades(uploadImgDir,processedImgDir,'/media/paper/'+ request.POST.get('uploadPath')+ '/processed')
        result = save_grades.saveGrades(courseId,teacherNum,grades)
        return HttpResponse(json.dumps(result))
    except:
        return HttpResponse(json.dumps({'status': 'error'}))
