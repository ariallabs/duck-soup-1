### Setup

```bash
# MacOS
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```

```bash
# Windows
virtualenv venv -p python3
venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
# Run the application with the following command:
python Note_App.py
```


### Build
```bash
# If you want to builf the application run the following command:

pyinstaller --name=duck-soup --windowed --onefile --icon=icon.ico Note_App.py 
```

