## installs the dependencies listed in requirements.txt

```bash
pip install -r requirements.txt
```

## runs the server at 127.0.0.1:8000 and listens and reloads the entire app on save for real time logging

```bash
uvicorn src.project_biophilia.main:app --reload --reload-dir .
```

## runs the server at 127.0.0.1:8000 and listens

```bash
uvicorn src.project_biophilia.main:app --reload
```

## if it says "uvicorn not found", use this

```bash
python3 -m uvicorn src.project_biophilia.main:app --reload
```
