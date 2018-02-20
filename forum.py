from flask import Flask, render_template,request, redirect, url_for,session
import config
from models import User, Question, Comment
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    context = {
        # - shows that it's from big to small.
        'getQuestion': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        #attention: 'telephone' is the login.html/input:name="telepthone"
        un = request.form.get('username')
        pw = request.form.get('password')
        userinfo = User.query.filter(User.username == un, User.password == pw).first()
        if userinfo:
            #set up a cookie, next we can be easy to know who wants to login.
            session['user_id'] = userinfo.id
            #you don't need to login in 10 days
            session.pernanent = True
            return redirect(url_for('index'))
        else:
            #return "phone number or password is not correct! try again!"
            return redirect(url_for('login'))



@app.route('/regist/', methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #we should confirm the telephone number, if it's used by people, then people can't use it to register again.
        #inport
        userPhone = User.query.filter(User.telephone == telephone).first()
        if userPhone:
            return "It has existed ! Please use other phone number."
        else:
            #pw1 must be equal to pw2
            if password1 != password2:
                return "password is not same! Try again!"
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                #import redirect method
                return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/questionAndAnswer/', methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>', methods=['GET','POST'])
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    # question is in the templates.
    return render_template('detail.html', question2=question_model)

@app.route('/add_comment/', methods=['POST'])
@login_required
def add_comment():
    content = request.form.get('add_comment_templates')
    question_id = request.form.get('question_id')

    answer = Comment(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    answer.author =  user
    question = Comment.query.filter(Comment.id == question_id).first()
    answer.qeustion = question
    db.session(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))

if __name__ == '__main__':
    app.run()
