# automatedPythonMarker

## Setting up the code


### Windows

#### PyCharm
1. Install PyCharm community edition
2. Click Get from Version Control
3. Create the virtual environment: ```python -m venv my_venv```
4. Activate the virtual environment: ```.\my_venv\Scripts\activate```
5. Install required dependencies: ```pip install -r requirements.txt```
6. To deactive run: ```deactivate```



### Adding templates to executable
To add templates from a new app to the executable:
1. Add `resource_path("{APP_NAME}/templates")` to the `DIRS` list in `TEMPLATES` in `settings.py`
2. Add `Tree('{APP_NAME}', prefix='APP_NAME'),` to `exe` under the other `Tree` configs in `automatedPythonMarker.spec`

## Distributing automatedPythonMarker
The app is packaged using Pyinstaller. The file ```automatedPythonMarker.spec``` contains configuration options. The file
```dist.py``` contains the command to be run to generate the executable. 

To rename the executable change the ```name``` parameter in ```automatedPythonMarker.spec``` and re-run 
```pyinstaller manage.py dist_mac```.

Generated executables will be created in the ``dist`` folder. This folder will be automatically created when running 
the pyinstaller command below if it does not already exist.


### Windows
First you need to install pyinstaller bootloader. To do this activate the virtual environment and do the following
within the venv (this is instead of doing ```pip install pyinstaller``` which will work however causes
false positives with virus checkers such as virusTotal). This has been tested using Python 3.8.8:
1. ```git clone https://github.com/pyinstaller/pyinstaller```
2. ```cd pyinstaller```
3. ```git checkout v4.7```
4. ```cd \bootloader```
5. ```python ./waf distclean all```
6. ```cd ..```
7. ```python setup.py install```

To create a Windows executable you will need to run the following commands on a Windows machine.

Run ```pyinstaller manage.py dist_win``` to create the executable # Note dist here is a custom command defined in  ```dist.py```

To execute the generated executable file navigate to the `dist` directory (`cd dist`) and run `.\pythonMarker.exe 
runserver --noreload`


### Mac
To create a Mac executable you will need to run the following commands on a Mac.

Run ```pyinstaller manage.py dist``` # Note dist here is a custom command defined in  ```dist.py```

To execute the generated Unix file 
cd to ```dist``` folder and run ```./pythonMarker runserver --noreload```.
