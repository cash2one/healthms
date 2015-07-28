# encoding: utf8
import MySQLdb
from werkzeug.utils import secure_filename
from flask import Flask, g, request, render_template, abort, url_for, jsonify, session, redirect
import sys, logging, StringIO, time, datetime, json, base64, random

import check_code

from sae.storage import Bucket

# 从 SAE 中导入 MYSQL 配置参数
from sae.const import (MYSQL_HOST, MYSQL_HOST_S,
    MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
)

# 把 str 编码由 ascii 改为 utf8
reload(sys)
sys.setdefaultencoding('utf8')

# 生成 Flask 类
app = Flask(__name__)
# 设置网站是否为 DEBUG 模式
app.debug = True

# 静态资源路径
# STATIC_CSS_PATH = '/static/bootstrap/dist/css'
# STATIC_JS_PATH = '/static/bootstrap/dist/js'
# STATIC_JQ_PATH = '/static/jquery/dist'

# 设置网站 Title
PROJECT_NAME = u'中医健康管理平台'

# 设置 测试名称 列表
# TEST_NAMES = [u'中医基本体质分类', u'常见身心症状自评', u'生活质量', u'特质应对',u'抑郁症状自评']
TEST_NAMES = [u'中医基本体质分类', u'常见身心症状自评']

USER_TYP = [u'patient', u'doctor', u'admin']

INFO_TYP = [u'健康新资讯', u'中医疗法介绍']

WEB_INFOS = {'PROJECT_NAME': PROJECT_NAME, 'TEST_NAMES': TEST_NAMES, 'USER_TYP': USER_TYP, 'INFO_TYP': INFO_TYP}

CAROUSEL_TYP = ['jpg', 'jpeg', 'JPEG', 'JPG', 'png', 'PNG']

# 设置会话密钥
app.secret_key = '\xb7Y\x9a\xbb\xdcH\xb8[\xa7[\xe8:\xfa\xac\t\xf5\x89\xb0\x8e\xc9H\xeb\x08\xd2'



# 连接数据库
@app.before_request
def before_request():
    ''' 连接数据库 '''
    g.db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS,
                           MYSQL_DB, port=int(MYSQL_PORT), charset="utf8")
    # c = g.db.cursor()
    # c.execute("SET NAMES utf8");
    # g.db.commit();

# 关闭数据库
@app.teardown_request
def teardown_request(exception):
    '''关闭数据库'''
    if hasattr(g, 'db'): g.db.close()

# 首页
@app.route('/', methods=['GET'])
def index():
    c = g.db.cursor()
    c.execute('SELECT * FROM healthms_info WHERE info_type = "健康新资讯" ORDER BY info_edit_date DESC LIMIT 9')
    infoNews = list(c.fetchall())
    c.execute('SELECT * FROM healthms_info WHERE info_type = "中医疗法介绍" ORDER BY info_edit_date DESC LIMIT 9')
    infoMedicine = list(c.fetchall())
    c.execute('SELECT * FROM healthms_friend_link ORDER BY friend_link_date DESC')
    friendLink = list(c.fetchall())
    c.execute('SELECT * FROM healthms_carousel_img ORDER BY carousel_img_date DESC')
    carouselImg = list(c.fetchall())

    c.execute('SELECT b.* FROM (SELECT doctor_id, COUNT(doctor_id) AS answer_num FROM healthms_ask_answer_doctors ORDER BY answer_num LIMIT 3) AS a RIGHT JOIN healthms_doctors_info AS b ON a.doctor_id = b.doctor_id WHERE b.doctor_check = 2')
    doctors = list(c.fetchall())
    infoDict = {'infoNews': infoNews, 'infoMedicine': infoMedicine, 'friendLink': friendLink, 'carouselImg': carouselImg, 'doctors': doctors}
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        return render_template('index.html', patientInfo = patientInfo, WEB_INFOS = WEB_INFOS, infoDict = infoDict)
    elif 'doctorEmail' in session:
        doctorInfo = get_doctor_info_session()
        return render_template('index.html', doctorInfo = doctorInfo, WEB_INFOS = WEB_INFOS, infoDict = infoDict)
    return render_template('index.html', WEB_INFOS = WEB_INFOS, infoDict = infoDict)

# 文章列表
@app.route('/info/list/<infoTyp>')
def info_list(infoTyp):
    c = g.db.cursor()
    c.execute('SELECT * FROM healthms_info WHERE info_type = "' + infoTyp + '" ORDER BY info_edit_date DESC')
    infos = list(c.fetchall())
    infoHot = sorted(infos, key=lambda item:item[4], reverse=True)[:5]
    infoDict = {'infoTyp': infoTyp, 'infos':infos, 'infoHot': infoHot}
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        return render_template('info_list.html', patientInfo = patientInfo, WEB_INFOS = WEB_INFOS, infoDict = infoDict)
    elif 'doctorEmail' in session:
        doctorInfo = get_doctor_info_session()
        return render_template('info_list.html', doctorInfo = doctorInfo, WEB_INFOS = WEB_INFOS, infoDict = infoDict)
    return render_template('info_list.html', WEB_INFOS = WEB_INFOS, infoDict=infoDict)

# 文章正文
@app.route('/info/<int:articleId>')
def info(articleId):
    c = g.db.cursor()
    c.execute('SELECT * FROM healthms_info WHERE info_id = ' + str(articleId))
    info = list(c.fetchall())[0]
    # 处理 文章热度  当 session 中没有文章 id 时，文章热度+1
    aSession = 'article' + str(articleId)
    if not aSession in session:
        c.execute('UPDATE healthms_info SET info_hot = ' + str(info[4]+1) + ' WHERE info_id = ' + str(articleId))
        session[aSession] = True
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        return render_template('info.html', patientInfo = patientInfo, WEB_INFOS = WEB_INFOS, info=info)
    elif 'doctorEmail' in session:
        doctorInfo = get_doctor_info_session()
        return render_template('info.html', doctorInfo = doctorInfo, WEB_INFOS = WEB_INFOS, info=info)
    return render_template('info.html', WEB_INFOS = WEB_INFOS, info=info)

# 医生列表
@app.route('/list/doctors', methods=['GET'])
def list_doctors():
    c = g.db.cursor()
    c.execute('SELECT b.*, a.* FROM (SELECT doctor_id, COUNT(doctor_id) AS answer_num FROM healthms_ask_answer_doctors ORDER BY answer_num) AS a RIGHT JOIN healthms_doctors_info AS b ON a.doctor_id = b.doctor_id WHERE b.doctor_check = 2')
    doctors = list(c.fetchall())
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        return render_template('list_doctors.html', patientInfo = patientInfo, WEB_INFOS = WEB_INFOS, doctors=doctors)
    elif 'doctorEmail' in session:
        doctorInfo = get_doctor_info_session()
        return render_template('list_doctors.html', doctorInfo = doctorInfo, WEB_INFOS = WEB_INFOS, doctors=doctors)
    return redirect(url_for('login', userTyp=USER_TYP[0]))

# 医生详细页面
@app.route('/detail/doctors/<int:doctorId>', methods=['GET'])
def detail_doctors(doctorId):
    c = g.db.cursor()
    c.execute('SELECT * FROM healthms_doctors_info WHERE doctor_check = 2 AND doctor_id = %s', [doctorId])
    doctor = list(c.fetchall())[0]
    c.execute('SELECT ask_doctor_cardinal_symptom, ask_doctor_date FROM healthms_ask_answer_doctors AS a INNER JOIN healthms_ask_form AS b ON a.ask_doctor_id = b.ask_doctor_id WHERE a.doctor_id = %s', [doctorId])
    hasAskForms = list(c.fetchall())
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        return render_template('detail_doctors.html', patientInfo = patientInfo, WEB_INFOS = WEB_INFOS, doctor=doctor, hasAskForms = hasAskForms)
    elif 'doctorEmail' in session:
        doctorInfo = get_doctor_info_session()
        return render_template('detail_doctors.html', doctorInfo = doctorInfo, WEB_INFOS = WEB_INFOS, doctor=doctor, hasAskForms = hasAskForms)
    return redirect(url_for('login', userTyp=USER_TYP[0]))

# 登录页面
@app.route('/login/<userTyp>', methods=['GET', 'POST'])
def login(userTyp):
    if request.method == 'GET':
        if 'patientEmail' in session:
            return redirect(url_for('patient_index'))
        elif 'doctorEmail' in session:
            return redirect(url_for('index'))
        return render_template('login.html', WEB_INFOS = WEB_INFOS, userTyp=userTyp)
    else:
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        if userTyp == 'patient':
            result = valid_login(email, password, userTyp)
            if result['result'] == 'success':
                set_patient_info_session(result['userInfo'])
                return jsonify(result = 'success', typ = userTyp)
            elif result['result'] == 'pwdError' or result['result'] == 'emailError':
                return jsonify(result = result['result'], typ = userTyp)
            else:
                abort(404)
        elif userTyp == 'doctor':
            result = valid_login(email, password, userTyp)
            if result['result'] == 'success':
                set_doctor_info_session(result['userInfo'])
                return jsonify(result = 'success', typ = userTyp)
            elif result['result'] == 'pwdError' or result['result'] == 'emailError' or result['result'] == 'notCheck' or result['result'] == 'checkFailed':
                return jsonify(result = result['result'], typ = userTyp)
            else:
                abort(404)
        else:
            abort(404)

