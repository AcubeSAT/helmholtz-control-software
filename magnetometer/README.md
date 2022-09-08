## Magnetometer Calibration Interface

In order to use the magnetometer calibration algorithm from python, you need to install the Matlab Engine package. More info on the installation can be found [here](https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html). An error that might occur while using said package is
```
import matlab.engine
ModuleNotFoundError: No module named 'matlab.engine'; 'matlab' is not a package
```
in this case, you have to locate `matlab.py` path, which might look like this `"/home/user/.local/lib/python3.X/site-packages/matlab.py"` and rename the `matlab.py` file.