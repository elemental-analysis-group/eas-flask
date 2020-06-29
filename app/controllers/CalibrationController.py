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
from app.utils.Utils import prepare, load_example_data

@app.route("/calibration/new",methods=['POST','GET'])
@login_required
def newCalibration():
    form = CalibrationForm()
    if form.validate_on_submit():
        calibration_data = Calibration(
            description = form.description.data,
            user_id = current_user.get_id()
        )
        db.session.add(calibration_data)
        db.session.commit()
        if(form.init_type.data == "example"):
            load_example_data(calibration_data.id)
        return redirect(url_for('showCalibration',id=calibration_data.id))
    return render_template('calibration/new.html',form=form)

@app.route("/calibration/index",methods=['GET'])
@login_required
def indexCalibration():
    calibrations = Calibration.query.all()
    return render_template('calibration/index.html',calibrations=calibrations)

@app.route("/calibration/<id>",methods=['POST','GET'])
@login_required
def showCalibration(id):
    form = CalibrationFilesForm()
    calibration = Calibration.query.filter_by(id=id).first()
    
    if form.validate_on_submit():

        # pattern to filenames: calibration_ID_filename.txt|csv
        begin = 'calibration_' + str(calibration.id) + '_'

        # csv
        csv_filename = begin + secure_filename(form.csv_file.data.filename)
        form.csv_file.data.save( app.config['FILES'] + '/' + csv_filename )

        # txt
        txt_filename = begin + secure_filename(form.txt_file.data.filename)
        form.txt_file.data.save( app.config['FILES'] + '/' + txt_filename)

        # save filename and location on database
        calibration_files_data = CalibrationFiles(
            csv_file = csv_filename,
            txt_file = txt_filename,
            standard_target = form.standard_target.data,
            calibration_id = calibration.id
        )
        db.session.add(calibration_files_data)
        db.session.commit()

        return redirect(url_for('showCalibration',id=calibration.id))

    
    # get all uploaded files from this calibration
    uploads = CalibrationFiles.query.filter_by(calibration_id=calibration.id).all()
    
    response_factors = prepare(uploads)

    return render_template('calibration/show.html',
            calibration=calibration,
            form=form,
            uploads = uploads,
            response_factors = response_factors
    )