# 用户注册页面
@app.route('/register/<userTyp>', methods=['GET', 'POST'])
def register(userTyp):
    if request.method == 'GET':
        if userTyp == 'patient':
            return render_template('patient_register.html', WEB_INFOS = WEB_INFOS)
        elif userTyp == 'doctor':
            return render_template('doctor_register.html', WEB_INFOS = WEB_INFOS)
        else:
            abort(404)
    else:
        registerTime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        if userTyp == USER_TYP[0]:
            patientRegEmail = request.form['patientRegEmail'].strip()
            patientRegPassword = base64.encodestring(request.form['patientRegPassword'].strip())
            patientRegName = request.form['patientRegName'].strip()
            patientRegProvince = request.form['patientRegProvince']
            patientRegCity = request.form['patientRegCity']
            patientRegCounty = request.form['patientRegCounty']
            patientRegGender = request.form['patientRegGender']
            patientRegBirthday = request.form['patientRegBirthday'].strip()
            patientRegTel = request.form['patientRegTel'].strip()
            patientRegProfession = request.form['patientRegProfession'].strip()
            patientRegNation = request.form['patientRegNation']
            patientRegMarried = request.form['patientRegMarried']
            patientRegAddress = request.form['patientRegAddress'].strip()

            c = g.db.cursor()
            c.execute("INSERT INTO healthms_patients_info (patient_email, patient_password, patient_name, patient_province, patient_city, patient_county, patient_gender, patient_birthday, patient_tel, patient_profession, patient_nation, patient_married, patient_address, patient_register_date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [patientRegEmail, patientRegPassword, patientRegName, patientRegProvince, patientRegCity, patientRegCounty, patientRegGender, patientRegBirthday, patientRegTel, patientRegProfession, patientRegNation, patientRegMarried, patientRegAddress, registerTime])

            userInfo = [g.db.insert_id(), patientRegEmail,'', patientRegName, patientRegProvince, patientRegCity, patientRegCounty, patientRegGender, patientRegBirthday, patientRegTel, patientRegProfession, patientRegNation, patientRegMarried, patientRegAddress, registerTime, registerTime]
            set_patient_info_session(userInfo)

            return redirect(url_for('index'))
        elif userTyp == USER_TYP[1]:
            doctorRegEmail = request.form['doctorRegEmail'].strip()
            doctorRegPassword = base64.encodestring(request.form['doctorRegPassword'].strip())
            doctorRegName = request.form['doctorRegName'].strip()
            doctorRegGender = request.form['doctorRegGender']
            doctorRegBirthday = request.form['doctorRegBirthday'].strip()
            doctorRegCheckTelCode = request.form['doctorRegCheckTelCode'].strip()
            doctorRegCheckTel = request.form['doctorRegCheckTel'].strip()
            doctorRegTel = request.form['doctorRegTel'].strip()
            doctorRegProvince = request.form['doctorRegProvince']
            doctorRegCity = request.form['doctorRegCity']
            doctorRegCounty = request.form['doctorRegCounty']
            doctorRegHospitalName = request.form['doctorRegHospitalName'].strip()
            doctorRegOffices = request.form['doctorRegOffices'].strip()
            doctorRegProfessional = request.form['doctorRegProfessional']
            doctorRegJob = request.form['doctorRegJob'].strip()
            doctorRegSpecialty = request.form['doctorRegSpecialty'].strip()

            doctorRegCheckTel = str(doctorRegCheckTelCode) + '-' + str(doctorRegCheckTel)

            c = g.db.cursor()
            c.execute("INSERT INTO healthms_doctors_info (doctor_email, doctor_password, doctor_name, doctor_gender, doctor_birthday, doctor_check_tel, doctor_tel, doctor_province, doctor_city, doctor_county, doctor_hospital_name, doctor_offices, doctor_professional, doctor_job, doctor_specialty, doctor_img, doctor_check, doctor_register_date) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [doctorRegEmail, doctorRegPassword, doctorRegName, doctorRegGender, doctorRegBirthday, doctorRegCheckTel, doctorRegTel, doctorRegProvince, doctorRegCity, doctorRegCounty, doctorRegHospitalName, doctorRegOffices, doctorRegProfessional, doctorRegJob, doctorRegSpecialty, url_for('static', filename='images/user.png') , '0', registerTime])

            return redirect(url_for('index'))
        else:
            abort(404)

@app.route('/edit/user/info/<userTyp>', methods=['GET', 'POST'])
def user_edit_info(userTyp):
    if request.method == 'GET':
        if userTyp == USER_TYP[0]:
            if 'patientEmail' in session:
                patientInfo = get_patient_info_session()
                return render_template('patient_edit_info.html', WEB_INFOS = WEB_INFOS, patientInfo = patientInfo)
            else:
                return redirect(url_for('login', userTyp=userTyp))
        elif userTyp == USER_TYP[1]:
            if 'doctorEmail' in session:
                doctorInfo = get_doctor_info_session()
                return render_template('doctor_edit_info.html', WEB_INFOS = WEB_INFOS, doctorInfo = doctorInfo)
            else:
                return redirect(url_for('login', userTyp=userTyp))
        else:
            abort(404)
    else:
        userGender = request.form.get('editGender')
        userBirthday = request.form.get('editBirthday')
        userProvince = request.form.get('editProvince')
        userCity = request.form.get('editCity')
        userCounty = request.form.get('editCounty')
        userTel = request.form.get('editTel')
        result = True
        c = g.db.cursor()
        if userTyp == USER_TYP[0]:
            try:
                userNation = request.form.get('editPatientNation')
                userMarried = request.form.get('editPatientMarried')
                userProfession = request.form.get('editPatientProfession')
                userAddress = request.form.get('editPatientAddress')
                userId = get_patient_info_session()['patientId']
                # return userGender+userBirthday+userNation+userProvince+userCity+userCounty+userTel+userMarried+userProfession+userAddress
                c.execute('UPDATE healthms_patients_info SET patient_gender = %s, patient_birthday = %s, patient_nation = %s, patient_province = %s, patient_city = %s, patient_county = %s, patient_tel = %s, patient_married = %s, patient_profession = %s, patient_address = %s WHERE patient_id = %s', [userGender, userBirthday, userNation, userProvince, userCity, userCounty, userTel, userMarried, userProfession, userAddress, userId])
                edit_session('patientGender', userGender)
                edit_session('patientBirthday',userBirthday)
                edit_session('patientNation',userNation)
                edit_session('patientProvince',userProvince)
                edit_session('patientCity',userCity)
                edit_session('patientCounty',userCounty)
                edit_session('patientTel',userTel)
                edit_session('patientMarried',userMarried)
                edit_session('patientProfession',userProfession)
                edit_session('patientAddress',userAddress)
                patientInfo = get_patient_info_session()
                result = True
            except Exception, e:
                logging.warning(e)
                result = u'后台数据错误！'
            return render_template('patient_edit_info.html', WEB_INFOS = WEB_INFOS, patientInfo = patientInfo, result = result)
        elif userTyp == USER_TYP[1]:
            try:
                userCheckTel = request.form.get('editDoctorCheckTel')
                userHospitalName = request.form.get('editDoctorHospitalName')
                userOffices = request.form.get('editDoctorOffices')
                userProfessional = request.form.get('editDoctorProfessional')
                userJob = request.form.get('editDoctorJob')
                userSpecialty = request.form.get('editDoctorSpecialty')
                userImg = request.files['editDoctorImg']
                userId = get_doctor_info_session()['doctorId']
                imgUrl = get_doctor_info_session()['doctorImg']
                isImgFile = '.' in secure_filename(userImg.filename) and secure_filename(userImg.filename).split('.')[1] in CAROUSEL_TYP
                if isImgFile:
                    imgExtension = secure_filename(userImg.filename).split('.')[1]
                    if imgExtension in CAROUSEL_TYP:
                        imgName = str(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))) + str(random.randint(10000, 99999)) + '.' + imgExtension
                        bucket = Bucket('doctorimg')
                        imgOldName = imgUrl.split('/')[-1]
                        if imgOldName != 'user.png':
                            bucket.delete_object(imgOldName)
                        bucket.put_object(imgName, userImg)
                        imgUrl = bucket.generate_url(imgName)
                    else:
                        result = u'图片格式错误！'
                        return render_template('doctor_edit_info.html', WEB_INFOS = WEB_INFOS, doctorInfo = doctorInfo, result = result)
                c.execute('UPDATE healthms_doctors_info SET doctor_gender = %s, doctor_birthday = %s, doctor_check_tel =%s, doctor_tel = %s, doctor_province = %s, doctor_city =%s, doctor_county = %s, doctor_hospital_name = %s, doctor_offices = %s, doctor_professional = %s, doctor_job = %s, doctor_specialty = %s, doctor_img = %s WHERE doctor_id = %s', [userGender, userBirthday, userCheckTel, userTel, userProvince, userCity, userCounty, userHospitalName, userOffices, userProfessional, userJob, userSpecialty, imgUrl, userId])
                edit_session('doctorGender', userGender)
                edit_session('doctorBirthday',userBirthday)
                edit_session('doctorCheckTel',userCheckTel)
                edit_session('doctorTel',userTel)
                edit_session('doctorProvince',userProvince)
                edit_session('doctorCity',userCity)
                edit_session('doctorCounty',userCounty)
                edit_session('doctorHospitalName',userHospitalName)
                edit_session('doctorOffices',userOffices)
                edit_session('doctorProfessional',userProfessional)
                edit_session('doctorJob',userJob)
                edit_session('doctorSpecialty',userSpecialty)
                edit_session('doctorImg',imgUrl)
                doctorInfo = get_doctor_info_session()
            except Exception, e:
                logging.warning(e)
                result = u'后台数据错误！'
            return render_template('doctor_edit_info.html', WEB_INFOS = WEB_INFOS, doctorInfo = doctorInfo, result = result)
        return redirect(url_for('edit_user_info', userTyp=userTyp))

@app.route('/edit/user/password/<userTyp>', methods=['GET', 'POST'])
def user_edit_pwd(userTyp):
    if request.method == 'GET':
        if userTyp == USER_TYP[0]:
            if 'patientEmail' in session:
                patientInfo = get_patient_info_session()
                return render_template('user_edit_pwd.html', WEB_INFOS = WEB_INFOS, patientInfo = patientInfo)
            else:
                return redirect(url_for('login', userTyp=userTyp))
        elif userTyp == USER_TYP[1]:
            if 'doctorEmail' in session:
                doctorInfo = get_doctor_info_session()
                return render_template('user_edit_pwd.html', WEB_INFOS = WEB_INFOS, doctorInfo = doctorInfo)
            else:
                return redirect(url_for('login', userTyp=userTyp))
        else:
            abort(404)
    else:
        userCurPwd = request.form.get('editCurPwd').strip()
        userPwd = request.form.get('editPwd').strip()
        c = g.db.cursor()
        if userTyp == USER_TYP[0]:
            if 'patientEmail' in session:
                patientInfo = get_patient_info_session()
                try:
                    c.execute('SELECT patient_password FROM healthms_patients_info WHERE patient_id = %s', [patientInfo['patientId']])
                    patient = list(c.fetchall())
                    if userCurPwd == base64.decodestring(patient[0][0]):
                        c.execute('UPDATE healthms_patients_info SET patient_password = %s WHERE patient_id = %s', [base64.encodestring(userPwd), patientInfo['patientId']])
                        result = True
                    else:
                        result = u'对不起，原密码错误！'
                except Exception, e:
                    logging.warning(e)
                    result = u'对不起，后台数据错误！'
                return render_template('user_edit_pwd.html', WEB_INFOS=WEB_INFOS, patientInfo=patientInfo, result=result)
            else:
                return redirect(url_for('login', userTyp=userTyp))
        elif userTyp == USER_TYP[1]:
            if 'doctorEmail' in session:
                doctorInfo = get_doctor_info_session()
                try:
                    c.execute('SELECT doctor_password FROM healthms_doctors_info WHERE doctor_id = %s', [doctorInfo['doctorId']])
                    doctor = list(c.fetchall())
                    if userCurPwd == base64.decodestring(doctor[0][0]):
                        c.execute('UPDATE healthms_doctors_info SET doctor_password = %s WHERE doctor_id = %s', [base64.encodestring(userPwd), doctorInfo['doctorId']])
                        result = True
                    else:
                        result = u'对不起，原密码错误！'
                except Exception, e:
                    logging.warning(e)
                    result = u'对不起，后台数据错误！'
                return render_template('user_edit_pwd.html', WEB_INFOS=WEB_INFOS, doctorInfo=doctorInfo, result=result)
            else:
                return redirect(url_for('login', userTyp=userTyp))
        else:
            abort(404)


