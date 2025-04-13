import mlflow
import mlflow.pyfunc
import json

from flask import Flask, request, render_template
from flask_cors import cross_origin
import os

from flask_app.predictionFile import ReceiveData
import dagshub

app = Flask(__name__)

dagshub_token = os.getenv("DAGSHUB_PAT")
if not dagshub_token:
    raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

mlflow.set_tracking_uri("https://dagshub.com/SHIVRAJSHINDE/AirlineFare_EndToEnd.mlflow")

# dagshub.init(repo_owner='SHIVRAJSHINDE', repo_name='AirlineFare_EndToEnd', mlflow=True)
# os.environ['DAGSHUB_PAT'] = '6d430bde13e3d953e86bec39074f2fccd2b8595a'
# tracking_uri = "http://localhost:5000"
# mlflow.set_tracking_uri(tracking_uri)

def load_model_info() -> dict:
    """Load the model info from a JSON file."""
    if not os.path.exists('reports/experiment_info.json'):
        raise FileNotFoundError(f"Model info file not found: {'reports/experiment_info.json'}")

    with open('reports/experiment_info.json', 'r') as file:
        return json.load(file)

ModelName = "Lasso"
model_info = load_model_info()
model_uri = f"runs:/{model_info['run_id']}/{ModelName}"

# model_uri = 'runs:/b86d75382ed74105b6546b9c899fdc44/Lasso_model'

try:
    print(model_uri)
    model = mlflow.pyfunc.load_model(model_uri)

    print(model)
except Exception as e:
    print("Error loading model:", e)

@app.route("/")
@cross_origin()

def home():
    return render_template("home.html")


@app.route("/predict", methods=["GET", "POST"])
@cross_origin()

def predict():
    if request.method=="GET":
        return render_template(home.html)
    
    elif request.method=="POST":

        receiveData_Obj =  ReceiveData()
        
        df = receiveData_Obj.receive_data_from_ui_create_df(Airline = request.form.get('Airline'),
                                        Date_of_Journey = request.form.get('Date_of_Journey'),
                                        Source = request.form.get('Source'),
                                        Destination = request.form.get('Destination'),
                                        Dep_Time = request.form.get('Dep_Time'),
                                        Arrival_Time = request.form.get('Arrival_Time'),
                                        Duration = request.form.get('Duration'),
                                        Total_Stops = request.form.get('Total_Stops'))
        print(df)

        value = receiveData_Obj.execute_pipeline(df)
        prediction_value = model.predict(value)
        print("----------------------------------------------------")
        print(prediction_value)
        print("----------------------------------------------------")
        return render_template("prediction.html", prediction=prediction_value)

    return render_template("home.html")


if __name__ == "__main__":
    #app.run(debug=True, host="0.0.0.0", port=8080)
    app.run(debug=True, host="0.0.0.0")
