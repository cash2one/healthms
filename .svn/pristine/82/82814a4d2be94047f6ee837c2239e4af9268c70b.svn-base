# encoding: utf8
import MySQLdb
from flask import Flask, g, request, render_template, abort, url_for, jsonify, session, redirect
import sys, logging, StringIO, time, json, base64

import check_code

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

# 设置试题 名称
TEST_NAME = u'中医体质分类与判定'

# 设置会话密钥
app.secret_key = '\xb7Y\x9a\xbb\xdcH\xb8[\xa7[\xe8:\xfa\xac\t\xf5\x89\xb0\x8e\xc9H\xeb\x08\xd2'



# 连接数据库
@app.before_request
def before_request():
    ''' 连接数据库 '''
    g.db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS,
                           MYSQL_DB, port=int(MYSQL_PORT), charset="utf8")

# 关闭数据库
@app.teardown_request
def teardown_request(exception):
    '''关闭数据库'''
    if hasattr(g, 'db'): g.db.close()

# 首页，即登录页面
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'patientEmail' in session:
            return redirect(url_for('patient_index'))
        elif 'doctorEmail' in session:
            return redirect('/')
        return render_template('login.html', PROJECT_NAME = PROJECT_NAME)
    else:
        typ = request.form['type']
        if typ == 'patient':
            patientEmail = request.form['patientEmail'].strip()
            patientPwd = request.form['patientPassword'].strip()
            result = valid_login(patientEmail, patientPwd, typ)
            if result['result'] == 'success':
                set_patient_info_session(result['userInfo'])
                return jsonify(result = 'success', typ = typ)
            elif result['result'] == 'pwdError' or result['result'] == 'emailError':
                return jsonify(result = result['result'], typ = typ)
            else:
                abort(404)
        elif typ == 'doctor':
            doctorEmail = request.form['doctorEmail']
            doctorPwd = request.form['doctorPassword']
            result = valid_login(doctorEmail, doctorPwd, typ)
            if result == 'success':
                return jsonify(result = 'success', typ = typ)
            elif result == 'pwdError' or result == 'emailError':
                return jsonify(result = result, typ = typ)
            else:
                abort(404)
        else:
            abort(404)

# 用户个人首页，即病人目前体质
@app.route('/index', methods=['GET'])
def patient_index():
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        try:
            c = g.db.cursor()
            c.execute('SELECT * FROM healthms_test_result WHERE test_patient_id = ' + str(session['patientId']) + ' ORDER BY test_result_date DESC')
            tr = list(c.fetchall())[0]
            patientTestResult = select_test_result(tr, True)
        except :
            patientTestResult = dict()
        pageTitle = '我的体质'
        navName = ['home']
        return render_template('patient_index_result.html', PROJECT_NAME = PROJECT_NAME, patientInfo = patientInfo, patientTestResult = patientTestResult, pageTitle = pageTitle, navName = navName)
    return redirect(url_for('login'))

# 用户历史体质页面
@app.route('/index/history', methods=['GET','POST'])
def patient_test_history():
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        if request.method == 'GET':
            c = g.db.cursor()
            c.execute('SELECT * FROM healthms_test_result WHERE test_patient_id = ' + str(session['patientId']) + ' ORDER BY test_result_date DESC')
            trs = list(c.fetchall())
            patientTestResultList = list()
            if trs:
                for tr in trs:
                    patientTestResultList.append(select_test_result(tr, False))
            pageTitle = '我的体质'
            return render_template('patient_index_history.html', PROJECT_NAME = PROJECT_NAME, patientInfo = patientInfo, patientTestResultList = patientTestResultList)
        else:
            delId = request.form['delId']
            if delId != '':
                try:
                    c = g.db.cursor()
                    c.execute('DELETE FROM healthms_test_result WHERE test_result_id = ' + str(delId))
                except:
                    abort(404)
            return jsonify(result = 'success')

    else:
        return redirect(url_for('login'))

# 9种体质详细页面
@app.route('/index/cate/<nav_name>/<int:cate_id>', methods=['GET'])
def patient_test_cate(nav_name, cate_id):
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        try:
            c = g.db.cursor()
            c.execute('SELECT * FROM healthms_test_characteristic WHERE test_characteristic_id = ' + str(cate_id))
            tc = list(c.fetchall())[0]
        except:
            abort(404)
        navName = list()
        if nav_name == 'history':
            navName.append('history')
        elif nav_name == 'home':
            navName.append('home')
        return render_template('patient_index_cate.html', PROJECT_NAME = PROJECT_NAME, patientInfo = patientInfo, patientTestCate = tc, navName = navName)
    else:
        return redirect(url_for('login'))