# 用户首页
@app.route('/patient', methods=['GET'])
def patient_index():
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        patientTestResult = dict()
        try:
            c = g.db.cursor()
            c.execute('SELECT * FROM healthms_test_result WHERE patient_id = %s AND test_title_id = 1 ORDER BY test_result_date DESC LIMIT 1', [session['patientId']])
            physique = list(c.fetchall())
            if physique != []:
                patientPhysiqueResult ={'testResultId': physique[0][0], 'patientPhysiqueResult': get_select_test(physique[0], True), 'testResultDate': physique[0][4]}
                patientTestResult['physique'] = patientPhysiqueResult
            c.execute('SELECT * FROM healthms_test_result WHERE patient_id = %s AND test_title_id = 2 ORDER BY test_result_date DESC LIMIT 1', [session['patientId']])
            SCL90 = list(c.fetchall())
            if SCL90 != []:
                patientSCL90Result ={'testResultId': SCL90[0][0], 'patientSCL90Result': get_select_test(SCL90[0], True), 'testResultDate': SCL90[0][4]}
                patientTestResult['SCL90'] = patientSCL90Result
        except Exception, e:
            logging.warning(e)
        return render_template('patient_index.html', WEB_INFOS = WEB_INFOS, patientInfo = patientInfo, patientTestResult = patientTestResult)
    return redirect(url_for('index'))

# 中医体质分类与判定试题 页面
@app.route('/test/<testTitle>', methods=['GET','POST'])
def patient_test(testTitle):
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        c = g.db.cursor()
        c.execute('SELECT * FROM  healthms_test_title WHERE test_title_name = "' + testTitle + '"')
        tt = list(c.fetchall())[0]
        c.execute('SELECT * FROM healthms_test_list WHERE test_title_id = ' + str(tt[0]) + ' ORDER BY test_list_id')
        tls = list(c.fetchall())
        if request.method == 'GET':
            testLists = [dict(test_list_id = tl[0], test_list_index = tl[1], test_list_content = tl[3], test_list_category = tl[4], test_list_group = tl[5], test_list_group_id = tl[6], test_list_is_opposite = tl[7], test_list_gender = tl[8]) for tl in tls]
            test = [{'test_title_id': tt[0], 'test_title_name': tt[1], 'test_title_description': tt[2], 'test_title_list_group': tt[3]}, testLists]
            return render_template('patient_test_list.html', WEB_INFOS = WEB_INFOS, patientInfo = patientInfo, test = test)
        else:
            test = set_select_test(testTitle, tls, request)
            if not test:
                abort(404)
            testResult = json.dumps(test)
            c.execute("INSERT INTO healthms_test_result (patient_id, test_title_id, test_result_content, test_result_date) VALUES (%s, %s, %s, %s)", (session['patientId'], str(tt[0]), testResult, str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))))
            return redirect(url_for('patient_test_result', result_id = g.db.insert_id()))
    return redirect(url_for('index'))

# 用户历史体质页面
@app.route('/test/history/<testTitle>', methods=['GET','POST'])
def patient_test_history(testTitle):
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        if request.method == 'GET':
            c = g.db.cursor()
            c.execute('SELECT * FROM healthms_test_title WHERE test_title_name = "' + testTitle + '"')
            tt = list(c.fetchall())[0]
            c.execute('SELECT * FROM healthms_test_result WHERE patient_id = ' + str(session['patientId']) + ' AND test_title_id = ' + str(tt[0]) + ' ORDER BY test_result_date DESC')
            trs = list(c.fetchall())
            patientTestResultList = list()
            if trs:
                for tr in trs:
                    patientTestResultList.append({'testResultId': tr[0], 'testTitleId': tr[2], 'testResultContent': get_select_test(tr, False), 'testResultDate': tr[4]})
            return render_template('patient_test_history.html', WEB_INFOS = WEB_INFOS, patientInfo = patientInfo, patientTestResultList = patientTestResultList, testTitle = testTitle, goBack=request.args.get('goBack',''))
        else:
            delId = request.form['delId']
            if delId != '':
                try:
                    c = g.db.cursor()
                    c.execute('DELETE FROM healthms_test_result WHERE test_result_id = ' + str(delId))
                except:
                    abort(404)
            return jsonify(result = 'success')
    if 'doctorEmail' in session:
        doctorInfo = get_doctor_info_session()
        if request.method == 'GET':
            c = g.db.cursor()
            c.execute('SELECT b.patient_id FROM healthms_ask_answer_doctors AS a INNER JOIN healthms_ask_form AS b ON a.ask_doctor_id = b.ask_doctor_id WHERE a.doctor_id = %s', [doctorInfo['doctorId']])
            patientId = list(c.fetchall())
            if patientId != []:
                c.execute('SELECT * FROM healthms_test_title WHERE test_title_name = "' + testTitle + '"')
                tt = list(c.fetchall())[0]
                c.execute('SELECT * FROM healthms_test_result WHERE patient_id = %s AND test_title_id = %s ORDER BY test_result_date DESC', [patientId[0][0], tt[0]])
                trs = list(c.fetchall())
                patientTestResultList = list()
                if trs:
                    for tr in trs:
                        patientTestResultList.append({'testResultId': tr[0], 'testTitleId': tr[2], 'testResultContent': get_select_test(tr, False), 'testResultDate': tr[4]})
                return render_template('patient_test_history.html', WEB_INFOS = WEB_INFOS, doctorInfo = doctorInfo, patientTestResultList = patientTestResultList, testTitle = testTitle, goBack=request.args.get('goBack',''))
            else:
                abort(404)
    else:
        return redirect(url_for('index'))

# 用户体质结果页面
@app.route('/test/result/<int:result_id>', methods=['GET'])
def patient_test_result(result_id):
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        tr = list()
        try:
            c = g.db.cursor()
            c.execute('SELECT a.*, b.test_title_name FROM healthms_test_result as a INNER JOIN healthms_test_title as b ON a.test_title_id = b.test_title_id WHERE a.test_result_id = ' + str(result_id))
            tr = list(c.fetchall())
        except Exception, e:
            logging.warning(e)
            abort(404)
        if tr != []:
            tr = tr[0]
            if tr[1] == session['patientId']:
                testTitle = None
                patientTestResult = {'testResultId': tr[0], 'test_title_id':tr[2], 'testResultContent': get_select_test(tr, True), 'testResultDate': tr[4]}
                return render_template('patient_test_result.html', WEB_INFOS = WEB_INFOS, patientInfo = patientInfo, patientTestResult = patientTestResult, testTitle = tr[5])
        else:
            abort(404)
    elif 'doctorEmail' in session:
        doctorInfo = get_doctor_info_session()
        tr = list()
        try:
            c = g.db.cursor()
            c.execute('SELECT b.patient_id FROM healthms_ask_answer_doctors AS a INNER JOIN healthms_ask_form AS b ON a.ask_doctor_id = b.ask_doctor_id WHERE a.doctor_id = %s', [doctorInfo['doctorId']])
            patientId = list(c.fetchall())
            if patientId != []:
                c.execute('SELECT a.*, b.test_title_name FROM healthms_test_result as a INNER JOIN healthms_test_title as b ON a.test_title_id = b.test_title_id WHERE a.test_result_id = %s', [result_id])
                tr = list(c.fetchall())
                if tr != []:
                    tr = tr[0]
                    if tr[1] == patientId[0][0]:
                        testTitle = None
                        patientTestResult = {'testResultId': tr[0], 'test_title_id':tr[2], 'testResultContent': get_select_test(tr, True), 'testResultDate': tr[4]}
                        return render_template('patient_test_result.html', WEB_INFOS = WEB_INFOS, doctorInfo = doctorInfo, patientTestResult = patientTestResult, testTitle = tr[5])
            else:
                abort(404)
        except Exception, e:
            logging.warning(e)
            abort(404)
        else:
            abort(404)
    else:
        return redirect(url_for('index'))

# 9种体质详细页面
@app.route('/test/physique/cate/<int:cate_id>', methods=['GET'])
def patient_test_physique_cate(cate_id):
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        try:
            c = g.db.cursor()
            c.execute('SELECT * FROM healthms_test_characteristic WHERE test_characteristic_id = ' + str(cate_id))
            tc = list(c.fetchall())[0]
            patientTestCate = {'cateId': tc[0], 'cateName': tc[3], 'cateContent': get_physique_cate(tc), 'cateCreateDate': tc[5]}
        except Exception, e:
            logging.warning(e)
            abort(404)
        return render_template('patient_test_cate.html', WEB_INFOS = WEB_INFOS, patientInfo = patientInfo, patientTestCate = patientTestCate, testTitle=WEB_INFOS['TEST_NAMES'][0])
    else:
        return redirect(url_for('index'))

