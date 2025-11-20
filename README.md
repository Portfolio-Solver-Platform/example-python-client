# Example Python Client

This is an example of a client written in Python that consumes the API that is exposed via PSP.

Download dependencies using `pip install -r requirements.txt`

You can run it using `python src/main.py`.

You should look in `src/main.py` to see how it works.
Additionally, the necessary configuration is put under `src/config.py`.

## Contributing

Download the development dependencies by using `pip install -r requirements-dev.txt`.

### Updating dependencies

You can manually update dependencies by:
```bash
pip-compile pyproject.toml -o requirements.txt --strip-extras
pip-compile pyproject.toml --extra dev -o requirements-dev.txt --strip-extras
```
