import setuptools
# readme.md = github readme.md, 這裡可接受markdown寫法
# 如果沒有的話，需要自己打出介紹此專案的檔案，再讓程式知道
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gy_redis", # 
    version="0.0.2",
    author="jeff7522553",
    author_email="jeff7522553@gmail.com",
    description="GuanYu for test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guanyuhoujeff/gy-redis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)