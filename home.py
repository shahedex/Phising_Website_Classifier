from flask import Flask, render_template
import main
from flask import request
import csv
app = Flask(__name__)

@app.route('/')
def runpy():
    return render_template('index.html')

@app.route('/',methods=['post'])
def form_post():
    texts = request.form['text']
    textify = {'0':50}
    if texts != '':
        main.testurl = texts
        textify = main.main()
        if textify['result'] == 0:
            text = 'The website '+str(texts)+ ' does not contain any spam'
        else:
            text = 'The website '+str(texts)+ ' contains spams'
    else:
        text = 'Warning!! Website name can not be empty'
    spam = 100 - float(textify['0'])
    return render_template('index.html', text=text,hamprob=textify['0'],spamprob=spam)

@app.route('/results')
def show_result():
    with open('test_features.csv','rb') as csvfile:
        feature_list = csv.DictReader(csvfile)
        for row in feature_list:
            values = row
        print values
    return render_template('result.html',value=values)



if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug=True)