# 用户提问
@app.route('/ask/form/<typ>', methods=['GET', 'POST'])
def patient_ask_form_deal(typ):
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        if request.method == 'GET':
            if typ == 'add':
                return render_template('patient_ask_form_deal.html', WEB_INFOS = WEB_INFOS, patientInfo = patientInfo, CAROUSEL_TYP = CAROUSEL_TYP)
            # elif typ == 'edit':
            #     askId = request.args.get('askId')
            #     c = g.db.cursor()
            #     c.execute('SELECT * FROM healthms_ask_form WHERE ask_doctor_id = %s', [askId])
            #     askForm = list(c.fetchall())[0]
            #     return render_template('patient_ask_form_deal.html', WEB_INFOS = WEB_INFOS, patientInfo = patientInfo, CAROUSEL_TYP = CAROUSEL_TYP, askForm = askForm)
            else:
                abort(404)
        else:
            cardinalSymptom = request.form.get('cardinalSymptom').strip()
            otherDiscomfort = request.form.get('otherDiscomfort').strip()
            sickTime = request.form.get('sickTime').strip()
            lipColor = request.form.get('lipColor').strip()
            bodyFeel = request.form.get('bodyFeel').strip()
            sweatingCondition = request.form.get('sweatingCondition').strip()
            appetiteCondition = request.form.get('appetiteCondition').strip()
            drinkingCondition = request.form.get('drinkingCondition').strip()
            shitCondition = request.form.get('shitCondition').strip()
            urineCondition = request.form.get('urineCondition').strip()
            spiritSleepCondition = request.form.get('spiritSleepCondition').strip()
            moodCondition = request.form.get('moodCondition').strip()
            tonguePulseCondition = request.form.get('tonguePulseCondition').strip()
            pubesCondition = request.form.get('pubesCondition')
            localLesion = request.form.get('localLesion').strip()
            briefHistory = request.form.get('briefHistory').strip()
            tongueImg = request.files['tongueImg']
            nowTime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            c = g.db.cursor()
            imgUrl = ''
            isImgFile = '.' in secure_filename(tongueImg.filename) and secure_filename(tongueImg.filename).split('.')[1] in CAROUSEL_TYP
            if isImgFile:
                imgExtension = secure_filename(tongueImg.filename).split('.')[1]
                if imgExtension in CAROUSEL_TYP:
                    imgName = str(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))) + str(random.randint(10000, 99999)) + '.' + imgExtension
                    bucket = Bucket('tongue')
                    bucket.put_object(imgName, tongueImg)
                    imgUrl = bucket.generate_url(imgName)
            if cardinalSymptom != '' and sickTime != '' and lipColor != '' and bodyFeel != '' and sweatingCondition != '' and appetiteCondition != '' and drinkingCondition != '' and shitCondition != '' and urineCondition != '' and spiritSleepCondition != '' and moodCondition != '' and tonguePulseCondition != '' and briefHistory != '':   
                if typ == 'add':
                    c.execute('INSERT INTO healthms_ask_form (patient_id, ask_doctor_cardinal_symptom, ask_doctor_other_discomfort, ask_doctor_sick_time, ask_doctor_lip_color, ask_doctor_body_feel, ask_doctor_sweating_condition, ask_doctor_appetite_condition, ask_doctor_drinking_condition, ask_doctor_shit_condition, ask_doctor_urine_condition, ask_doctor_spirit_sleep_condition, ask_doctor_mood_condition, ask_doctor_tongue_pulse_condition, ask_doctor_pubes_condition, ask_doctor_local_lesion, ask_doctor_brief_history, ask_doctor_tongue_img, ask_doctor_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [patientInfo['patientId'], cardinalSymptom, otherDiscomfort, sickTime, lipColor, bodyFeel, sweatingCondition, appetiteCondition, drinkingCondition, shitCondition, urineCondition, spiritSleepCondition, moodCondition, tonguePulseCondition, pubesCondition, localLesion, briefHistory, imgUrl, nowTime])
                else:
                    abort(404)
                # elif typ == 'edit':
                # 有 bug 当提交信息时 若未上传图片 会将数据库中原有的 舌苔图片 路径覆盖为空
                #     askId = request.form.get('askId')
                #     c.execute('UPDATE healthms_ask_form SET ask_doctor_cardinal_symptom = %s, ask_doctor_other_discomfort = %s, ask_doctor_sick_time = %s, ask_doctor_lip_color = %s, ask_doctor_body_feel = %s, ask_doctor_sweating_condition = %s, ask_doctor_appetite_condition = %s, ask_doctor_drinking_condition = %s, ask_doctor_shit_condition = %s, ask_doctor_urine_condition = %s, ask_doctor_spirit_sleep_condition = %s, ask_doctor_mood_condition = %s, ask_doctor_tongue_pulse_condition = %s, ask_doctor_pubes_condition = %s, ask_doctor_local_lesion = %s, ask_doctor_brief_history = %s, ask_doctor_tongue_img = %s WHERE ask_doctor_id = %s', [cardinalSymptom, otherDiscomfort, sickTime, lipColor, bodyFeel, sweatingCondition, appetiteCondition, drinkingCondition, shitCondition, urineCondition, spiritSleepCondition, moodCondition, tonguePulseCondition, pubesCondition, localLesion, briefHistory, imgUrl, askId])
            return redirect(url_for('patient_ask_form_list'))
    else:
        return redirect(url_for('index'))

# 用户提问列表
@app.route('/ask/form/list', methods=['GET'])
def patient_ask_form_list():
    if 'patientEmail' in session:
        c = g.db.cursor()
        if request.method == 'GET':
            patientInfo = get_patient_info_session()
            c.execute('SELECT * FROM healthms_ask_form WHERE patient_id = %s ORDER BY ask_doctor_date DESC', [patientInfo['patientId']])
            askForms = list(c.fetchall())
            return render_template('patient_ask_form_list.html', WEB_INFOS = WEB_INFOS, patientInfo = patientInfo, askForms = askForms)
        # 取消 用户删除 问诊单
        # else: 
        #     try:
        #         askId = request.form.get('askId')
        #         c.execute('SELECT ask_doctor_tongue_img FROM healthms_ask_form WHERE ask_doctor_id = %s', [askId])
        #         imgOldName = c.fetchall()[0][0]
        #         if imgOldName != '':
        #             imgOldName = imgOldName.split('/')[-1]
        #             Bucket('tongue').delete_object(imgOldName)                
        #         c.execute('DELETE FROM healthms_ask_form WHERE ask_doctor_id = %s', [askId])
        #     except Exception, e:
        #         logging.warning(e)
        #         return json.dumps('error')
        #     return json.dumps('success')
    else:
        return redirect(url_for('index'))

# @app.route('/ask/form/detail/<int:askId>', methods=['GET'])
# def patient_ask_form_detail(askId):
#     if 'patientEmail' in session:
#         patientInfo = get_patient_info_session()
#         try:
#             c = g.db.cursor()
#             c.execute('SELECT a.*, b.* FROM healthms_ask_form AS a INNER JOIN healthms_patients_info AS b ON a.patient_id = b.patient_id WHERE a.ask_doctor_id = %s', [askId])
#             askForm = list(c.fetchall())[0]
#         except Exception, e:
#             logging.warning(e)
#         return render_template('ask_form_detail.html', WEB_INFOS = WEB_INFOS, patientInfo = patientInfo, askForm = askForm)
#     return redirect(url_for('index'))

# 医生查看 问诊单 列表
@app.route('/doctor/ask/form/list', methods=['GET'])
def doctor_ask_form_list():
    if 'doctorEmail' in session:
        doctorInfo = get_doctor_info_session()
        try:
            c = g.db.cursor()
            c.execute('SELECT a.*, b.* FROM healthms_ask_form AS a INNER JOIN healthms_patients_info AS b ON a.patient_id = b.patient_id WHERE a.ask_doctor_hasDoctor = 0 ORDER BY a.ask_doctor_date DESC')
            askForms = list(c.fetchall())
        except Exception, e:
            logging.warning(e)
        return render_template('doctor_ask_form_list.html', WEB_INFOS = WEB_INFOS, doctorInfo = doctorInfo, askForms = askForms)
    return redirect(url_for('index'))

# 医生查看自己 问诊单列表
@app.route('/doctor/has/ask/form/list', methods=['GET'])
def doctor_has_ask_form_list():
    if 'doctorEmail' in session:
        doctorInfo = get_doctor_info_session()
        try:
            c = g.db.cursor()
            c.execute('SELECT * FROM (SELECT b.* FROM healthms_ask_answer_doctors AS a INNER JOIN healthms_ask_form AS b ON a.ask_doctor_id=b.ask_doctor_id WHERE doctor_id = %s) AS c INNER JOIN healthms_patients_info AS d ON c.patient_id = d.patient_id ORDER BY c.ask_doctor_date DESC', [doctorInfo['doctorId']])
            askForms = list(c.fetchall())
        except Exception, e:
            logging.warning(e)
        return render_template('doctor_has_ask_form_list.html', WEB_INFOS = WEB_INFOS, doctorInfo = doctorInfo, askForms = askForms)
    return redirect(url_for('index'))

@app.route('/ask/form/detail/<userTyp>/<int:askId>', methods=['GET'])
def ask_form_detail(userTyp, askId):
    c = g.db.cursor()
    if userTyp == USER_TYP[0]:
        if 'patientEmail' in session:
            patientInfo = get_patient_info_session()
            patientTestResult = dict()
            try:
                # 查询 问诊单
                c.execute('SELECT * FROM healthms_ask_form WHERE ask_doctor_id = %s', [askId])
                askForm = list(c.fetchall())[0]
                # 查询患者信息
                c.execute('SELECT * FROM healthms_patients_info WHERE patient_id = %s', [askForm[1]])
                patient = list(c.fetchall())[0]
                # 查询回复列表
                c.execute('SELECT * FROM healthms_ask_answer_list WHERE ask_doctor_id = %s ORDER BY answer_date', [askId])
                answers = list(c.fetchall())
                # 查询医生信息
                c.execute('SELECT b.* FROM healthms_ask_answer_doctors AS a INNER JOIN healthms_doctors_info AS b ON a.doctor_id = b.doctor_id WHERE a.ask_doctor_id = %s', [askId])
                doctor = list(c.fetchall())
                # 查询 本用户 最新一次 中医基本体质分类
                c.execute('SELECT * FROM healthms_test_result WHERE patient_id = %s AND test_title_id = 1 ORDER BY test_result_date DESC LIMIT 1', [session['patientId']])
                physique = list(c.fetchall())
                if physique != []:
                    patientPhysiqueResult ={'testResultId': physique[0][0], 'patientPhysiqueResult': get_select_test(physique[0], True), 'testResultDate': physique[0][4]}
                    patientTestResult['physique'] = patientPhysiqueResult
                # 查询 本用户 最新一次 SCL-90 
                c.execute('SELECT * FROM healthms_test_result WHERE patient_id = %s AND test_title_id = 2 ORDER BY test_result_date DESC LIMIT 1', [session['patientId']])
                SCL90 = list(c.fetchall())
                if SCL90 != []:
                    patientSCL90Result ={'testResultId': SCL90[0][0], 'patientSCL90Result': get_select_test(SCL90[0], True), 'testResultDate': SCL90[0][4]}
                    patientTestResult['SCL90'] = patientSCL90Result
                resultDict = {'askForm': askForm, 'answers': answers, 'patient': patient, 'doctor': doctor, 'patientTestResult': patientTestResult}
            except Exception, e:
                logging.warning(e)
                abort(404)
            return render_template('ask_form_detail.html', WEB_INFOS = WEB_INFOS, patientInfo = patientInfo, resultDict = resultDict)
        return redirect(url_for('index'))
    elif userTyp == USER_TYP[1]:
        if 'doctorEmail' in session:
            doctorInfo = get_doctor_info_session()
            patientTestResult = dict()
            try:
                # 查询 问诊单
                c.execute('SELECT * FROM healthms_ask_form WHERE ask_doctor_id = %s', [askId])
                askForm = list(c.fetchall())[0]
                # 查询 患者信息
                c.execute('SELECT * FROM healthms_patients_info WHERE patient_id = %s', [askForm[1]])
                patient = list(c.fetchall())[0]
                # 查询 回复列表
                c.execute('SELECT * FROM healthms_ask_answer_list WHERE ask_doctor_id = %s ORDER BY answer_date', [askId])
                answers = list(c.fetchall())
                # 查询 医生信息
                c.execute('SELECT b.* FROM healthms_ask_answer_doctors AS a INNER JOIN healthms_doctors_info AS b ON a.doctor_id = b.doctor_id WHERE a.ask_doctor_id = %s', [askId])
                doctor = list(c.fetchall())
                # 查询 患者 最新一次 中医基本体质分类
                c.execute('SELECT * FROM healthms_test_result WHERE patient_id = %s AND test_title_id = 1 ORDER BY test_result_date DESC LIMIT 1', [askForm[1]])
                physique = list(c.fetchall())
                if physique != []:
                    patientPhysiqueResult ={'testResultId': physique[0][0], 'patientPhysiqueResult': get_select_test(physique[0], True), 'testResultDate': physique[0][4]}
                    patientTestResult['physique'] = patientPhysiqueResult
                # 查询 患者 最新一次 SCL-90 
                c.execute('SELECT * FROM healthms_test_result WHERE patient_id = %s AND test_title_id = 2 ORDER BY test_result_date DESC LIMIT 1', [askForm[1]])
                SCL90 = list(c.fetchall())
                if SCL90 != []:
                    patientSCL90Result ={'testResultId': SCL90[0][0], 'patientSCL90Result': get_select_test(SCL90[0], True), 'testResultDate': SCL90[0][4]}
                    patientTestResult['SCL90'] = patientSCL90Result
                resultDict = {'askForm': askForm, 'answers': answers, 'patient': patient, 'doctor': doctor, 'patientTestResult': patientTestResult}
                logging.warning(resultDict)
            except Exception, e:
                logging.warning(e)
                abort(404)
            return render_template('ask_form_detail.html', WEB_INFOS = WEB_INFOS, doctorInfo = doctorInfo, resultDict = resultDict)
        return redirect(url_for('index'))
    abort(404)

@app.route('/ask/form/deal/<userTyp>', methods=['POST'])
def ask_form_deal(userTyp):
    c = g.db.cursor()
    if userTyp == USER_TYP[0]:
        if 'patientEmail' in session:
            askId = request.form.get('askId')
            commition = request.form.get('commition')
            c.execute('INSERT INTO healthms_ask_answer_list (ask_doctor_id, answer_content, answer_is_patient) VALUES (%s, %s, %s)', [askId, commition, 1])
            c.execute('UPDATE healthms_ask_form SET ask_doctor_isAnswer = 0 WHERE ask_doctor_id = %s', [askId])
            return redirect(url_for('ask_form_detail', userTyp=userTyp, askId=askId))
        else:
            return redirect(url_for('index'))
    elif userTyp == USER_TYP[1]:
        if 'doctorEmail' in session:
            doctorInfo = get_doctor_info_session()
            askId = request.form.get('askId')
            commition = request.form.get('commition')
            c.execute('SELECT ask_doctor_id FROM healthms_ask_answer_doctors WHERE ask_doctor_id = %s', [askId])
            askDoctorId = c.fetchall()
            if askDoctorId !=[]:
                c.execute('INSERT INTO healthms_ask_answer_doctors (doctor_id, ask_doctor_id) VALUES (%s, %s)', [doctorInfo['doctorId'], askId])
                c.execute('UPDATE healthms_ask_form SET ask_doctor_hasDoctor = 1 WHERE ask_doctor_id = %s', [askId])
            c.execute('INSERT INTO healthms_ask_answer_list (ask_doctor_id, answer_content, answer_is_patient) VALUES (%s, %s, %s)', [askId, commition, 0])
            c.execute('UPDATE healthms_ask_form SET ask_doctor_isAnswer = 1 WHERE ask_doctor_id = %s', [askId])
            return redirect(url_for('ask_form_detail', userTyp=userTyp, askId=askId))
        else:
            return redirect(url_for('index'))
    else:
        abort(404)

@app.route('/ask/form/finish', methods=['POST'])
def ask_form_finish():
    if 'patientEmail' in session:
        askId = request.form.get('askId')
        c = g.db.cursor()
        c.execute('UPDATE healthms_ask_form SET ask_doctor_is_finish = 1 WHERE ask_doctor_id = %s', [askId])
        return redirect(url_for('ask_form_detail', userTyp=USER_TYP[0], askId=askId))
    else:
        return redirect(url_for('index'))

# 检测 Email 是否存在 URL
@app.route('/check_email_exist', methods=['POST'])
def check_email_exist():
    typ = request.form['typ']
    email = request.form['email'].strip()
    result = False
    if typ == WEB_INFOS['USER_TYP'][0]:
        try:
            c = g.db.cursor()
            c.execute('SELECT patient_email FROM healthms_patients_info WHERE patient_email = "' + email + '"')
            patients = list(c.fetchall())
            if patients != []:
                result = True
        except Exception, e:
            logging.warning(e)
    elif typ == WEB_INFOS['USER_TYP'][1]:
        try:
            c = g.db.cursor()
            c.execute('SELECT doctor_email FROM healthms_doctors_info WHERE doctor_email = "' + email + '"')
            doctors = list(c.fetchall())
            if doctors != []:
                result = True
        except Exception, e:
            logging.warning(e)
    return jsonify(result = result)

# 获得验证码 和 验证验证码 URL
@app.route('/code/<float:n>', methods=['GET','POST']) 
def get_code(n): 
    if request.method == 'GET':  
        #把strs发给前端,或者在后台使用session保存 
        code_img,strs = check_code.create_validate_code() 
        buf = StringIO.StringIO() 
        code_img.save(buf,'JPEG',quality=70) 
     
        buf_str = buf.getvalue() 
        response = app.make_response(buf_str)  
        response.headers['Content-Type'] = 'image/jpeg'  
        session['code'] = strs
        return response 
    else:
        code = request.form['code']
        if code == session['code']:
            return jsonify(result = True)
        else:
            return jsonify(result = False)

# 用户登出 URL
@app.route('/logout/<userTyp>', methods=['GET'])
def logout(userTyp):
    if userTyp == 'patient':
        del_patient_info_session()
    elif userTyp == 'doctor':
        del_doctor_info_session()
    elif userTyp == 'admin':
        del_admin_info_session()
        return redirect(url_for('admin_login'))
    return redirect(url_for('index'))

# 后台登录页面
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        adminName = request.form['adminName'].strip()
        adminPassword = request.form['adminPassword'].strip()
        try:
            c = g.db.cursor()
            c.execute('SELECT * FROM healthms_admins_info')
            admins = list(c.fetchall())
            for admin in admins:
                if adminName == admin[1] and adminPassword == base64.decodestring(admin[2]):
                    set_admin_info_session(admin)
                    return redirect(url_for('admin'))
            error = u'对不起，用户名或密码不正确！'
        except Exception, e:
            logging.warning(e)
        return render_template('admin_login.html', WEB_INFOS = WEB_INFOS, error = error)
    elif request.method == 'GET':
        return render_template('admin_login.html', WEB_INFOS = WEB_INFOS)
    else:
        abort(404)

@app.route('/admin', methods=['GET'])
def admin():
    if 'adminUsername' in session:
        adminInfo = get_admin_info_session()
        return render_template('admin_index.html', WEB_INFOS = WEB_INFOS, adminInfo = adminInfo)
    return redirect(url_for('admin_login'))

@app.route('/admin/info/add/<infoTyp>', methods=['GET', 'POST'])
def admin_info_add(infoTyp):
    if 'adminUsername' in session:
        if infoTyp in WEB_INFOS['INFO_TYP']:
            adminInfo = get_admin_info_session()
            if request.method == 'GET':
                return render_template('admin_info_add.html', WEB_INFOS = WEB_INFOS, adminInfo = adminInfo, infoTyp = infoTyp)
            else:
                nowTime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                infoTitle = request.form.get('infoTitle')
                infoContent = request.form.get('infoContent')
                try:
                    c = g.db.cursor()
                    c.execute('INSERT INTO healthms_info (info_type, info_title, info_content, admin_id, info_create_date) VALUES (%s, %s, %s, %s, %s)', [infoTyp, infoTitle, infoContent, adminInfo['adminId'], nowTime])
                except Exception, e:
                    raise e
                return redirect(url_for('admin_info_list', infoTyp=infoTyp))
        else:
            abort(404)
    return redirect(url_for('admin_login'))

@app.route('/admin/info/del/', methods=['POST'])
def admin_info_del():
    if 'adminUsername' in session:
        adminInfo = get_admin_info_session()
        infoId = request.form.get('infoId')
        c = g.db.cursor()
        c.execute('DELETE FROM healthms_info WHERE info_id = %s', [infoId])
        return json.dumps('success')
    return redirect(url_for('admin_login'))

@app.route('/admin/info/list/<infoTyp>', methods=['GET'])
def admin_info_list(infoTyp):
    if 'adminUsername' in session:
        if infoTyp in WEB_INFOS['INFO_TYP']:
            adminInfo = get_admin_info_session()
            c = g.db.cursor()
            c.execute('SELECT a.*,b.admin_username,b.admin_id FROM healthms_info AS a INNER JOIN healthms_admins_info AS b ON a.admin_id = b.admin_id WHERE a.info_type = "' + infoTyp + '" ORDER BY a.info_edit_date DESC')
            articles = list(c.fetchall())
            return render_template('admin_info_list.html', WEB_INFOS = WEB_INFOS, adminInfo = adminInfo, articles = articles, infoTyp = infoTyp)
        else:
            abort(404)
    return redirect(url_for('admin_login'))

@app.route('/admin/info/list/<int:infoId>', methods=['GET', 'POST'])
def admin_info_detail(infoId):
    if 'adminUsername' in session:
        adminInfo = get_admin_info_session()
        c = g.db.cursor()
        if request.method == 'GET':
            c.execute('SELECT a.*,b.admin_username FROM healthms_info AS a INNER JOIN healthms_admins_info AS b ON a.admin_id = b.admin_id WHERE a.info_id = ' + str(infoId) + ' ORDER BY a.info_edit_date DESC')
            article = list(c.fetchall())
            isAdmin = False
            if article[0][5] == adminInfo['adminId']:
                isAdmin = True
            article.append(isAdmin)
            return render_template('admin_info_detail.html', WEB_INFOS = WEB_INFOS, adminInfo = adminInfo, article = article)
        else:
            infoTitle = request.form.get('infoTitle')
            infoContent = request.form.get('infoContent')
            infoTyp = request.form.get('infoTyp')
            c.execute('UPDATE healthms_info SET info_title = %s, info_content = %s WHERE info_id = %s', [infoTitle, infoContent, str(infoId)])
            return redirect(url_for('admin_info_list', infoTyp = infoTyp))
    return redirect(url_for('admin_login'))

@app.route('/admin/friend/link/<typ>', methods=['GET', 'POST'])
def admin_friend_link(typ):
    if 'adminUsername' in session:
        adminInfo = get_admin_info_session()
        c = g.db.cursor()
        if request.method == 'GET':
            if typ == 'list':
                c.execute('SELECT a.*,b.admin_username FROM healthms_friend_link AS a INNER JOIN healthms_admins_info AS b ON a.admin_id = b.admin_id')
                friendLinks = list(c.fetchall())
                return render_template('admin_friend_link.html', WEB_INFOS = WEB_INFOS, adminInfo = adminInfo, friendLinks = friendLinks)
        else:
            if typ == 'add':
                friendLinkTitle = request.form.get('friendLinkTitle')
                friendLinkUrl = request.form.get('friendLinkUrl')
                c.execute('INSERT INTO healthms_friend_link (friend_link_title, friend_link_url, admin_id) VALUES (%s, %s, %s)', [friendLinkTitle, friendLinkUrl, adminInfo['adminId']])
                return json.dumps('success')
            elif typ == 'edit':
                friendLinkId = request.form.get('friendLinkId')
                friendLinkTitle = request.form.get('friendLinkTitle')
                friendLinkUrl = request.form.get('friendLinkUrl')
                c.execute('UPDATE healthms_friend_link SET friend_link_title = %s, friend_link_url = %s, admin_id = %s WHERE friend_link_id = %s', [friendLinkTitle, friendLinkUrl, adminInfo['adminId'], friendLinkId])
                return json.dumps('success')
            elif typ == 'del':
                friendLinkId = request.form.get('friendLinkId')
                c.execute('DELETE FROM healthms_friend_link WHERE friend_link_id = %s', [friendLinkId])
                return json.dumps('success')
            else:
                return redirect(url_for('admin_friend_link', typ='list'))
    return redirect(url_for('admin_login'))

@app.route('/admin/carousel/list', methods=['GET', 'POST'])
def admin_carousel_list():
    if 'adminUsername' in session:
        adminInfo = get_admin_info_session()
        c = g.db.cursor()
        if request.method == 'GET':
            c.execute('SELECT a.*, b.admin_username FROM healthms_carousel_img AS a INNER JOIN healthms_admins_info AS b ON a.admin_id = b.admin_id ORDER BY carousel_img_date DESC')
            imgs = list(c.fetchall())
            return render_template('admin_carousel_list.html', WEB_INFOS = WEB_INFOS, adminInfo = adminInfo, imgs = imgs)
        else:
            # 删除图片 处理
            imgId = request.form.get('imgId')
            c.execute('SELECT carousel_img_url FROM healthms_carousel_img WHERE carousel_img_id = %s', [imgId])
            imgOldName = c.fetchall()[0][0].split('/')[-1]
            c.execute('DELETE FROM healthms_carousel_img WHERE carousel_img_id = %s', [imgId])
            Bucket('carousel').delete_object(imgOldName)
            return json.dumps('success')
    return redirect(url_for('admin_login'))

@app.route('/admin/carousel/<typ>', methods=['GET', 'POST'])
def admin_carousel_deal(typ):
    if 'adminUsername' in session:
        adminInfo = get_admin_info_session()
        c = g.db.cursor()
        if request.method == 'GET':
            if typ == 'add':
                return render_template('admin_carousel_deal.html', WEB_INFOS = WEB_INFOS, adminInfo = adminInfo, typ=typ, CAROUSEL_TYP = CAROUSEL_TYP)
            elif typ == 'edit':
                imgId = request.args.get('imgId')
                c.execute('SELECT a.*, b.admin_username FROM healthms_carousel_img AS a INNER JOIN healthms_admins_info AS b ON a.admin_id = b.admin_id WHERE carousel_img_id = %s',[imgId])
                img = list(c.fetchall())[0]
                return render_template('admin_carousel_deal.html', WEB_INFOS = WEB_INFOS, adminInfo = adminInfo, typ=typ, CAROUSEL_TYP = CAROUSEL_TYP, img= img)
            else:
                return redirect(url_for('admin_carousel_list'))
        else:
            imgTitle = request.form.get('imgTitle')
            imgLink = request.form.get('imgLink')
            imgFile = request.files['imgFile']
            imgUrl = ''
            isImgFile = '.' in secure_filename(imgFile.filename)
            if isImgFile:
                imgExtension = secure_filename(imgFile.filename).split('.')[1]
                if imgExtension in CAROUSEL_TYP:
                    imgName = str(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))) + str(random.randint(10000, 99999)) + '.' + imgExtension
                    bucket = Bucket('carousel')
                    bucket.put_object(imgName, imgFile)
                    imgUrl = bucket.generate_url(imgName)
                
            if typ == 'add':
                if imgTitle != '' and imgLink != '' and imgUrl != '':
                    if imgUrl != '':
                        c.execute('INSERT INTO healthms_carousel_img (carousel_img_title, carousel_img_url, carousel_img_link, admin_id) VALUES (%s, %s, %s, %s)', [imgTitle, imgUrl, imgLink, adminInfo['adminId']])
            elif typ == 'edit':
                imgId = request.form.get('imgId')
                if imgTitle != '' and imgLink != '' and isImgFile:
                    c.execute('SELECT * FROM healthms_carousel_img WHERE carousel_img_id = %s', [imgId])
                    img = list(c.fetchall())[0]
                    imgOldName = img[2].split('/')[-1]
                    bucket.delete_object(imgOldName)
                    c.execute('UPDATE healthms_carousel_img SET carousel_img_title = %s, carousel_img_url = %s, carousel_img_link = %s, admin_id = %s WHERE carousel_img_id = %s', [imgTitle, imgUrl, imgLink, adminInfo['adminId'], imgId])
                else:
                    c.execute('UPDATE healthms_carousel_img SET carousel_img_title = %s, carousel_img_link = %s, admin_id = %s WHERE carousel_img_id = %s', [imgTitle, imgLink, adminInfo['adminId'], imgId])
            return redirect(url_for('admin_carousel_list'))
    return redirect(url_for('admin_login'))

