from flask import Flask,render_template,request,redirect
from flask_cors import CORS,cross_origin
import pickle
import pandas as pd
import numpy as np

app=Flask(__name__)
cors=CORS(app)
model=pickle.load(open('model.pkl','rb'))
df2=pd.read_csv('flight_cleaned.csv')

@app.route('/',methods=['GET','POST'])
def index():
    
    airline=df2['airline'].unique()
    source_city=df2['source_city'].unique()
    departure_time=df2['departure_time'].unique()
    stops=df2['stops'].unique()
    arrival_time=df2['arrival_time'].unique()
    destination_city=df2['destination_city'].unique()
    classes=df2['classes'].unique()
    duration=df2['duration'].unique()
    days_left=df2['days_left'].unique()

    return render_template('index.html',airline=airline, source_city=source_city, departure_time=departure_time,stops=stops,arrival_time=arrival_time,destination_city=destination_city,classes=classes,duration=duration,days_left=days_left)


@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():

    airline=request.form.get('airline')
    source_city=request.form.get('source_city')
    departure_time=request.form.get('departure_time')
    stops=request.form.get('stops')
    arrival_time=request.form.get('arrival_time')
    destination_city=request.form.get('destination_city')
    classes=request.form.get('classes')
    duration=request.form.get('duration')
    days_left=request.form.get('days_left')

    prediction=model.predict(pd.DataFrame(columns=['airline', 'source_city', 'departure_time', 'stops', 'arrival_time','destination_city', 'classes', 'duration', 'days_left'],
                              data=np.array([airline,source_city,departure_time,stops,arrival_time,destination_city,classes,duration,days_left]).reshape(1, 9)))
    print(prediction)

    return str(np.round(prediction[0],2))



if __name__=="__main__":
    app.run(debug=True, host = "0.0.0.0",  port = 3000)