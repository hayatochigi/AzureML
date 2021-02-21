
# %%
import numpy as np
import pandas as pd
from azureml.core import Workspace, Run
from argparse import ArgumentParser as argp

new_run = Run.get_context()
ws = new_run.experiment.workspace

parser = argp()
parser.add_argument('--datafolder', type=str)
args = parser.parse_args()

import os
import pandas as pd
os.makedirs(name=args.datafolder, exist_ok=True)
path = os.path.join(args.datafolder, 'defaults_prep.csv')
dataset = pd.read_csv(path)

X = dataset.drop(columns=['Loan_Status'])
y = dataset['Loan_Status']


from sklearn.model_selection import train_test_split
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2)


# %%
from sklearn.linear_model import LogisticRegression
reg = LogisticRegression()
reg.fit(X_tr, y_tr)
y_pred = reg.predict(X_te)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_te, y_pred)
cm_dict = {"schema_type": "confusion_matrix",
        "schema_version": "v1",
        "data": {"class_labels": ["0", "1"],
                    "matrix": cm.tolist()}
        }


new_run.log('TotalObservation', len(dataset))
new_run.log_confusion_matrix('ConfusionMatrix', cm_dict)

X_test = X_te.reset_index(drop=True)
y_test = y_te.reset_index(drop=True)

pred = pd.DataFrame(y_pred, columns=['Scored Label'])
pred.to_csv('./outputs/Loan_scored.csv', index=False)

new_run.complete()