@app.route('/admin/<userTyp>/list', methods=['GET', 'POST'])
def admin_user_list(userTyp):
    if 'adminUsername' in session:
        if userTyp in WEB_INFOS['USER_TYP']:
            adminInfo = get_admin_info_session()
            if request.method == 'GET':
                return render_template('admin_user_list.html', WEB_INFOS = WEB_INFOS, adminInfo = adminInfo, userTyp = userTyp)
        else:
            abort(404)
    return redirect(url_for('admin_login'))

@app.route('/admin/<userTyp>/list/table', methods=['GET'])
def admin_user_list_table(userTyp):
    if 'adminUsername' in session:
        c = g.db.cursor()
        if request.method == 'GET':
            if userTyp == WEB_INFOS['USER_TYP'][0]:
                c.execute('SELECT * FROM healthms_patients_info ORDER BY patient_register_date DESC')
                patients = list(c.fetchall())
                users = list()
                for patient in patients:
                    users.append({'userId': patient[0], 'userEmail': patient[1], 'userName': patient[3], 'userGender': patient[7], 'userRegDate': patient[15]})
                users = {'users': users, 'userTyp': userTyp}
            elif userTyp == WEB_INFOS['USER_TYP'][1]:
                doctorListTyp = request.args.get('doctorListTyp')
                logging.warning(doctorListTyp)
                if doctorListTyp ==  '0' or doctorListTyp ==  '1' or doctorListTyp ==  '2':
                    c.execute('SELECT * FROM healthms_doctors_info WHERE doctor_check = ' + doctorListTyp + ' ORDER BY doctor_register_date DESC')
                else:
                    c.execute('SELECT * FROM healthms_doctors_info ORDER BY doctor_register_date DESC')
                doctors = list(c.fetchall())
                users = list()
                for doctor in doctors:
                    users.append({'userId': doctor[0], 'userEmail': doctor[1], 'userName': doctor[3], 'userGender': doctor[4], 'doctorCheck': doctor[17], 'userRegDate': doctor[18]})
                users = {'users': users, 'userTyp': userTyp, 'doctorListTyp': '3'}
            return render_template('admin_user_list_table.html', WEB_INFOS = WEB_INFOS, users = users)
        else:
            if userTyp in WEB_INFOS['USER_TYP']:
                doctorListTyp = request.form.get('doctorListTyp')
                if doctorListTyp ==  '0' or doctorListTyp ==  '1' or doctorListTyp ==  '2':
                    c.execute('SELECT * FROM healthms_doctors_info WHERE doctor_check = ' + doctorListTyp + ' ORDER BY doctor_register_date DESC')
                else:
                    c.execute('SELECT * FROM healthms_doctors_info ORDER BY doctor_register_date DESC')
                doctors = list(c.fetchall())
                users = list()
                for doctor in doctors:
                    users.append({'userId': doctor[0], 'userEmail': doctor[1], 'userName': doctor[3], 'userGender': doctor[4], 'doctorCheck': doctor[17], 'userRegDate': doctor[18]})
                users = {'users': users, 'userTyp': userTyp, 'doctorListTyp': doctorListTyp}
                return render_template('admin_user_list_table.html', WEB_INFOS = WEB_INFOS, users = users)
            else:
                abort(404)
    else:
        return redirect(url_for('index'))

