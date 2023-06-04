from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired,  NumberRange

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class WriterForm(FlaskForm):
    
    name = StringField(label = "name", validators = [DataRequired(message = "Name is a required field.")])

    book = StringField(label = "book", validators = [DataRequired(message = "Book id is a required field.")])

    submit = SubmitField("Create")
