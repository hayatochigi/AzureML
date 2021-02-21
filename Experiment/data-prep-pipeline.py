
# %%
import numpy as np
import pandas as pd
from azureml.core import Workspace, Run


# Get dataset from azureml

new_run = Run.get_context()
ws = new_run.experiment.workspace
dataset = new_run.input_datasets['loan_dataset'].to_pandas_dataframe()
#dataset = pd.read_csv('../data/Loan Approval Prediction.csv')

# %%
dataset = dataset.dropna()
status = dataset['Loan_Status']
status = status.map({'N': 0, 'Y':1})
dataset = dataset.drop(columns=['Loan_Status'], axis=1)

cat_list = []
for col in dataset.columns:
    if np.dtype(dataset[col]) == 'object':
        cat_list.append(col)

dataset = pd.get_dummies(dataset, columns=cat_list, drop_first=True)

dataset = pd.concat([dataset, status], axis=1)
from argparse import ArgumentParser as argp
parser = argp()
parser.add_argument('--datafolder', type=str)
args = parser.parse_args()

import os
os.makedirs(name=args.datafolder, exist_ok=True)
path = os.path.join(args.datafolder, 'defaults_prep.csv')
dataset.to_csv(path, index=False)

# %%