@app.route('/admin/doctor/check', methods=['GET'])
def admin_doctor_check():
    if 'adminUsername' in session:
        adminInfo = get_admin_info_session()
        c = g.db.cursor()
        c.execute('SELECT * FROM healthms_doctors_info WHERE doctor_check = 0 ORDER BY doctor_register_date DESC')
        doctors = list(c.fetchall())
        return render_template('admin_doctor_check.html', WEB_INFOS = WEB_INFOS, adminInfo = adminInfo, doctors = doctors)
    return redirect(url_for('admin_login'))

@app.route('/admin/doctor/detail/<int:doctorId>', methods=['GET', 'POST'])
def admin_doctor_detail(doctorId):
    if 'adminUsername' in session:
        adminInfo = get_admin_info_session()
        navTyp = request.args.get('navTyp')
        c = g.db.cursor()
        c.execute('SELECT * FROM healthms_doctors_info WHERE doctor_id = ' + str(doctorId))
        doctor = list(c.fetchall())[0]
        if request.method == 'GET':
            doctorCheckReason = list()
            if doctor[17] != 0:
                c.execute('SELECT * FROM healthms_doctor_check_list WHERE doctor_id = ' + str(doctorId))
                doctorCheckReason = list(c.fetchall())[0]
                logging.warning(doctorCheckReason)
            return render_template('admin_doctor_detail.html', WEB_INFOS = WEB_INFOS, adminInfo = adminInfo, doctor = doctor, doctorCheckReason = doctorCheckReason, navTyp = navTyp)
        elif request.method == 'POST':
            result = request.form.get('doctorCheckResult')
            checkResult = ''
            if result == 'false':
                checkResult = 1 # 1为未通过验证
            elif result == 'true':
                checkResult = 2 # 2为通过验证
            if checkResult != '':
                checkTime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                doctorCheckReason = request.form.get('doctorCheckReason')
                c.execute('INSERT INTO healthms_doctor_check_list (doctor_id, admin_id, doctor_check_result, doctor_check_reason, doctor_check_date) VALUES (%s, %s, %s, %s, %s)', [doctor[0], adminInfo['adminId'], checkResult, doctorCheckReason, checkTime])
                c.execute('UPDATE healthms_doctors_info SET doctor_check = %s WHERE doctor_id = %s', [checkResult, doctor[0]])
                return redirect(url_for('admin_doctor_check'))
            else:
                abort(404)
    return redirect(url_for('admin_login'))

