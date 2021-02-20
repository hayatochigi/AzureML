# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from azureml.core import Workspace, Datastore, Dataset, Experiment
from azureml.core import Run

ws = Workspace.from_config('./config.json')
az_store = Datastore.get(ws, 'from_sdk')
az_ds = Dataset.get_by_name(ws, 'Loan Applications Using SDK')
az_default_store = ws.get_default_datastore()


new_run = Run.get_context()

df = az_ds.to_pandas_dataframe()
total_len = len(df)
null_info = df.isnull().sum()

new_df = df.loc[:,['Gender', 'Married', 'Education', 'Loan_Status']]
new_df.to_csv('./outputs/Loan_trunc.csv', index=False)

# Log metrics
new_run.log('Total Length', total_len, description='Total length of dataset')

for column in df.columns:
    new_run.log(column, null_info[column])

# Complete the experiment
new_run.complete()


