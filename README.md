# gy-redis

## pip package
```
<<<<<<< HEAD
pip install gy-redis
=======
pip install numpy redis reactivex 
>>>>>>> 12ae13dd42968f39fb7164b8da38f6cb8c82424b
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