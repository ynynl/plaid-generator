# plaid-generator

run app:
```
py -3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3 ./app.py
```

update package:
```
python -m pip freeze
```

run docker:
```
docker build --tag python-docker .

docker run python-docker
```
