# This script generates the scoring and schema files
# necessary to operationalize the Iris Classification sample
#Init and run functions
from azure.ml.api.schema.dataTypes import DataTypes
from azure.ml.api.schema.sampleDefinition import SampleDefinition
from azure.ml.api.realtime.services import generate_schema
import pandas

# Prepare the web service definition by authoring
# init() and run() functions. Test the functions
# before deploying the web service.
def init():
    from sklearn.externals import joblib

    # load the model file
    global model
    model = joblib.load('model.pkl')

def run(input_df):
    import json
    
    # append 40 random features just like the training script does it.
    import numpy as np
    n = 40
    random_state = np.random.RandomState(0)
    n_samples, n_features = input_df.shape
    input_df = np.c_[input_df, random_state.randn(n_samples, n)]

    pred = model.predict(input_df)
    return json.dumps(str(pred[0]))

df = pandas.DataFrame(data=[[3.0, 3.6, 1.3, 0.25]], columns=['sepal length', 'sepal width','petal length','petal width'])
df.dtypes
df

init()
input1 = pandas.DataFrame([[3.0, 3.6, 1.3, 0.25]])
run(input1)

inputs = {"input_df": SampleDefinition(DataTypes.PANDAS, df)}
# The prepare statement writes the scoring file (main.py) and
# the schema file (service_schema.json) the the output folder.
generate_schema(run_func=run, inputs=inputs, filepath='service_schema.json')
