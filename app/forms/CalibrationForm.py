from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextField, FieldList, SelectField
from wtforms.validators import DataRequired, InputRequired, Optional
from flask_wtf.file import FileField, FileRequired, FileAllowed

import sys
import os
import pathlib
from app.elemental_analysis_tools_temp import micromatter

class CalibrationForm(FlaskForm):
    description = TextField('description', validators=[DataRequired()])
    init_type = TextField('init_type',validators=[Optional()])

class CalibrationFilesForm(FlaskForm):
    csv_file = FileField(validators=[FileRequired(),FileAllowed(['csv'], 'csv only!')])
    txt_file = FileField(validators=[FileRequired(),FileAllowed(['txt'], 'txt only!')])

    file_path = os.path.join(os.path.dirname(__file__), '../utils/micromatter-table-iag.csv')
    micromatter_file = pathlib.Path(file_path).read_text()
    choices = micromatter.serialsAsTuples(micromatter_file)

    standard_target = SelectField('standard_target',coerce=str, choices=choices, validators=[Optional()])
    
