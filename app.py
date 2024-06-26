from flask import Flask, render_template,request
import re
from nltk.stem import WordNetLemmatizer
import pickle

wo = WordNetLemmatizer()

app = Flask(__name__)

def preprocess(data):
    #preprocess
    a = re.sub('[^a-zA-Z]',' ',data)
    a = a.lower()
    a = a.split()
    a = [wo.lemmatize(word) for word in a ]
    a = ' '.join(a)
    return a


tfidf_vectorizer = pickle.load(open('vectorizer.pkl','rb'))
model =  pickle.load(open('prediction.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods= ['POST'])
def predict():
    msg = request.form['mood_pred']
    if msg == '':
        return render_template('index.html', pred = "Please enter a message")
    else:
        a = preprocess(msg)
        result = model.predict(tfidf_vectorizer.transform([a]))[0]
        if result == 1:
            return render_template('index.html',pred = "You are Depressed")
        if result == 0:
            return render_template('index.html',pred = "You are Not Depressed")

if __name__ == '__main__':
    app.run(debug=True)