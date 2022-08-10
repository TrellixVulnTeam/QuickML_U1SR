import os
import json
from tabulate import tabulate
from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd
from sklearn import datasets
from sourceCode import Data_Pre_Processing as DPP

# Defining 'views' blueprint. 
# It is registered in webapp/__init__.py
views = Blueprint('base', __name__)

# Constants to be used when user submitted file is stored
UPLOAD_FOLDER = '/home/user/Documents/git/QuickML/sourceCode'
ALLOWED_EXTENSIONS = {'csv'}

# Making 'filename' writeable by defining it in the global scope. 
filename = ''

# Returns base page - starting point of application
@views.route('/')
def base(): 
    return render_template('base.html')

# Invoked when user submits file - 
# creates HTML table with attributes of file
@views.route('/', methods=['POST'])
def upload_file():
    global filename
    file = request.files['file']
    dataSet = pd.read_csv(file)
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    filename = file.filename
    return render_template('home.html', attributes = list(dataSet.columns))


# Invoked when user submits variable mapping 
@views.route('/dataPreProcessing', methods=['POST'])
def dataPre():
    # result is the variable mapping in a JSON format
    result =  request.get_json()

    # Dataset and variable mapping to be passed into the data
    # pre-processing function
    varMap = json.loads(result)
    file = os.path.join(UPLOAD_FOLDER, filename)

    table = DPP.dataPreProcess(file, varMap)

    # Getting the individual components of pre processed data 
    # to keep a reference to them for when they need to be passed 
    # in to the selected algorithm.
    xTest = pd.DataFrame(table['X_test'])
    xTrain = pd.DataFrame(table['X_train'])
    yTest = pd.DataFrame(table['y_test'])
    yTrain = pd.DataFrame(table['y_train'])   

    # Creating variables to store file names and locations for pre 
    # processed data locations
    fN_xT = '/home/user/Documents/git/QuickML/pre_processed_data/xTest'
    fN_xTr = '/home/user/Documents/git/QuickML/pre_processed_data/xTrain'
    fN_yT = '/home/user/Documents/git/QuickML/pre_processed_data/yTest'
    fN_yTr = '/home/user/Documents/git/QuickML/pre_processed_data/yTrain'

    # pd.to_csv creates the file if it does not exist, but it does not 
    # create any non existent directories. The pre_processed_data directory 
    # already exists, pd.to_csv <i>creates</i> the files and populates them 
    # with the contents of their respective components. 
    xTest.to_csv(fN_xT)
    xTrain.to_csv(fN_xTr)
    yTest.to_csv(fN_yT)
    yTrain.to_csv(fN_yTr)

    # Getting the file out of the whole path and converting it to a dataframe.
    dF = pd.read_csv(file.split('/')[-1])
    
    # Columns still hard coded! Fix before deploying to production. 
    col = dF.columns

    # return formattes string which contains HTML and HTML tables using 
    # the 'tabulate' module
    return (f'''
            <h2 style="text-align:center">Scroll to Preview your Pre-Processed Data!</h2>
            <hr>
            <div>
                <h3 style="text-align:left"> X train </h3> 
                <h3 style="text-align:right; margin-top:-40px"> Y train </h3> <hr><br>
                <div class="container" style="display:flex; width=70%">
                    {tabulate(table['X_train'], tablefmt='html', headers = col)}
                    {tabulate(table['y_train'], tablefmt='html', headers = col[4:])}
                </div>
                <hr>
                <h3 style="text-align:left"> X test </h3> 
                <h3 style="text-align:right; margin-top:-40px"> Y test </h3> <hr><br>
                <div class="container" style="display:flex; width=70%">
                    {tabulate(table['X_test'], tablefmt='html', headers = col)}
                    {tabulate(table['y_test'], tablefmt='html', headers = col[4:])}
                </div>
            </div>
    ''' )
    # buliding APIs, data analytics, proficiency in python 
    # python, docker, smart contracts (soliidty)

@views.route('/Results', methods=["POST"])
def confusionMatrix():
    return render_template("results.html")