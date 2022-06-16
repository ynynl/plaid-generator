# plaid-generator

run app:
```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
flask run
```

update package:
```
python -m pip freeze
```

run docker:
```
docker build --tag flask-app .   

docker run -p 5000:5000 flask-app
```
