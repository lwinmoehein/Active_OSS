'''
    from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
'''
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from polls.models import TestModel
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import TestModel,CrimeRecord
from .forms import PersonForm,CrimeRecordForm
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.fonts import addMapping
from .fusioncharts import FusionCharts
import datetime
import json

'''
def index(request):
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace('ndb')
    insert = TestModel(nrc="12/mgdn(naing)123456",labour_id="Hello",marital_status=1,name="ei nghon",race="burmese",religion="muslim")
    insert.save()
    cluster.shutdown()
    return HttpResponse("Hello world")
'''

def index(request):
    return render(request, 'main_base.html')

#return HttpResponse("Hello, world. You're at the polls index.")

def homepage(request):
    return render(request,'homepage.html')

def indexform(request2):
    return render(request2, 'indexform.html')

def indexnewform(request2):
    return render(request2, 'indexnewform.html')

def add_person(request):
    submitted = False
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            print("save")
            return HttpResponseRedirect('/add_person/?submitted=True')
    else:
        form = TestModel()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_person.html', {'form': form, 'submitted': submitted})
#return HttpResponse("DONE")


def get_a_person(request):
    a= [0,1,2,3]
    b= {'a':0,'b':1}
    
    return render( request, 'retrieve_person.html',{'TestModel':list(TestModel.objects.all())})

def delete_a_person(request):
    submitted = False
    if request.method == 'POST':
        aa = request.POST
        c = TestModel.objects.get(nrc=aa.get('nrc'))
        c.delete();
        return HttpResponseRedirect('/delete_a_person/?submitted=True')

    else:
        form = TestModel()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'delete_person.html', {'form': form, 'submitted': submitted})

def request_approval(request):
    submitted = False
    if request.method == 'POST':
        aa = request.POST
        c = TestModel.objects.get(nrc=aa.get('nrc'))

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="desktop/mypdf1.pdf"'
        font_file = 'Pyidaungsu.ttf'
        pdfmetrics.registerFont(TTFont('Pyidaungsu', font_file))
        addMapping('Pyidaungsu', 0, 0, 'Pyidaungsu')
        width, height = defaultPageSize

#actual content
        dateTimeObj = datetime.datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        next_line='\n'
        pdf_content=u"မင်္ဂလာဒုံမြို့နယ်----------------"+next_line+"စာအမှတ်၊     1/သဃအ-ရကအ/၂၀ -------------\nရက်စွဲ၊"+timestampStr+'\n------------------အကြောင်းအရာ။    ထောက်ခံချက်--------------------------------------------------- \n\n'+c.township+'..မြို့နယ်၊..'+c.ward+'..ကျေးရွာ..'+c.street+'လမ်း၊'+'  '+c.home_no+'အမှတ် ..'+'  '+'တွင်နေထိုင်သော (အဘ)ဦး'+c.father_name+'၏ ...သား/သမီးဖြစ်သူ မောင်/မ'+c.name +' ... နိုင်ငံသားစိစစ်ရေးကဒ်ပြားအမှတ်'+c.nrc + '...ကိုင်သောသူသည် ကျေးရွာအုပ်စုအတွင်း...အမှန်တကယ်နေထိုင်ကြောင်းကို...အပိုင်ဆယ်အိမ်မှူး/ရာအိမ်မှူး ၏ထောက်ခံချက်အရ ...မှန်ကန်ကြောင်း ထပ်ဆင့်ထောက်ခံအပ်ပါသည်။'
        pdf_content.replace("\n", "<br />")

        styles = getSampleStyleSheet()
        styles["Title"].fontName = 'Pyidaungsu'
        para = Paragraph(pdf_content, styles["Title"])
        canv = canvas.Canvas('test_mm_font1.pdf')

        para.wrap(width, height)
        para.drawOn(canv, 0, height/2)

        canv.showPage()
        canv.save()
    
        return response
    
    else:
        form = TestModel()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'request_approval.html', {'form': form, 'submitted': submitted})

def update_person(request):
    submitted = False
    if request.method == 'POST':
        form = PersonForm(request.POST)
        aa = request.POST
        c = TestModel.objects.get(nrc=aa.get('nrc'))
    #    c.labour_id=aa.get('attribute')

        attribute=aa.get('attribute')
        setattr(c, attribute, aa.get('value'))
        c.save();
        return HttpResponseRedirect('/update_person/?submitted=True')

    else:
        form = TestModel()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'update_person.html', {'form': form, 'submitted': submitted})


