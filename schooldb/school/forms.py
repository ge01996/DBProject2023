from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class SchoolForm(FlaskForm):
   
    name = StringField(label = "School name", validators = [DataRequired(message = "School name is a required field.")])

    email = StringField(label = "Email", validators = [DataRequired(message = "Email is a required field."), Email(message = "Invalid email format.")])

    principal = StringField(label = "Principal", validators = [DataRequired(message = "Principal is a required field.")])

    librarian = StringField(label = "Librarian", validators = [DataRequired(message = "Librarian is a required field.")])

    city = StringField(label = "City", validators = [DataRequired(message = "City is a required field.")])

    address = StringField(label = "Address", validators = [DataRequired(message = "Address is a required field.") ])

    zip_code = StringField(label = "Zip Code", validators = [DataRequired(message = "Zip Code is a required field.") ])

    phone = StringField(label = "Phone number", validators = [DataRequired(message = "Phone number is a required field.")])

    submit = SubmitField("Create")
