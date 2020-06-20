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

from app.elemental_analysis_tools_temp import *

@app.route("/calibration_files/<id>",methods=['POST','GET'])
@login_required
def showCalibrationFiles(id):

    calibration_files = CalibrationFiles.query.filter_by(id=id).first()
    calibration = Calibration.query.filter_by(id=calibration_files.calibration_id).first()
    return render_template('calibration_files/show.html',
            calibration = calibration,
            calibration_files = calibration_files,
    )

@app.route("/calibration_files/<id>/delete",methods=['POST','GET'])
@login_required
def delete_calibration_files(id):
    # mantem id para redirect
    calibration_files = CalibrationFiles.query.filter_by(id=id).first()
    calibration_id = calibration_files.calibration_id

    CalibrationFiles.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(url_for('showCalibration',id=calibration_id))
