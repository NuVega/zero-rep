from flask import render_template, request, Blueprint, flash

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    user_data = None
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        hobby = request.form['hobby']
        age = request.form['age']
        if name and city and hobby and age:
            user_data = {
                'name': name,
                'city': city,
                'hobby': hobby,
                'age': age
            }
            flash('Данные успешно отправлены!', 'success')
        else:
            flash('Пожалуйста, заполните все поля.', 'danger')
    return render_template('index.html', user_data=user_data)