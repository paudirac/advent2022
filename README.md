# advent2022

First add dependencies ([pytest](https://docs.pytest.org/en/6.2.x/), mostly):

``` sh
$ python -m venv venv
$ source venv/bin/activate
(venv) $ python -m pip install -r src/requirements.txt
```

To run the tests

``` sh
(venv) $ cd src && source src/.env
(venv) $ pytest
```
