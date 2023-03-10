from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user_model

@app.route('/')
def login_reg():
    return render_template('log_reg.html')

@app.route('/user/register', methods=['POST'])
def register_user():
    if not user_model.User.validate_register(request.form):
        return redirect('/')
    new_user= user_model.User.save_user(request.form)
    print(new_user)
    session['user_id'] = new_user
    return redirect(f'/user/{new_user}')

@app.route('/user/login', methods=['POST'])
def login_user():
    if not user_model.User.validate_login(request.form):
        return redirect('/')
    email_data={
        'email':request.form['login_email']
    }
    returning_user= user_model.User.get_user_by_email(email_data)
    session['user_id']= returning_user.id
    return redirect(f'/user/{returning_user.id}')

@app.route('/user/<int:id>')
def user_profile(id):
    if 'user_id' not in session:
        return redirect('/')
    data_dict={
        "user_id":id
    }
    logged_user =user_model.User.get_user_with_posts(data_dict)
    return render_template('user_w_blogs.html', one_user = logged_user )

@app.route('/all_users')
def all_users():
    user_model.User.get_all()
    return "look at the terminal results"

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')