# 用户体质结果页面
@app.route('/index/result/<int:result_id>', methods=['GET'])
def patient_test_result(result_id):
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        tr = list()
        try:
            c = g.db.cursor()
            c.execute('SELECT * FROM healthms_test_result WHERE test_result_id = ' + str(result_id))
            tr = list(c.fetchall())[0]
        except:
            abort(404)
        if tr[1] == session['patientId']:
            c1 = g.db.cursor()
            c1.execute('SELECT * FROM  healthms_test_characteristic')
            tcs = list(c1.fetchall())
            patientTestMainResult = list()
            patientTestResult = select_test_result(tr, True)
            pageTitle = '评测结果'
            navName = ['history']
            return render_template('patient_index_result.html', PROJECT_NAME = PROJECT_NAME, patientInfo = patientInfo, patientTestResult = patientTestResult, pageTitle = pageTitle, navName = navName)
        else:
            abort(404)
        

# 中医体质分类与判定试题 页面
@app.route('/index/test/<nav_name>', methods=['GET','POST'])
def patient_test(nav_name):
    if 'patientEmail' in session:
        patientInfo = get_patient_info_session()
        c = g.db.cursor()
        c.execute('SELECT * FROM healthms_test_list ORDER BY test_list_id DESC')
        tls = list(c.fetchall())
        navName = list()
        if nav_name == 'history':
            navName.append('history')
        elif nav_name == 'home':
            navName.append('home')
        if request.method == 'GET':
            testLists = list()
            for tl in tls:
                testList = {'healthms_test_list_id': tl[0], 'healthms_test_list_content': tl[1], 'healthms_test_list_category': tl[2], 'healthms_test_list_gender': tl[3] }
                testLists.append(testList)
            testLists = json.dumps(testLists)
            return render_template('patient_index_test.html', PROJECT_NAME = PROJECT_NAME, patientInfo = patientInfo, TEST_NAME = TEST_NAME, testLists = testLists, navName = navName)
        else:
            testListPHValues = 0
            testListQXValues = 0
            testListYaXValues = 0
            testListYiXValues = 0
            testListTSValues = 0
            testListSRValues = 0
            testListXYValues = 0
            testListQYValues = 0
            testListTBValues = 0

            for tl in tls:
                tlId = tl[0]
                healthmsTestListId = 'healthmsTestList'
                healthmsTestListId += str(tlId)
                testListValue = request.form.get(healthmsTestListId)
                if testListValue != None:
                    testListCate = tl[2]
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

            testListResult = judge_physique(testListValues)
            c.execute("INSERT INTO healthms_test_result (test_patient_id, test_result_main_physique_ph, test_result_maybe_physique_ph, test_result_main_physique_ot, test_result_maybe_physique_ot, test_result_date, test_result_ph, test_result_qx, test_result_yax, test_result_yix, test_result_ts, test_result_sr, test_result_xy, test_result_qy, test_result_tb) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (session['patientId'], testListResult['mainPhysiquePH'], testListResult['maybePhysiquePH'], testListResult['mainPhysiqueOt'], testListResult['maybePhysiqueOt'], str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))), set_conversion_score(testListPHValues, 8), set_conversion_score(testListQXValues, 8), set_conversion_score(testListYaXValues, 7), set_conversion_score(testListYiXValues, 8), set_conversion_score(testListTSValues, 8), set_conversion_score(testListSRValues, 6), set_conversion_score(testListXYValues, 7), set_conversion_score(testListQYValues, 7), set_conversion_score(testListTBValues, 7)))
            return redirect(url_for('patient_test_result', nav_name = navName[0], result_id = g.db.insert_id()))
    return redirect(url_for('login'))

# 用户注册页面
@app.route('/register/<userTyp>', methods=['GET', 'POST'])
def register(userTyp):
    if request.method == 'GET':
        if userTyp == 'patient':
            return render_template('patient_register.html', PROJECT_NAME = PROJECT_NAME)
        elif userTyp == 'doctor':
            return render_template('doctor_register.html', PROJECT_NAME = PROJECT_NAME)
        else:
            abort(404)
    else:
        typ = request.form['regType']
        registerTime = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        if typ == 'patient':
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

            return redirect(url_for('patient_test', nav_name='home'))
        elif typ == 'doctor':
            pass
        else:
            abort(404)

# 检测 Email 是否存在 URL
@app.route('/check_email_exist', methods=['POST'])
def check_email_exist():
    typ = request.form['typ']
    email = request.form['email'].strip()
    result = False
    if typ == 'patient':
        c = g.db.cursor()
        c.execute('SELECT patient_email FROM healthms_patients_info')
        patients = list(c.fetchall())
        patients.reverse()
        for patient in patients:
            if (email == patient[0]):
                result = True
                break
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
    return redirect(url_for('login'))




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
            if (email == doctor[1]) and (pwd == base64.decodestring(doctor[2])):
                result = {'result': 'success', 'userInfo': doctor}
                break
            elif (email == doctor[1]) and (pwd != base64.decodestring(doctor[2])):
                result = 'pwdError'
                break
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

def set_conversion_score(score, itemNum):
    '''接受两个参数分别为：原始分，条目数
    根据：
        原始分=各个条目分值相加
        转化分数＝[(原始分－条目数)/(条目数×4)]×100
    两个公式得出转化分, 并输出
    '''
    return (score - itemNum) / (itemNum * 4) * 100


def judge_physique(testListValues):
    '''
    # 接受一个九种体质的字典，格式为{'体质名': 转化分}；
    # 返回一个字典，分别为： mainPhysiquePH （主要体质为平和质）、
    #                     maybePhysiquePH （主要体质基本为平和质）、
    #                     mainPhysiqueOt （主要体质为其他8种体质中的一种或几种）、
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
    logging.warning(len(mainPhysiqueOtList))
    if len(mainPhysiqueOtList) > 1:
        for temp in mainPhysiqueOtList[:-1]:
            maybePhysiqueOtList.append(mainPhysiqueOtList.pop())
    if len(mainPhysiqueOtList) == 0:
        if testListPHValue >= 60:
            if not maybePhysiqueOtList:
                mainPhysiquePH = '平和质'
            else:
                maybePhysiquePH = '平和质'
    return {'mainPhysiquePH': mainPhysiquePH, 'maybePhysiquePH': maybePhysiquePH, 'mainPhysiqueOt': ''.join(mainPhysiqueOtList), 'maybePhysiqueOt': ', '.join(maybePhysiqueOtList)}

def is_max_num(numKey, num, nums):
    '''检测传入的字典 nums 中value值是否有比 num 大的数，若有返回 False；若没有返回 True'''
    flag = True
    for key, value in nums.iteritems():
        if numKey != key:
            if value > num:
                flag = False
                break
    return flag

def select_test_result(tr, isCate):
    patientTestMainResult = list()
    patientTestOtResult = list()
    c = g.db.cursor()
    c.execute('SELECT * FROM  healthms_test_characteristic')
    tcs = list(c.fetchall())
    if tr[4] == '':
        if tr[2] != '':
            patientTestMainResult.append('平和质')
        else:
            patientTestMainResult.append('基本是平和质')
        if isCate:
            for tc in tcs:
                if tc[1] == '平和质':
                    phtc = {'cName': tc[1], 'cGeneral': tc[2], 'cPhysique': tc[3], 'cExpression': tc[4], 'cPsychology': tc[5], 'cInciTend': tc[6], 'cAdaptability': tc[7], 'cIdentification': tc[8], 'cAdjust': tc[9]}
            patientTestMainResult.append(phtc)
    else:
        patientTestMainResult.append(tr[4])
        if isCate:
            for tc in tcs:
                if tc[1] == tr[4]:
                    phtc = {'cName': tc[1], 'cGeneral': tc[2], 'cPhysique': tc[3], 'cExpression': tc[4], 'cPsychology': tc[5], 'cInciTend': tc[6], 'cAdaptability': tc[7], 'cIdentification': tc[8], 'cAdjust': tc[9]}
            patientTestMainResult.append(phtc)
    if tr[5] != '':
        patientTestOtList = tr[5].split(', ')
        for patientTestOt in patientTestOtList:
            if isCate:
                for tc in tcs:
                    if tc[1] == patientTestOt:
                        patientTestOtResult.append({'patientTestOt': patientTestOt, 'patientTestCateId':tc[0]})
            else:
                patientTestOtResult.append({'patientTestOt': patientTestOt})
    return {'testResultId': tr[0], 'patientTestMainResult': patientTestMainResult, 'patientTestOtResult': patientTestOtResult, 'patientTestDate': tr[6]}
        

