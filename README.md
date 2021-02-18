# Environment
- Visual Studio Code
- Anaconda

1. Anaconda環境で普通に```pip install azureml-sdk```でインストール
2. VSCodeのnotebookからcoreをimportしてみると、[ModuleNotFoundError: No module named 'ruamel' error from built image](https://github.com/Azure/MachineLearningNotebooks/issues/1110)が発生
3. ```python -m --user pip install pip==20.1.1```でpipをダウングレード
4. notebookで再度coreをimportすると、[Failure while loading azureml_run_type_providers](https://docs.microsoft.com/en-us/answers/questions/87272/failure-while-loading-azureml-run-type-providers.html)が発生
5. ```pip install --user azureml-sdk[notebooks]```で解決
