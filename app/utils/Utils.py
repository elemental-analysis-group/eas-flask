import sys
import os
import pathlib
import shutil
from app import app, db, lm
import numpy
import pandas as pd
import math

from app.elemental_analysis_tools_temp import winqxas, micromatter, shimadzu
from app.elemental_analysis_tools_temp.responseFactor import responseFactor
from app.models.CalibrationFiles import CalibrationFiles

def load_example_data(calibration_id):

    micromatter_data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'micromatter-table-iag.csv'))

    for index, row in micromatter_data.iterrows():

        # Remover alguns serials
        #removidos = [34667,34668, 34686, 34687]
        #if(row['serial'] in removidos or row['serial'] > 34690):
        #    continue

        serial = str(row['serial'])

        # Copia os arquivos de modelo
        begin = 'calibration_' + str(calibration_id) + '_'
        txt_from = pathlib.Path(os.path.dirname(__file__)+'/example-data/txt/' + serial + '.txt')
        txt_to   = pathlib.Path(app.config['FILES'] + '/' + begin + serial + '.txt')
        shutil.copy(txt_from, txt_to)

        csv_from = pathlib.Path(os.path.dirname(__file__)+'/example-data/csv/' + serial + '.csv')
        csv_to   = pathlib.Path(app.config['FILES'] + '/' + begin + serial + '.csv')
        shutil.copy(csv_from, csv_to)

        calibration_files_data = CalibrationFiles(
            csv_file = begin + serial + '.csv',
            txt_file = begin + serial + '.txt',
            standard_target = serial,
            calibration_id = calibration_id
        )
        db.session.add(calibration_files_data)
        db.session.commit()

def prepare(uploads):
    """
    Esse método prepara as variáveis para o template:
    """
    # a ideia é que seja genérico para qualquer alvo padrão, mas por hora fixar na micromatter
    file_path = os.path.join(os.path.dirname(__file__), 'micromatter-table-iag.csv')
    micromatter_file = pathlib.Path(file_path).read_text()

    micromatter_data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'micromatter-table-iag.csv'))
    response_factors_K = pd.DataFrame(columns=['serial','Z','Y','Yerror'])
    response_factors_L = pd.DataFrame(columns=['serial','Z','Y','Yerror'])

    for i in uploads:

        # 2. Ler arquivos txt e csv correspondentes
        txt_content = pathlib.Path( app.config['FILES'] + '/' + i.txt_file).read_text()
        txt_info = winqxas.parseTxt(txt_content)

        csv_content = pathlib.Path( app.config['FILES'] + '/' + i.csv_file).read_text()
        csv_info = shimadzu.parseCsv(csv_content)

        # 3. Para os elementos que estão tabelados para ao serial em questão, fazer o cálculo do fator de resposta        
        row = micromatter_data[ micromatter_data.serial == int(i.standard_target) ]

        for j in [['element1','density1'],['element2','density2']]:
            element = row[j[0]].values[0]
            density = row[j[1]].values[0]

            if not math.isnan(element):
                try:
                    N = float(txt_info['K']['peaks'][element])       
                    sigma_N = float(txt_info['K']['errors'][element])
                    R, sigma_R = responseFactor(N, density,csv_info['current'],csv_info['livetime'],sigma_N)

                    response_factors_K = response_factors_K.append({
                        'serial': i.standard_target,
                        'Z': element , 
                        'Y': R , 
                        'Yerror': sigma_R
                        }, ignore_index=True)
                except:
                    pass

            # Vou repetir por pura preguiça... mas é o memos de cima, trocando linha K por L
                try:
                    N = float(txt_info['L']['peaks'][element])       
                    sigma_N = float(txt_info['L']['errors'][element])
                    R, sigma_R = responseFactor(N, density,csv_info['current'],csv_info['livetime'],sigma_N)

                    response_factors_L = response_factors_L.append({
                        'serial': i.standard_target,
                        'Z': element , 
                        'Y': R , 
                        'Yerror': sigma_R
                        }, ignore_index=True)
                except:
                    pass

    response_factors_K["Z"] = response_factors_K["Z"].astype(int)
    response_factors_L["Z"] = response_factors_L["Z"].astype(int)
    return response_factors_K, response_factors_L

def response_factors_medias(response_factors):
    aux = pd.DataFrame(columns=['Z','Y','Yerror'])

    elements = numpy.unique(response_factors['Z'])
    for element in elements:
        rows = response_factors[response_factors.Z == element]
        aux = aux.append({
            'Z': element , 
            'Y': rows.Y.mean() , 
            'Yerror': math.sqrt(numpy.square(rows.Yerror).sum())
        }, ignore_index=True)

    aux["Z"] = aux["Z"].astype(int)
    return aux