#pdf generation testing
def request_crime_record(request):
    submitted = False
    if request.method == 'POST':
        aa = request.POST

        c = CrimeRecord.objects.get(criminal_nrc=aa.get('nrc'))
        #totalcrime=CrimeRecord.objects.get(criminal_nrc=aa.get('nrc')).count()
        totalcount=CrimeRecord.objects.count()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="desktop/mypdf1.pdf"'
        font_file = 'Pyidaungsu.ttf'
        pdfmetrics.registerFont(TTFont('Pyidaungsu', font_file))
        addMapping('Pyidaungsu', 0, 0, 'Pyidaungsu')
        width, height = defaultPageSize

    #actual content
        dateTimeObj = datetime.datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        c = CrimeRecord.objects.get(criminal_nrc=aa.get('nrc'))
        totalcount=CrimeRecord.objects.filter(criminal_nrc=aa.get('nrc')).count()
      
        if (totalcount>0):
            next_line='\n'
            totalcount_str=str(totalcount)
            pdf_content=u"မြို့နယ်----------------"+next_line+"စာအမှတ်၊     1/သဃအ-ရကအ/၂၀ -------------\nရက်စွဲ၊"+timestampStr+'\n------------------အကြောင်းအရာ။    ထောက်ခံချက်--------------------------------------------------- \n\n'+c.township+'..မြို့နယ်၊..'+c.ward+'..ကျေးရွာ..'+c.street+'လမ်း၊'+'  '+c.number+'အမှတ် ..'+'  '+'တွင်နေထိုင်သော (အဘ)ဦး'+c.tayalo_name+'၏ ...သား/သမီးဖြစ်သူ မောင်/မ'+c.criminal_name +' ... နိုင်ငံသားစိစစ်ရေးကဒ်ပြားအမှတ်'+c.criminal_nrc + '...ကိုင်သောသူသည် ကျေးရွာအုပ်စုအတွင်း...အမှန်တကယ်နေထိုင်ကြောင်းကို...အပိုင်ဆယ်အိမ်မှူး/ရာအိမ်မှူး ၏ထောက်ခံချက်အရ ...မှန်ကန်ကြောင်း ထပ်ဆင့်ထောက်ခံအပ်ပါသည်။'
            pdf_content.replace("\n", "<br />")

            styles = getSampleStyleSheet()
            styles["Title"].fontName = 'Pyidaungsu'
            para = Paragraph(pdf_content, styles["Title"])
            canv = canvas.Canvas('test_mm_font1.pdf')

            para.wrap(width, height)
            para.drawOn(canv, 0, height/2)

            canv.showPage()
            canv.save()

        else:
            
            next_line='\n'
            pdf_content=u"မင်္ဂလာဒုံမြို့နယ်----------------"+next_line+"စာအမှတ်၊     1/သဃအ-ရကအ/၂၀ -------------\nရက်စွဲ၊"+timestampStr+'\n------------------အကြောင်းအရာ။    ထောက်ခံချက်--------------------------------------------------- \n\n'+c.township+'..မြို့နယ်၊..'+c.ward+'..ကျေးရွာ..'+c.street+'လမ်း၊'+'  '+c.number+'အမှတ် ..'+'  '+'တွင်နေထိုင်သော (အဘ)ဦး'+c.tayalo_name+'၏ ...သား/သမီးဖြစ်သူ မောင်/မ'+c.tayalo_name +' ... နိုင်ငံသားစိစစ်ရေးကဒ်ပြားအမှတ်'+c.criminal_nrc + '...ကိုင်သောသူသည် ကျေးရွာအုပ်စုအတွင်း...အမှန်တကယ်နေထိုင်ကြောင်းကို...အပိုင်ဆယ်အိမ်မှူး/ရာအိမ်မှူး ၏ထောက်ခံချက်အရ ...မှန်ကန်ကြောင်း ထပ်ဆင့်ထောက်ခံအပ်ပါသည်။'
            pdf_content.replace("\n", "<br />")

            styles = getSampleStyleSheet()
            styles["Title"].fontName = 'Pyidaungsu'
            para = Paragraph(pdf_content, styles["Title"])
            canv = canvas.Canvas('test_mm_font1.pdf')

            para.wrap(width, height)
            para.drawOn(canv, 0, height/2)

            canv.showPage()
            canv.save()    
           

        return response
    
    else:
        form = TestModel()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'request_approval.html', {'form': form, 'submitted': submitted})

    '''

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="desktop/mypdf.pdf"'
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        
        # Start writing the PDF here
        x=300
        y=300
        test = u'こんにちは'
        p.drawString(100,500,test.encode('utf-8'))
        for i in list(TestModel.objects.all()):
        
        p.drawString(x, y,i.nrc)
        x=x+10
        y=y+10
        # End writing
        
        p.showPage()
        p.save()
        
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        
        return response
    
    
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="desktop/mypdf.pdf"'
    width, height = defaultPageSize
    pdf_content = "It's emoji time \u263A \U0001F61C. Let's add some cool emotions \U0001F48F \u270C. And some more \u2764 \U0001F436"
    
    styles = getSampleStyleSheet()
    para = Paragraph(pdf_content, styles["Title"])
    canv = canvas.Canvas('emoji.pdf')
    
    para.wrap(width, height)
    para.drawOn(canv, 0, height/2)
    
    canv.save()
    response.write(canv)
    
    return response
    
    '''
