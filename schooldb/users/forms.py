from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired 
## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class UserForm(FlaskForm):

    username = StringField(label = "Username", validators = [DataRequired(message = "Username is a required field.")])

    password = StringField(label = "Password", validators = [DataRequired(message = "Password is a required field.")])

    first_name = StringField(label = "First name", validators = [DataRequired(message = "First name is a required field.")])

    last_name = StringField(label = "Last name", validators = [DataRequired(message = "Last name is a required field.")])

    birthdate = StringField(label = "Birthdate", validators = [DataRequired(message = "Birthdate is a required field.")])

    address = StringField(label = "Address", validators = [DataRequired(message = "Address is a required field.") ])

    zip_code = StringField(label = "Zip Code", validators = [DataRequired(message = "Zip Code is a required field.") ])

    school = StringField(label = "School", validators = [DataRequired(message = "School name is a required field.") ])

    position = StringField(label = "Position", validators = [DataRequired(message = "Position name is a required field.") ])

    submit = SubmitField("Create")

class passform(FlaskForm):
    
    pass1 = StringField(label = "New password")
    submit = SubmitField("Submit")




class form331(FlaskForm):
    
    title = StringField(label = "Title")

    category = StringField(label = "Category")

    writer = StringField(label = "Writer")

    submit = SubmitField("Create")

class formid(FlaskForm):
    
    id = StringField(label = "User ID")
    submit = SubmitField("Submit")

class formid2(FlaskForm):
    
    id2 = StringField(label = "User ID")
    submit = SubmitField("Submit")
class formid3(FlaskForm):
    
    id3 = StringField(label = "User ID")
    submit = SubmitField("Submit")


class formbid(FlaskForm):
    
    title = StringField(label = "Book Title")
    submit = SubmitField("Submit")

class formbid2(FlaskForm):
    
    title2 = StringField(label = "Book Title")
    submit = SubmitField("Submit")

class formbid3(FlaskForm):
    
    title3 = StringField(label = "Book Title")
    submit = SubmitField("Submit")

class formbreview(FlaskForm):
    
    title = StringField(label = "Book Title")
    text =  StringField(label = "Review Text")
    rating =  StringField(label = "Rating(1-5)")
    submit = SubmitField("Submit")

class formresdel(FlaskForm):
    
    title = StringField(label = "Book Title")
    date =  StringField(label = "Reservation Date")
   
    submit = SubmitField("Submit")


class formubid(FlaskForm):
    
    uid = StringField(label = "User ID")
    bid =  StringField(label = "Book ID")
   
    submit = SubmitField("Submit")

class formubid2(FlaskForm):
    
    uid2 = StringField(label = "User ID")
    bid2 =  StringField(label = "Book ID")
   
    submit = SubmitField("Submit")

class formubid3(FlaskForm):
    
    uid3 = StringField(label = "User ID")
    bid3 =  StringField(label = "Book ID")
   
    submit = SubmitField("Submit")