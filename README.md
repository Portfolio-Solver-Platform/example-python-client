# Example Python Client

This is an example of a client written in Python that consumes the API that is exposed via PSP.
It uses AuthLib to handle tokens.

You can run it using `python -m src.main src/main.py`.

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
