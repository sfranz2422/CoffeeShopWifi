from dotenv import load_dotenv
import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from csv import writer
from data import Get_Coffee_Data

load_dotenv('.env')
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Location URL',
                           validators=[DataRequired(), URL(require_tld=False, message="Must be a valid url")])
    open = StringField('Opening Time', validators=[DataRequired()])
    close = StringField('Closing Time', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', validators=[DataRequired()],
                         choices=[('✘', '✘'), ('☕', '☕'), ('☕☕', '☕☕'), ('☕☕☕', '☕☕☕'), ('☕☕☕☕', '☕☕☕☕'),
                                  ('☕☕☕☕☕', '☕☕☕☕☕')])
    wifi = SelectField('Wifi Strength', validators=[DataRequired()],
                       choices=[('✘', '✘'), ('💪', '💪'), ('💪💪', '💪💪'), ('💪💪💪', '💪💪💪'),
                                ('💪💪💪💪', '💪💪💪💪'), ('💪💪💪💪💪', '💪💪💪💪💪')])
    power = SelectField('Power Outlet Availability', validators=[DataRequired()],
                        choices=[('✘', '✘'), ('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'),
                                 ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    message = ""
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        list_of_elem = [form.cafe.data, form.location.data, form.open.data, form.close.data, form.coffee.data,
                        form.wifi.data, form.power.data]
        with open("cafe-data.csv", 'a', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(list_of_elem)
            print("csv closed")
            message = "Success"
    return render_template('add.html', form=form, message=message)


@app.route('/cafes')
def cafes():
    coffee_data = Get_Coffee_Data()
    print(coffee_data.data)
    return render_template('cafes.html', cafes=coffee_data.data)


if __name__ == '__main__':
    app.run(debug=True)
