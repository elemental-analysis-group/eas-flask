import sys
import os
import pathlib
from app import app, db, lm
import numpy
import pandas as pd 

from app.elemental_analysis_tools_temp import winqxas, micromatter, shimadzu
from app.elemental_analysis_tools_temp.responseFactor import responseFactor
from app.models.CalibrationFiles import CalibrationFiles

def load_example_data(calibration_id):

    micromatter = pd.read_csv(os.path.join(os.path.dirname(__file__), 'micromatter-table-iag.csv'))
    for index, row in micromatter.iterrows():
        serial = str(row['serial'])
        calibration_files_data = CalibrationFiles(
            csv_file = 'example/csv/' + serial + '.csv',
            txt_file = 'example/txt/' + serial + '.txt',
            standard_target = serial,
            calibration_id = calibration_id
        )
        db.session.add(calibration_files_data)
        db.session.commit()
        

    calibration_files_data = CalibrationFiles(
        csv_file = 'example/csv/34662.csv',
        txt_file = 'example/txt/34662.txt',
        standard_target = 34662,
        calibration_id = calibration_id
    )
    db.session.add(calibration_files_data)
    db.session.commit()

def prepare(uploads):
    """
    Esse método prepara as variáveis para o template:
    elements: 
    info: Informações dos alvos de calibração, no caso, por enquanto da micromatter
     ResponseFactors, 
    """
    info = {}
    ResponseFactors = {}
    ResponseFactorsErrors = {}
    elements = {}
    uploads_metadata = {}

    Z = []
    Y = []
    Yerror = []

    for i in uploads:
        # a ideia é que seja genérico para qualquer alvo padrão, mas por hora fixar na micromatter
        file_path = os.path.join(os.path.dirname(__file__), 'micromatter-table-iag.csv')
        micromatter_file = pathlib.Path(file_path).read_text()

        info[i.standard_target] = micromatter.get(i.standard_target, micromatter_file)

        # txt
        txt_content = pathlib.Path( app.config['FILES'] + '/' + i.txt_file).read_text()
        txt_info = winqxas.parseTxt(txt_content)

        # csv
        csv_content = pathlib.Path( app.config['FILES'] + '/' + i.csv_file).read_text()
        csv_info = shimadzu.parseCsv(csv_content)

        elements[i.standard_target] = {}
        ResponseFactors[i.standard_target] = {}
        ResponseFactorsErrors[i.standard_target] = {}

        elements[i.standard_target] = [ x for x in info[i.standard_target].keys() if x is not 'total' ]

        for element in elements[i.standard_target]:
            # se tiver espectro para o elemento em questão, calcula, senão passa direto
            try:
                density = float(info[i.standard_target][element])
                N = float(txt_info['K']['peaks'][element])
                sigma_N = float(txt_info['K']['errors'][element])

                R, sigma_R = responseFactor(N,density,csv_info['current'],csv_info['livetime'],sigma_N)

                ResponseFactors[i.standard_target][element] = R
                ResponseFactorsErrors[i.standard_target][element] = sigma_R

                Z.append(float(element))
                Y.append(R)
                Yerror.append(sigma_R)               

            except:
               pass

    # ATENÇÃO: Falta tirar média
    response_factors_final = {'Z': Z , 'Y': Y , 'Yerror': Yerror}

    return (info, elements, ResponseFactors, ResponseFactorsErrors, response_factors_final)
