from flask import Flask, render_template, session, redirect, url_for, request, escape
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
app.secret_key = b'kjkl3jk35jk3xciifo'
db = SQLAlchemy(app)



@app.route('/')
def root():
    if 'uid' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

### authentication ###
@app.route('/login', methods=['GET','POST'])
def login():
    # login code based on InLectureDemo1.py
    if request.method == 'POST':
        sql = """
            SELECT *
            FROM users
            """
        results = db.engine.execute(text(sql))
        for result in results:
            if result['username'] == request.form['username']:
                if result['password'] == request.form['password']:
                    session['uid'] = result['uid']
                    # record user_type for easy permission check
                    session['user_type'] = result['user_type']
                    return redirect(url_for('home'))
        # invalid credentials
        return render_template('login.msg.invalid_uspw.html')
    # if the user has logged in, redirect to homepage
    elif 'uid' in session:
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('uid', None)
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        newUserRole = request.form['role']
        newFirstName = request.form['first_name']
        newLastName = request.form['last_name']
        newUsername = request.form['username']
        newPassword = request.form['password']
        # username must be unique
        if newUsername in get_current_users():
            return render_template('signup.msg.username_taken.html')
        else:
            sql = """
                INSERT INTO users (user_type, username, password, first_name, last_name)
                VALUES ("{}", "{}", "{}", "{}", "{}")
                """.format(newUserRole, newUsername, newPassword, newFirstName, newLastName)
            db.engine.execute(text(sql))
            # if the new user has role student, add an entry in grades table to 
            # prevent crash when get_grades_by_id() is called
            if newUserRole == 'student':
                # the uid of new student user
                sql = """
                SELECT uid
                FROM users
                WHERE username == "{}"
                """.format(newUsername)
                newuid = db.engine.execute(text(sql)).fetchone()[0]
                # add an entry in grades table
                sql = """
                    INSERT INTO grades (uid)
                    VALUES ("{}")
                    """.format(newuid)
                db.engine.execute(text(sql))
            # require the user to log in with newly created credentials            
            return render_template('login.msg.login_with_new_account.html')
    elif 'uid' in session:
        return redirect(url_for('home'))
    else:
        return render_template('signup.html')

# guest user should not have access to the following pages
### course materials ###
@app.route('/home')
def home():
    try:
        # greet the user on homepage
        sql = """
        SELECT first_name
        FROM users
        WHERE uid == {}
        """.format(session['uid'])
        results = db.engine.execute(text(sql)).fetchone()
        return render_template('index2.html', first_name = results[0])
    except:
        return redirect(url_for('login'))

@app.route('/assignments')
def assignments():
    return render_template('assignments2.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar2.html')

@app.route('/courseteam')
def courseteam():
    return render_template('courseteam2.html')

# redirect the user to different page based on their user_type
@app.route('/feedback')
def feedback_redirect():
    try:
        if session['user_type'] == 'student':
            return redirect(url_for('studentfeedback'))
        elif session['user_type'] == 'instructor':
            return redirect(url_for('allstudentfeedbacks_v2'))
    except:
        return redirect(url_for('login'))

@app.route('/labs')
def labs():
    return render_template('labs2.html')

@app.route('/lectures')
def lectures():
    return render_template('lectures2.html')

# redirect the user to different page based on their user_type
@app.route('/grade')
def grade_redirect():
    try:
        if session['user_type'] == 'student':
            return redirect(url_for('studentgrades'))
        elif session['user_type'] == 'instructor':
            return redirect(url_for('allstudentgrades'))
    except:
        return redirect(url_for('login'))


### Student Users specific functions ###
@app.route('/studentfeedback', methods=['GET', 'POST'])
def studentfeedback():
    if request.method == 'POST':
        # convert ImmutableMultiDict to standard python dict
        form_data_but_in_dict = request.form.to_dict()
        # extract instructor_uid from the dict first
        print(form_data_but_in_dict)
        instructor_uid = form_data_but_in_dict.pop('instructor_uid')
        columns = 'uid'
        values = str(instructor_uid)
        # make sure the responses are recorded to the right questions
        for key in form_data_but_in_dict.keys():
            columns += ', ' + key
            values += ", '" + str(form_data_but_in_dict[key]) + "'"
        sql = """
        INSERT INTO student_feedback ({})
        VALUES ({})
        """.format(columns, values)
        db.engine.execute(text(sql))
        return render_template('studentfeedback_v2.success.html', instructors=get_uids_and_names_by_type("instructor"), questions=get_all_feedback_questions())
    else:
        return render_template('studentfeedback_v2.html', instructors=get_uids_and_names_by_type("instructor"), questions=get_all_feedback_questions())

