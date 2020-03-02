# Schedule

Tested for Python 3.7.

Links for virtual env setting:
[https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html) and
[https://virtualenv.pypa.io/en/stable/userguide/](https://docs.python.org/3/library/venv.html)

For my Win-machine:
```
python -m venv env
call env/scripts/activate.bat
```

Requirements install:

```
pip install -r requirements.txt
```
If you want to manually run all pre-commit hooks on the repository, run `pre-commit run --all-files`. To run individual hooks use `pre-commit run <hook_id>`.
