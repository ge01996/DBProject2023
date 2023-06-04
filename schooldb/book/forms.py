from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired,  NumberRange

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class BookForm(FlaskForm):
    
    isbn = StringField(label = "Isbn", validators = [DataRequired(message = "ISBN is a required field.")])

    title = StringField(label = "Title", validators = [DataRequired(message = "Title  is a required field.")])

    publisher = StringField(label = "Publisher", validators = [DataRequired(message = "Publisher  is a required field.")])

    summary = StringField(label = "Summary", validators = [DataRequired(message = "Summary is a required field.")])

    lang = StringField(label = "Language", validators = [DataRequired(message = "Language is a required field.")])

    pages = StringField(label = "Pages", validators = [DataRequired(message = "Number of pages is a required field.")])

    school = StringField(label = "School", validators = [DataRequired(message = "School ID is a required field.") ])

    copies = StringField(label = "Copies", validators = [DataRequired(message = "Number of cupies is a required field.") ])
   
    submit = SubmitField("Create")


class BookForm3(FlaskForm):
    
   
    id = StringField(label = "Book ID", validators = [DataRequired(message = "Book ID is a required field.")])

    school3 = StringField(label = "School ID", validators = [DataRequired(message = "School ID is a required field.") ])

    copies3 = StringField(label = "Copies", validators = [DataRequired(message = "Number of cupies is a required field.") ])
   
    submit = SubmitField("Create")
