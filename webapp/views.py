import json
from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
from sourceCode import Data_Pre_Processing

views = Blueprint('base', __name__)

@views.route('/')
def base(): 
    return render_template('base.html')


@views.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    dataSet = pd.read_csv(uploaded_file)
    
    return render_template('home.html', attributes = list(dataSet.columns))





@views.route('/dataPreProcessing', methods=['POST'])
def dataPre():
    result =  request.get_json()
    answer = json.loads(result)
    return answer





    # buliding APIs, data analytics, proficiency in python 
    # python, docker, smart contracts (soliidty)