@app.route('/admin/patient/detail/<int:patientId>', methods=['GET'])
def admin_patient_detail(patientId):
    if 'adminUsername' in session:
        adminInfo = get_admin_info_session()
        if request.method == 'GET':
            c = g.db.cursor()
            c.execute('SELECT * FROM healthms_patients_info WHERE patient_id = ' + str(patientId))
            patient = list(c.fetchall())[0]
            return render_template('admin_patient_detail.html', WEB_INFOS = WEB_INFOS, adminInfo = adminInfo, patient = patient)
    return redirect(url_for('admin_login'))


# @app.route('/ueditor/upload', methods=['GET', 'POST', 'OPTIONS'])
# def ueditor_upload():
#     result = {'state': 'REEOR'}
#     result = json.dumps(result)
#     res = make_response(result)
#     res.mimetype = mimetype
#     res.headers['Access-Control-Allow-Origin'] = '*'
#     res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
#     return res

# 函数
def valid_login(email, pwd, typ):
    '''验证登录是否成功
        接受三个参数：Email、密码、类型（patient 或 doctor）
    '''
    result = {'result': 'emailError'}
    if typ == 'patient':
        c = g.db.cursor()
        c.execute('SELECT * FROM healthms_patients_info')
        patients = list(c.fetchall())
        patients.reverse()
        for patient in patients:
            if (email == patient[1]) and (pwd == base64.decodestring(patient[2])):
                result = {'result': 'success', 'userInfo': patient}
                break
            elif (email == patient[1]) and (pwd != base64.decodestring(patient[2])):
                result = {'result': 'pwdError'}
                break
    elif typ == 'doctor':
        c = g.db.cursor()
        c.execute('SELECT * FROM healthms_doctors_info')
        doctors = list(c.fetchall())
        doctors.reverse()
        for doctor in doctors:
            if (email == doctor[1]) and (pwd != base64.decodestring(doctor[2])):
                result = {'result': 'pwdError'}
                break
            elif (email == doctor[1]) and (pwd == base64.decodestring(doctor[2])):
                if doctor[17] == 0:
                    result = {'result': 'notCheck'}
                elif doctor[17] == 1:
                    result = {'result': 'checkFailed'}
                elif doctor[17] == 2:
                    result = {'result': 'success', 'userInfo': doctor}
                break
    return result

def get_select_test(tr, isCate):
    if tr[2] == 1:
        return get_physique(tr[3], isCate)
    elif tr[2]  == 2:
        return get_SCL_90(tr[3], isCate)

def set_select_test(testTitle, testLists, request):
    if testTitle == WEB_INFOS['TEST_NAMES'][0]:
        testListPHValues = 0
        testListQXValues = 0
        testListYaXValues = 0
        testListYiXValues = 0
        testListTSValues = 0
        testListSRValues = 0
        testListXYValues = 0
        testListQYValues = 0
        testListTBValues = 0

        for tl in testLists:
            tlId = tl[0]
            healthmsTestListId = 'healthmsTestList'
            healthmsTestListId += str(tlId)
            testListValue = request.form.get(healthmsTestListId)
            if testListValue != None:
                testListCate = tl[4]
                if testListCate == '平和质':
                    testListPHValues += float(testListValue)
                elif testListCate == '气虚质':
                    testListQXValues += float(testListValue)
                elif testListCate == '阳虚质':
                    testListYaXValues += float(testListValue)
                elif testListCate == '阴虚质':
                    testListYiXValues += float(testListValue)
                elif testListCate == '痰湿质':
                    testListTSValues += float(testListValue)
                elif testListCate == '湿热质':
                    testListSRValues += float(testListValue)
                elif testListCate == '血瘀质':
                    testListXYValues += float(testListValue)
                elif testListCate == '气郁质':
                    testListQYValues += float(testListValue)
                elif testListCate == '特禀质':
                    testListTBValues += float(testListValue)
        testListValues = {'平和质': set_conversion_score(testListPHValues, 8), 
                          '气虚质': set_conversion_score(testListQXValues, 8),
                          '阳虚质': set_conversion_score(testListYaXValues, 7),
                          '阴虚质': set_conversion_score(testListYiXValues, 8),
                          '痰湿质': set_conversion_score(testListTSValues, 8),
                          '湿热质': set_conversion_score(testListSRValues, 6),
                          '血瘀质': set_conversion_score(testListXYValues, 7), 
                          '气郁质': set_conversion_score(testListQYValues, 7),
                          '特禀质': set_conversion_score(testListTBValues, 7)}
        return set_physique(testListValues)
    elif testTitle == WEB_INFOS['TEST_NAMES'][1]:
        f1,f2,f3,f4,f5,f6,f7,f8,f9,f10 = 0,0,0,0,0,0,0,0,0,0
        for tl in testLists:
            tlId = tl[0]
            healthmsTestListId = 'healthmsTestList'
            healthmsTestListId += str(tlId)
            testListValue = request.form.get(healthmsTestListId)
            if testListValue != None:
                testListGroup = tl[5]
                if testListGroup == 1:
                    f1 += float(testListValue)
                elif testListGroup == 2:
                    f2 += float(testListValue)
                elif testListGroup == 3:
                    f3 += float(testListValue)
                elif testListGroup == 4:
                    f4 += float(testListValue)
                elif testListGroup == 5:
                    f5 += float(testListValue)
                elif testListGroup == 6:
                    f6 += float(testListValue)
                elif testListGroup == 7:
                    f7 += float(testListValue)
                elif testListGroup == 8:
                    f8 += float(testListValue)
                elif testListGroup == 9:
                    f9 += float(testListValue)
                elif testListGroup == 10:
                    f10 += float(testListValue)
        testListValues = {'f1': f1, 'f2': f2, 'f3': f3, 'f4': f4, 'f5': f5, 'f6': f6, 'f7': f7, 'f8': f8, 'f9': f9, 'f10': f10}        
        return set_SCL_90(testListValues)
    else:
        return False

# 以下为 体质测试  处理函数
def set_conversion_score(score, itemNum):
    '''接受两个参数分别为：原始分，条目数
    根据：
        原始分=各个条目分值相加
        转化分数＝[(原始分－条目数)/(条目数×4)]×100
    两个公式得出转化分, 并输出
    '''
    return (score - itemNum) / (itemNum * 4) * 100


def set_physique(testListValues):
    '''
    # 接受一个九种体质的字典，格式为{'体质名': 转化分}；
    # 返回一个字典，分别为： mainPhysiquePH （主要体质为平和质）、
    #                     maybePhysiquePH （主要体质基本为平和质）、
    #                     mainPhysiqueOt （主要体质为其他8种体质中的一种）、
    #                     maybePhysiqueOt （倾向于其他8种体质中的一种或几种）
    # 注：当 mainPhysiqueOt 不为空时，mainPhysiquePH 和 maybePhysiquePH 为空
    '''
    testListPHValue = testListValues.pop('平和质')
    result = dict()
    mainPhysiquePH = ''
    maybePhysiquePH = ''
    mainPhysiqueOtList = list()
    maybePhysiqueOtList = list()
    for key, value in testListValues.iteritems():
        if value >= 40:
            if is_max_num(key, value, testListValues):
                mainPhysiqueOtList.append(key)
            else:
                maybePhysiqueOtList.append(key)
        elif value < 40 and value >= 30:
            maybePhysiqueOtList.append(key)
    # logging.warning(len(mainPhysiqueOtList))
    if len(mainPhysiqueOtList) > 1:
        for temp in mainPhysiqueOtList[:-1]:
            maybePhysiqueOtList.append(mainPhysiqueOtList.pop())
    if len(mainPhysiqueOtList) == 0:
        if testListPHValue >= 60:
            if not maybePhysiqueOtList:
                mainPhysiquePH = '平和质'
            else:
                maybePhysiquePH = '平和质'
    return {'mainPhysiquePH': mainPhysiquePH, 'maybePhysiquePH': maybePhysiquePH, 'mainPhysiqueOt': ''.join(mainPhysiqueOtList), 'maybePhysiqueOt': ', '.join(maybePhysiqueOtList), 'physiqueScore': testListValues}

def is_max_num(numKey, num, nums):
    '''检测传入的字典 nums 中value值是否有比 num 大的数，若有返回 False；若没有返回 True'''
    flag = True
    for key, value in nums.iteritems():
        if numKey != key:
            if value > num:
                flag = False
                break
    return flag

