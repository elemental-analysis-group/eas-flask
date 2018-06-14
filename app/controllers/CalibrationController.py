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

from app.forms.CalibrationForm import CalibrationForm, CalibrationFormFiles

import Micromatter
import WinQxas
import Shimadzu
from calculateResponseFactor import ResponseFactor

@app.route("/calibration/new",methods=['GET', 'POST'])
@login_required
def newCalibration():
    print()
    form = CalibrationForm()
    if form.validate_on_submit():

        # save in database
        calibration_data = Calibration(
            description = form.description.data,
            user_id = current_user.get_id()
        )
        db.session.add(calibration_data)
        db.session.commit()

        return redirect(url_for('showCalibration',id=calibration_data.id))

    return render_template('calibration/new.html',form=form)

@app.route("/calibration/index",methods=['GET', 'POST'])
@login_required
def indexCalibration():
    calibrations = Calibration.query.all()
    return render_template('calibration/index.html',
        calibrations=calibrations)

@app.route("/calibration",defaults={'id': 0})
@app.route("/calibration/<id>",methods=['GET', 'POST'])
@login_required
def showCalibration(id):
    form = CalibrationFormFiles()
    calibration = Calibration.query.filter_by(id=id).first()

    if form.validate_on_submit():
        begin = 'micromatter' + str(form.micromatter_id.data) + '_' + 'calibration_' + str(calibration.id) + '_'
        # csv
        csv_filename = begin + secure_filename(form.csv_file.data.filename)
        #form.csv_file.data.save(os.path.join('files', csv_filename))
        form.csv_file.data.save( app.config['FILES'] + '/' + csv_filename )

        # txt
        txt_filename = begin + secure_filename(form.txt_file.data.filename)
        #form.txt_file.data.save(os.path.join('files', txt_filename))
        form.txt_file.data.save( app.config['FILES'] + '/' + txt_filename)

        calibration_files_data = CalibrationFiles(
            csv_file = csv_filename,
            txt_file = txt_filename, 
            micromatter_id = form.micromatter_id.data, 
            calibration_id = calibration.id
        )
        db.session.add(calibration_files_data)
        db.session.commit()

        return redirect(url_for('showCalibration',id=calibration.id))

    # get all uploaded files from this calibration
    uploads = CalibrationFiles.query.filter_by(calibration_id=calibration.id).all()
    
    ######################################## TODO: migrate this code to an external function
    # adding micrommater info
    info = {}
    ResponseFactors = {}
    elements= {}
    for i in uploads:

        info[i.micromatter_id] = Micromatter.get(i.micromatter_id)

        # txt
        txt_content = pathlib.Path( app.config['FILES'] + '/' + i.txt_file).read_text()
        txt_info = WinQxas.parseTxt(txt_content)

        # csv
        csv_content = pathlib.Path( app.config['FILES'] + '/' + i.csv_file).read_text()
        csv_info = Shimadzu.parseCsv(csv_content)

        elements[i.micromatter_id] = {}
        ResponseFactors[i.micromatter_id] = {}

        elements[i.micromatter_id] = [ x for x in info[i.micromatter_id].keys() if x is not 'total']

        for element in elements[i.micromatter_id]:
            # se tiver espectro para o elemento em questão, calcula, senão passa direto
            try:
                Z = element
                density = float(info[i.micromatter_id][element])    
                N = txt_info['K']['peaks'][Z]
                ResponseFactors[i.micromatter_id][Z] = ResponseFactor(float(N),density,csv_info['current'],csv_info['livetime'])

            except:
               pass


    #####################################################################
    
    return render_template('calibration/show.html',
            calibration=calibration,
            form=form,
            info=info,
            uploads = uploads,
            ResponseFactors = ResponseFactors,
            elements = elements
    )

