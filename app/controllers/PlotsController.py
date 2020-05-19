import random
from io import BytesIO

from app import app
from flask import Flask, make_response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask_login import login_user, logout_user, login_required,current_user

from app.models.Calibration import Calibration
from app.models.CalibrationFiles import CalibrationFiles
from app.utils.Utils import prepare

from elemental_analysis_tools.fitResponseFactor import plotFit

@app.route("/plot/<id>",methods=['GET', 'POST'])
@login_required
def plot(id):

    calibration = Calibration.query.filter_by(id=id).first()
    uploads = CalibrationFiles.query.filter_by(calibration_id=calibration.id).all()
    info, elements, ResponseFactors, ResponseFactorsErrors,response_factors_final = prepare(uploads)

    Z = response_factors_final['Z']
    Y = response_factors_final['Y']
    Yerror = response_factors_final['Yerror']
    plt = plotFit(Z,Y,Yerror,start=11,end=50,degree=10,fit=False)
    fig = plt.gcf()

    # Faz a mágica para devolver um response do tipo imagem
    canvas = FigureCanvas(fig)
    output = BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response
