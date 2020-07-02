import random
from io import BytesIO
from io import StringIO

from app import app
from flask import Flask, make_response, redirect, request, send_file, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask_login import login_user, logout_user, login_required,current_user

from app.models.Calibration import Calibration
from app.models.CalibrationFiles import CalibrationFiles
from app.utils.Utils import prepare, response_factors_medias

from app.elemental_analysis_tools_temp.fitResponseFactor import plotFit, fitResponseFactor

@app.route("/plot/K/<id>",methods=['GET', 'POST'])
@login_required
def plotK(id):

    grau = request.args.get('grau_K',1,int)
    fit=False
    if grau != 1:
        fit = True

    calibration = Calibration.query.filter_by(id=id).first()
    uploads = CalibrationFiles.query.filter_by(calibration_id=calibration.id).all()
    response_factors_K, response_factors_L = prepare(uploads)

    response_factors = response_factors_medias(response_factors_K)

    Z = response_factors['Z']
    Y = response_factors['Y']
    Yerror = response_factors['Yerror']

    plt = plotFit(Z,Y,Yerror,start=min(Z),end=max(Z),degree=int(grau),fit=fit,'K')
    fig = plt.gcf()

    # Faz a mágica para devolver um response do tipo imagem
    canvas = FigureCanvas(fig)
    output = BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

# pura preguiça...
@app.route("/plot/L/<id>",methods=['GET', 'POST'])
@login_required
def plotL(id):

    grau = request.args.get('grau_L',1,int)
    fit=False
    if grau != 1:
        fit = True

    calibration = Calibration.query.filter_by(id=id).first()
    uploads = CalibrationFiles.query.filter_by(calibration_id=calibration.id).all()
    response_factors_K, response_factors_L = prepare(uploads)

    response_factors = response_factors_medias(response_factors_L)

    Z = response_factors['Z']
    Y = response_factors['Y']
    Yerror = response_factors['Yerror']

    plt = plotFit(Z,Y,Yerror,start=min(Z),end=max(Z),degree=int(grau),fit=fit,'L')
    fig = plt.gcf()

    # Faz a mágica para devolver um response do tipo imagem
    canvas = FigureCanvas(fig)
    output = BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
    

@app.route("/export/<line>/<id>",methods=['GET'])
@login_required
def download(line,id):

    grau = request.args.get('grau',0,int)

    calibration = Calibration.query.filter_by(id=id).first()
    uploads = CalibrationFiles.query.filter_by(calibration_id=calibration.id).all()
    response_factors_K, response_factors_L = prepare(uploads)

    if line == 'K':
        response_factors = response_factors_medias(response_factors_K)
    else:
        response_factors = response_factors_medias(response_factors_L)

    Z = response_factors['Z']
    Y = response_factors['Y']
    Yerror = response_factors['Yerror']

    export = fitResponseFactor(Z,Y,Yerror,start=min(Z),end=max(Z),degree=int(grau))['export']
    print(export)

    # Retorno do csv
    output = StringIO()
    filename = line + ".csv"
    export.to_csv(output, header=False, index=False, encoding='utf-8')
    csv_output = output.getvalue()
    output.close()

    resp = make_response(csv_output)
    resp.headers["Content-Disposition"] = ("attachment; filename=%s" % filename)
    resp.headers["Content-Type"] = "text/csv"
    return resp