def get_physique(physique, isCate):
    '''
    分析 json 格式的体质数据
    接受参数: json 格式的体质数据，是否添加倾向体质详细介绍
    返回值: 字典分别为 "patientTestMainResult": 主要体质名称（列表: [0]: 体质名称，[1]: 若 isCate 为 True 则为该体质的详细信息）
                     "patientTestOtResult": 倾向体质名称（多个体质的字典组成的列表，字典格式为：'patientTestOt': 体质名称，'patientTestCateId': 若 isCate 为 True 则为该体质的详细信息的 id）
    '''
    physique = json.loads(physique)
    patientTestMainResult = list()
    patientTestOtResult = list()
    c = g.db.cursor()
    c.execute('SELECT * FROM  healthms_test_characteristic WHERE test_characteristic_title_id = 1')
    tcs = list(c.fetchall())
    if physique['mainPhysiqueOt'] == '':
        if physique['mainPhysiquePH'] != '':
            patientTestMainResult.append('平和质')
        else:
            patientTestMainResult.append('基本是平和质')
        if isCate:
            for tc in tcs:
                if tc[3] == '平和质':
                    dpc = get_physique_cate(tc)
            patientTestMainResult.append(dpc)
    else:
        patientTestMainResult.append(physique['mainPhysiqueOt'])
        if isCate:
            for tc in tcs:
                if tc[3] == physique['mainPhysiqueOt']: 
                    dpc = get_physique_cate(tc)
            patientTestMainResult.append(dpc)
    if physique['maybePhysiqueOt'] != '':
        patientTestOtList = physique['maybePhysiqueOt'].split(', ')
        for patientTestOt in patientTestOtList:
            if isCate:
                for tc in tcs:
                    if tc[3] == patientTestOt:
                        patientTestOtResult.append({'patientTestOt': patientTestOt, 'patientTestCateId':tc[0]})
            else:
                patientTestOtResult.append({'patientTestOt': patientTestOt})
    return {'patientTestMainResult': patientTestMainResult, 'patientTestOtResult': patientTestOtResult}

def get_physique_cate(tc):
    '''
    处理详细体质
    接受参数：json 格式的体质详细信息
    返回值：字典
    '''
    cate_content = json.loads(tc[4])
    return {'cGeneral': cate_content['general'], 'cPhysique': cate_content['physique'], 'cExpression': cate_content['expression'], 'cPsychology': cate_content['psychology'], 'cInciTend': cate_content['inci_tend'], 'cAdaptability':cate_content['adaptability'], 'cIdentification': cate_content['identification'], 'cAdjust': cate_content['adjust']}


# 以下为 scl_90 处理函数
def set_SCL_90(content):
    testSum = 0
    testSingleAverDict = {}
    c = g.db.cursor()
    c.execute('SELECT test_list_group AS test_list_group, COUNT(test_list_group) FROM healthms_test_list WHERE test_title_id = 2 GROUP BY test_list_group')
    test_list_group_maxs = list(c.fetchall())
    for (k, v) in content.items():
        testSum += v
        for tlgm in test_list_group_maxs:
            if k == 'f'+str(tlgm[0]):
                testSingleAverDict[k] = v / tlgm[1]
    testAverage = testSum / 90
    testAnalyzeResult = {'testSum': testSum, 'testAverage': testAverage, 'testSingleAverDict': testSingleAverDict}
    return testAnalyzeResult

def get_SCL_90(content, isCate):
    content = json.loads(content)
    result = dict()
    testSingleAverList = list()
    if content['testSum'] < 160:
        result['testSum'] = {'testSum': content['testSum'], 'testSumMsg': '正常'}
    else:
        result['testSum'] = {'testSum': content['testSum'], 'testSumMsg': '不正常，请您尽快咨询心理医生'}
    result['testAverage'] = content['testAverage']
    if isCate:
        c = g.db.cursor()
        c.execute('SELECT * FROM healthms_test_characteristic WHERE test_characteristic_title_id = 2')
        htcList = list(c.fetchall())
        for (k, v) in content['testSingleAverDict'].items():
            for htc in htcList:
                if k == ('f' + str(htc[2])):
                    if v <= 1.5:
                        testSingleAverList.append([htc[3], v, '无症状', htc[4]])
                    elif v >1.5 and v <= 2.5:
                        testSingleAverList.append([htc[3], v, '轻微', htc[4]])
                    elif v >2.5 and v <= 3.5:
                        testSingleAverList.append([htc[3], v, '中度，请您尽快咨询心理医生', htc[4]])
                    elif v >3.5 and v <= 4.5:
                        testSingleAverList.append([htc[3], v, '严重，请您尽快咨询心理医生', htc[4]])
                    else:
                        testSingleAverList.append([htc[3], v, '非常严重，请您尽快咨询心理医生', htc[4]])
    result['testSingleAverList'] = testSingleAverList
    return result


def set_patient_info_session(userInfo):
    '''添加病人的 session 值，共15个'''
    session['patientId'] = userInfo[0]
    session['patientEmail'] = userInfo[1]
    session['patientName'] = userInfo[3]
    session['patientProvince'] = userInfo[4]
    session['patientCity'] = userInfo[5]
    session['patientCounty'] = userInfo[6]
    session['patientGender'] = userInfo[7]
    session['patientBirthday'] = userInfo[8]
    session['patientTel'] = userInfo[9]
    session['patientProfession'] = userInfo[10]
    session['patientNation'] = userInfo[11]
    session['patientMarried'] = userInfo[12]
    session['patientAddress'] = userInfo[13]
    session['patientLoginDate'] = userInfo[14]
    session['patientRegisterDate'] = userInfo[15]

def edit_session(key, value):
    '''修改 session 值'''
    session[key] = value

def get_patient_info_session():
    '''返回病人 session 中被设置的 session 值，共15个'''
    return {'patientId': session['patientId'],
            'patientEmail': session['patientEmail'], 
            'patientName': session['patientName'],
            'patientProvince': session['patientProvince'],
            'patientCity': session['patientCity'],
            'patientCounty': session['patientCounty'],
            'patientGender': session['patientGender'],
            'patientBirthday': session['patientBirthday'],
            'patientTel': session['patientTel'],
            'patientProfession': session['patientProfession'],
            'patientNation': session['patientNation'],
            'patientMarried': session['patientMarried'],
            'patientAddress': session['patientAddress'],
            'patientLoginDate': session['patientLoginDate'],
            'patientRegisterDate': session['patientRegisterDate']
            }

def del_patient_info_session():
    '''删除病人 session 中被设置的 session 值，共15个'''
    session.pop('patientId', None)
    session.pop('patientEmail', None)
    session.pop('patientName', None)
    session.pop('patientProvince', None)
    session.pop('patientCity', None)
    session.pop('patientCounty', None)
    session.pop('patientGender', None)
    session.pop('patientBirthday', None)
    session.pop('patientTel', None)
    session.pop('patientProfession', None)
    session.pop('patientNation', None)
    session.pop('patientMarried', None)
    session.pop('patientAddress', None)
    session.pop('patientLoginDate', None)
    session.pop('patientRegisterDate', None)

def set_doctor_info_session(userInfo):
    ''' 设置医生 session 值，共18个 '''
    session['doctorId'] = userInfo[0]
    session['doctorEmail'] = userInfo[1]
    session['doctorName'] = userInfo[3]
    session['doctorGender'] = userInfo[4]
    session['doctorBirthday'] = userInfo[5]
    session['doctorCheckTel'] = userInfo[6]
    session['doctorTel'] = userInfo[7]
    session['doctorProvince'] = userInfo[8]
    session['doctorCity'] = userInfo[9]
    session['doctorCounty'] = userInfo[10]
    session['doctorHospitalName'] = userInfo[11]
    session['doctorOffices'] = userInfo[12]
    session['doctorProfessional'] = userInfo[13]
    session['doctorJob'] = userInfo[14]
    session['doctorSpecialty'] = userInfo[15]
    session['doctorImg'] = userInfo[16]
    session['doctorLoginDate'] = userInfo[18]
    session['doctorRegisterDate'] = userInfo[19]

def get_doctor_info_session():
    '''返回医生 session 中被设置的 session 值，共18个'''
    return { 'doctorId': session['doctorId'],
             'doctorEmail': session['doctorEmail'],
             'doctorName': session['doctorName'],
             'doctorGender': session['doctorGender'],
             'doctorBirthday': session['doctorBirthday'],
             'doctorCheckTel': session['doctorCheckTel'],
             'doctorTel': session['doctorTel'],
             'doctorProvince': session['doctorProvince'],
             'doctorCity': session['doctorCity'],
             'doctorCounty': session['doctorCounty'],
             'doctorHospitalName': session['doctorHospitalName'],
             'doctorOffices': session['doctorOffices'],
             'doctorProfessional': session['doctorProfessional'],
             'doctorJob': session['doctorJob'],
             'doctorSpecialty': session['doctorSpecialty'],
             'doctorImg': session['doctorImg'],
             'doctorLoginDate': session['doctorLoginDate'],
             'doctorRegisterDate': session['doctorRegisterDate']
            }

def del_doctor_info_session():
    '''删除医生 session 中被设置的 session 值，共18个'''
    session.pop('doctorId', None)
    session.pop('doctorEmail', None)
    session.pop('doctorName', None)
    session.pop('doctorGender', None)
    session.pop('doctorBirthday', None)
    session.pop('doctorCheckTel', None)
    session.pop('doctorTel', None)
    session.pop('doctorProvince', None)
    session.pop('doctorCity', None)
    session.pop('doctorCounty', None)
    session.pop('doctorHospitalName', None)
    session.pop('doctorOffices', None)
    session.pop('doctorProfessional', None)
    session.pop('doctorJob', None)
    session.pop('doctorSpecialty', None)
    session.pop('doctorImg', None)
    session.pop('doctorLoginDate', None)
    session.pop('doctorRegisterDate', None)

def set_admin_info_session(userInfo):
    ''' 设置管理员 session 值，共5个 '''
    session['adminId'] = userInfo[0]
    session['adminUsername'] = userInfo[1]
    session['adminRank'] = userInfo[3]
    session['adminLoginDate'] = userInfo[4]
    session['adminCreateDate'] = userInfo[5]

def get_admin_info_session():
    '''返回管理员 session 中被设置的 session 值，共5个'''
    return { 'adminId': session['adminId'],
             'adminUsername': session['adminUsername'],
             'adminRank': session['adminRank'],
             'adminLoginDate': session['adminLoginDate'],
             'adminCreateDate': session['adminCreateDate']
            }

def del_admin_info_session():
    '''删除管理员 session 中被设置的 session 值，共5个'''
    session.pop('adminId', None)
    session.pop('adminUsername', None)
    session.pop('adminRank', None)
    session.pop('adminLoginDate', None)
    session.pop('adminCreateDate', None)