@app.route('/studentgrades')
def studentgrades():
    try:
        student_uid = session['uid']
        print(get_grades_by_id(student_uid))
        print(get_pretty_grade())
        return render_template("studentgrades.html", pretty_names=get_pretty_grade(), student_grades=get_grades_by_id(student_uid), remark_message="")
    except:
        return redirect(url_for('login'))


@app.route('/submit_remark_request', methods=['GET', 'POST'])
def studentremarkrequest():
    try:
        student_uid = session['uid']
    except:
        return redirect(url_for('login'))
    try:
        if request.method == 'POST':
            grade_db_name = request.form['grade_db_name']
            remark_reason = request.form['remark_reason']
            # insert value to db
            sql = """
                INSERT INTO remark_request (uid, grade_name, reason)
                VALUES ({}, "{}", "{}")
                """.format(student_uid, grade_db_name, remark_reason)
            db.engine.execute(text(sql))
            return render_template("studentgrades.html", pretty_names=get_pretty_grade(), student_grades=get_grades_by_id(student_uid), remark_message="Remark request submitted")
        elif request.method == 'GET':
            if session['user_type'] == 'instructor':
                return redirect(url_for('allstudentremarkrequests'))
            else:
                return redirect(url_for('studentgrades'))
    except:
        return render_template("studentgrades.html", pretty_names=get_pretty_grade(), student_grades=get_grades_by_id(student_uid), remark_message="You have already submitted a remark request for this grade")

### Instructor Users specific functions ###
@app.route('/allstudentgrades')
def allstudentgrades():
    uid_names = get_uids_and_names_by_type("student")
    # grade_dict =  {uid: {fullname: "student name", quiz1: int(), ...}}
    grade_dict = dict()
    for uid_key in uid_names.keys():
        uid_dict = dict()
        # get all grades by that uid
        uid_dict['fullname'] = uid_names[uid_key]
        grades = get_grades_by_id(uid_key)
        for grade_key in grades:
            uid_dict[grade_key] = grades[grade_key]
        grade_dict[uid_key] = uid_dict
    table_headers = get_pretty_grade()
    html_table_headers = ["Student Name", "UID"]
    for item in table_headers:
        html_table_headers.append(table_headers[item])
    message = request.args.get('message') # used to determine if a grade was successfully changed
    return render_template('allstudentgrades.html', table_header=html_table_headers, grade_dict=grade_dict, uids=get_uids_and_names_by_type('student'), grades=get_pretty_grade(), message=message)

@app.route('/allstudentfeedbacks')
def allstudentfeedbacks_v2():
    if ('uid' in session):
        instructor_uid = session['uid']
        questions = get_all_feedback_questions()
        responses = get_all_student_feedbacks_v2(instructor_uid)
        return render_template('allstudentfeedbacks.html', questions=questions, responses=responses, instructor_name=get_fullname_by_uid(instructor_uid))
    else:
        return redirect(url_for('login'))

@app.route('/allremarkrequests')
def allstudentremarkrequests():
    # get all remark requests
    sql = """
    SELECT *
    FROM remark_request
    """
    # get pretty grade names
    grade_names = get_pretty_grade()
    # group by grade_name
    # {grade_name: {uid: [fullname, reason, status]}}
    remark_requests = dict()
    for key in grade_names.keys():
        group_by_uid = dict()
        for item in db.engine.execute(text(sql)):
            if item[1] == key:
                if item[3] == 1:
                    status = 'Closed'
                else:
                    status = 'Open'
                group_by_uid[item[0]] = [get_fullname_by_uid(item[0]), item[2], status]
        if len(group_by_uid) > 0:
            remark_requests[key] = group_by_uid
    return render_template('allremarkrequests.html', remark_requests=remark_requests, pretty_names=grade_names)



@app.route('/change_student_grade', methods=["GET","POST"])
def change_student_grade():
    # keep the redirection on the back-end since can't use inline js to redirect as per assignment rules
    if session['user_type'] == 'student':
        return redirect(url_for('home'))
    elif session['user_type'] == 'instructor':
    # this assumes all input values are legal
        if request.method == 'POST':
            student_uid = request.form['student_uid']
            assignment_to_change = request.form['grade_db_name']
            mark = request.form['changed_mark']
            sql = """
                UPDATE grades
                SET {} = {}
                WHERE uid == {}
                """.format(assignment_to_change, mark, student_uid)
            db.engine.execute(text(sql))

            table_headers = get_pretty_grade()
            html_table_headers = ["Student Name", "UID"]
            for item in table_headers:
                html_table_headers.append(table_headers[item])
            # probably should just return a string like 'success'
            # return render_template('basicchangegrade.html', message="success", grades=get_pretty_grade(), uids=get_uids_and_names_by_type("student"))
            return redirect(url_for('allstudentgrades', message="success"))
        else:
            return redirect(url_for('grade_redirect'))
    else:
        return redirect(url_for('home'))

