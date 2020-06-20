import sys
import os
import pathlib

from flask import render_template, flash, url_for, redirect
from flask_login import login_user, logout_user, login_required,current_user
from app import app, db, lm
from werkzeug.utils import secure_filename

from app.models.Calibration import Calibration
from app.models.CalibrationFiles import CalibrationFiles
from app.models.User import User

from app.forms.CalibrationForm import CalibrationForm, CalibrationFilesForm
from app.utils.Utils import prepare

@app.route("/dados_exemplo",methods=['GET', 'POST'])
@login_required
def dados_exemplo():
    
    form = CalibrationForm()
    if form.validate_on_submit():
        # save in database
        calibration_data = Calibration(
            description = form.description.data,
            user_id = current_user.get_id()
        )
        db.session.add(calibration_data)
        db.session.commit()

        # Inserindo os dados de exemplo:
        file_path = os.path.join(os.path.dirname(__file__), '../utils/micromatter-table-iag.csv')
        calibration_files_data = CalibrationFiles(
            csv_file = 'a',
            txt_file = 'b',
            standard_target = 34662,
            calibration_id = calibration_data.id
        )
        db.session.add(calibration_files_data)
        db.session.commit()


        return redirect(url_for('showCalibration',id=calibration_data.id))
    return render_template('calibration/new.html',form=form)