# gy-redis

## pip package
```
pip install gy-redis -U
```

## build package
```
python setup.py sdist bdist_wheel 
```

## push pypitest
```
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

## push pypi
```
python -m twine upload dist/*
```