@app.route('/change_student_remark_request_status', methods=["GET","POST"])
def change_student_remark_request_status():
    # this assumes all input values are legal
    if request.method == 'POST':
        student_uid = request.form['student_uid']
        grade_name = request.form['grade_name']
        sql = """
            UPDATE remark_request
            SET closed = 1
            WHERE uid == {} AND grade_name == "{}"
            """.format(student_uid, grade_name)
        db.engine.execute(text(sql))
        return redirect(url_for('allstudentremarkrequests'))
    else:
        return redirect(url_for('allstudentremarkrequests'))

### helper functions ###
def get_uids_and_names_by_type(user_type):
    """
    returns a dict with the following structure
    {uid1: "firstname1 lastname1", uid2: "firstname2 lastname2", ...}
    where user_type == "student" or "instructor
    """
    if user_type == "instructor" or user_type == "student":
        sql = """
        SELECT uid, first_name, last_name
        FROM users
        WHERE user_type == "{}"
        """.format(user_type)
        uid_firstname_lastname_obj = db.engine.execute(text(sql))
        uid_firstname_lastname = dict()
        for result in uid_firstname_lastname_obj:
            uid_firstname_lastname[result[0]] = str(result[1]) + ' ' + str(result[2])
        return uid_firstname_lastname

def get_grades_by_id(uid):
    """
    return a dict with grades by uid
    this function assumes a student has grades
    if not this will crash
    """
    sql = """
    SELECT *
    FROM grades
    WHERE uid = {}""".format(uid)
    grade_obj = db.engine.execute(text(sql)).fetchone()
    table_headers = get_table_headers("grades")
    i = 0
    grade_by_uid = dict()
    while i < len(grade_obj):
        grade_by_uid[table_headers[i]] = grade_obj[i]
        i = i + 1 
    return grade_by_uid

def get_table_headers(table):
    """return the headers of a table in a list"""
    sql = """
    PRAGMA table_info({})
    """.format(table)
    table_obj = db.engine.execute(text(sql))
    table_headers = []
    for result in table_obj:
        table_headers.append(result[1])
    return table_headers

def get_pretty_grade():
    """return a dict of internal grade names and pretty grade names"""
    sql = """
    SELECT *
    FROM pretty_grades"""
    pretty_grade_obj = db.engine.execute(text(sql))
    pretty_grade = dict()
    for result in pretty_grade_obj:
        pretty_grade[result[0]] = result[1]
    return pretty_grade

def get_all_student_feedbacks_v2(instructor_uid):
    """
    given the instructor_uid, returns a dict with the following structure
        {q1: ["response from student1", "response from student2", ...], 
        q2: ["response from student1", "response from student2", ...],
        ...}
    """
    # get the internal name of the questions in db
    table_headers = get_table_headers("student_feedback")
    # remove uid from the list of questions
    table_headers.remove("uid")
    feedbacks = dict()
    for question in table_headers:
        sql = """
        SELECT {}
        FROM student_feedback
        WHERE uid == {}""".format(question ,instructor_uid)
        responses_obj = db.engine.execute(text(sql))
        responses = list()
        for response in responses_obj:
            responses.append(response[0])
        feedbacks[question] = responses
    return feedbacks

def get_all_feedback_questions():
    """
    we store the feedback questions the same way as we store the students responses
    but the questions are stored in a row with uid -1
    """
    return get_all_student_feedbacks_v2("-1")

def get_fullname_by_uid(uid):
    """get a user's full name given a uid"""
    sql = """
    SELECT first_name, last_name
    FROM users
    WHERE uid == {}""".format(uid)
    fullname_obj = db.engine.execute(text(sql))
    fullname = str()
    for item in fullname_obj:
        fullname = item[0] + ' ' + item[1]
    return fullname

def get_current_users():
    """return a list of usernames in the db"""
    sql = """
        SELECT username
        FROM users
        """
    results = db.engine.execute(text(sql))
    list_of_users = list()
    for result in results:
        list_of_users.append(result[0])
    return list_of_users

def escape_characters(old_string):
    """
    Add escape_special characters to prevent crash in sqlite
    """
    print(old_string)
    new_string = str()
    for char in old_string:
        # the only case that is easy to fix
        if char == "'":
            new_string += "'"
        new_string += char
    print(new_string)
    return new_string

if __name__ == '__main__':
    app.run()