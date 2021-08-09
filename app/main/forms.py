from flask_wtf import FlaskForm
from wtforms import StringField, SelectField

def generate_options():
    list_of_choices = []
    for i in range(24):
        first = ""+str(i)+":00"
        second = ""+str(i)+":15"
        third = ""+str(i)+":30"
        fourth = ""+str(i)+":45"
        list_of_choices.append(first)
        list_of_choices.append(second)
        list_of_choices.append(third)
        list_of_choices.append(fourth)

    return list_of_choices

class LoginForm(FlaskForm):
    name = StringField("name")
    password = StringField("password")

class ScheduleForm(FlaskForm):
    list_of_choices = generate_options()
    unit_co2_on = SelectField("CO2 schedule on", choices=list_of_choices)
    unit_co2_off = SelectField("CO2 schedule off", choices=list_of_choices)
    unit_o2_on = SelectField("O2 schedule on", choices=list_of_choices)
    unit_o2_off = SelectField("O2 schedule off", choices=list_of_choices)
    unit_light_on = SelectField("Light schedule on", choices=list_of_choices)
    unit_light_off = SelectField("Light schedule off", choices=list_of_choices)
    unit_temp_on = SelectField("Temp schedule on", choices=list_of_choices)
    unit_temp_off = SelectField("Temp schedule off", choices=list_of_choices)