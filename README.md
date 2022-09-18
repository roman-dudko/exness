# API testing framework 
> https://gorest.co.in is used for demo

## Install requirements
``` bash
pip install -r requirements.txt
```

## Download and configure report generation tool
1. Download and unzip the latest release from: https://github.com/allure-framework/allure2/releases
2. Copy the path till bin
3. Add it to the path environment variable

## Run tests
execute command from project folder:
``` bash
pytest -n 3 --reruns 1 --alluredir=./allure-results
```
Tests will be run in 3 threads. In cases of failure test will be restarted once. 

## Generate report
Execute command from project folder:
``` bash
allure generate --clean
```
Allure report will be generated in 'allure-report' folder. Open index.html 