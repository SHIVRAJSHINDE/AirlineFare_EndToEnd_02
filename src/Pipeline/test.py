from mlflow.tracking import MlflowClient
import mlflow
import dagshub

mlflow.set_tracking_uri("https://dagshub.com/SHIVRAJSHINDE/AirlineFare_EndToEnd.mlflow")
dagshub.init(repo_owner='SHIVRAJSHINDE', repo_name='AirlineFare_EndToEnd', mlflow=True)


client = MlflowClient()
models = [m.name for m in client.search_registered_models()]
print("Registered Models:", models)
