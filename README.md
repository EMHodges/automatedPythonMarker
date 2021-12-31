# automatedPythonMarker

## Distributing automatedPythonMarker
The app is packaged using Pyinstaller. The file ```automatedPythonMarker.spec``` contains configuration options. The file
```dist.py``` contains the command to be run to generate the executable. 


### Mac
To create a Mac executable you will need to run the following commands on a Mac.

Run ```pyinstaller manage.py dist``` # Note dist here is a custom command defined in  ```dist.py```

To execute the generated Unix file 
cd to ```dist``` folder and run ```./pythonMarker runserver --noreload```.

To rename the executable change the ```name``` parameter in ```automatedPythonMarker.spec``` and re-run 
```pyinstaller manage.py dist```.

