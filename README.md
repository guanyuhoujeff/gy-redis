# gy-redis

## pip package
```
pip install numpy redis reactivex
```

## 打包套件
python setup.py sdist bdist_wheel 

## 放到 pypitest
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

## 放到 pypi
python -m twine upload dist/*