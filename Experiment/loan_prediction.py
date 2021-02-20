# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
import pandas as pd
from azureml.core import Workspace, Run

ws = Workspace.from_config('./')
new_run = Run.get_context()

dataset = pd.read_csv('./Loan Approval Prediction.csv')
dataset = dataset.dropna()
dataset = dataset.drop(columns=['Loan_ID'], axis=1)


# %%
y = dataset['Loan_Status']
X = dataset.drop(columns=['Loan_Status'], axis=1)

cat_list = []
for col in X.columns:
    if np.dtype(X[col]) == 'object':
        cat_list.append(col)

X = pd.get_dummies(X, columns=cat_list, drop_first=True)
from sklearn.model_selection import train_test_split
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2)

print(X_tr)


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
# %%
