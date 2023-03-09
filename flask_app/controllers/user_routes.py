from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user_model

@app.route('/')
def login_reg():
    return render_template('log_reg.html')

@app.route('/user/register', methods=['POST'])
def register_user():
    if not user_model.User.validate_user(request.form):
        return redirect('/')
    new_user= user_model.User.save_user(request.form)
    print(new_user)
    return redirect(f'/user/{new_user}')

@app.route('/user/<int:id>')
def user_profile(id):
    data_dict={
        "user_id":id
    }
    logged_user =user_model.User.get_user_with_posts(data_dict)
    return render_template('user_w_blogs.html', one_user = logged_user )
