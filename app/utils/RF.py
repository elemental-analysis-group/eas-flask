import sys
import os
import pathlib
from app import app, db, lm

#import micromatter
#import winqxas
#import shimadzu
#from responseFactor import responseFactor

def RF(uploads):
    info = {}
    ResponseFactors = {}
    elements= {}
#    for i in uploads:

#        info[i.micromatter_id] = Micromatter.get(i.micromatter_id)

        # txt
#        txt_content = pathlib.Path( app.config['FILES'] + '/' + i.txt_file).read_text()
#        txt_info = winqxas.parseTxt(txt_content)

        # csv
#        csv_content = pathlib.Path( app.config['FILES'] + '/' + i.csv_file).read_text()
#        csv_info = shimadzu.parseCsv(csv_content)

#        elements[i.micromatter_id] = {}
#        ResponseFactors[i.micromatter_id] = {}

#        elements[i.micromatter_id] = [ x for x in info[i.micromatter_id].keys() if x is not 'total']

#        for element in elements[i.micromatter_id]:
            # se tiver espectro para o elemento em questão, calcula, senão passa direto
#            try:
#                Z = element
#                density = float(info[i.micromatter_id][element])    
#                N = txt_info['K']['peaks'][Z]
#                ResponseFactors[i.micromatter_id][Z] = ResponseFactor(float(N),density,csv_info['current'],csv_info['livetime'])

#            except:
#               pass

#    return (info, ResponseFactors, elements)
    return ('')