def data_visualization(request):

  #  totalcount=list(TestModel.objects.get(ward='စမ်းကြီးဝ'))

    totalcount_gent=TestModel.objects.filter(gender='ကျား').count()
    totalcount_lady=TestModel.objects.filter(gender='မ').count()

    total_teacher=TestModel.objects.filter(occupation='ျောင်းဆရာမ').count()
    total_merchant=TestModel.objects.filter(occupation='ကုန်သည်').count()
    total_engineer=TestModel.objects.filter(occupation='အင်ဂျင်နီယာ').count()
    total_unpaid=TestModel.objects.filter(occupation='မှီခို').count()
    total_doctor=TestModel.objects.filter(occupation='ဆရာဝန်').count()

    total_buddhist=TestModel.objects.filter(religion='ဗုဒ္').count()
    total_christian=TestModel.objects.filter(religion='ခရစ်ယာန်').count()
    total_islam=TestModel.objects.filter(religion='အစ္စလာမ်').count()


    b=5000
    religion_json_string=json.dumps({'chart':{ "caption": "Data chart based on religion","subCaption" : "for all population in database", "showValues":"1","showPercentInTooltip" : "0","numberPrefix" : "","enableMultiSlicing":"1","theme": "fusion"},'data':[{ "label": "buddist","value": total_buddhist},{"label": "Hindu","value": 50},{"label": "christian","value":total_christian },{"label": "Islam","value": total_islam}]})
    occupation_json_string=json.dumps({'chart':{ "caption": "Data chart based on occupation","subCaption" : "for all population in database", "showValues":"1","showPercentInTooltip" : "0","numberPrefix" : "","enableMultiSlicing":"1","theme": "fusion"},'data':[{ "label": "teacher","value": total_teacher},{"label": "marchant","value": total_merchant},{"label": "engineer","value": total_engineer},{"label": "unpaid job","value": total_unpaid}]})
    gender_json_string=json.dumps({'chart':{ "caption": "Data chart based on gender","subCaption" : "for all population in database", "showValues":"1","showPercentInTooltip" : "0","numberPrefix" : "","enableMultiSlicing":"1","theme": "fusion"},'data':[{ "label": "Male","value": totalcount_gent},{"label": "Female","value": totalcount_lady}]})
    # Create an object for the column2d chart using the FusionCharts class constructor
    gender_pie3d = FusionCharts("pie3d", "ex1" , "100%", "400", "chart-1", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                        gender_json_string)
    occupation_chart=FusionCharts("column2D", "ex2" , "100%", "400", "chart-2", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                        occupation_json_string)
    religion_chart=FusionCharts("pie3d", "ex3" , "100%", "400", "chart-3", "json",
                         # The data is passed as a string in the `dataSource` as parameter.
                        religion_json_string)
    # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
    return render(request, 'data_visualization.html', {'output' : gender_pie3d.render(),'output2':occupation_chart.render(),'output3':religion_chart.render()})



def register_crime_record(request):
    submitted = False
    if request.method == 'POST':
        form = CrimeRecordForm(request.POST)
        if form.is_valid():
            form.save()
            print("save")
            return HttpResponseRedirect('/register_crime_record/?submitted=True')
    else:
        form = CrimeRecord()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'crime_record.html', {'form': form, 'submitted': submitted})

