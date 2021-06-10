# HAL Atom Locator

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Some useful commands

**Build the gui**

```bash
$> pyuic5 main.ui > MainUI.py
```

**Add folder to python path (conda)**

_NOTE :_ should not be necessary now...
```bash
$> conda develop /path/to/folder
```

## PyQtGraph

We use the PyQtGraph package for image and data display (mostly because it is faster than matplotlib). Useful links :

* [official website](http://www.pyqtgraph.org/)
* [documentation](https://pyqtgraph.readthedocs.io/en/latest/)

To see examples (useful to start programming):

```bash
$> python -m pyqtgraph.examples
```

## Start with HAL without problems

**Clone the repository from git-hub**

```bash
$> git clone https://github.com/adareau/HAL.git
```


Congrats ! you have now access to HAL !

**Create an virtual environnement.**

To do so you will need the package python3-venv so if you do not already have it, install it. 

```bash
$> sudo apt-get install python3-venv
```

We will install  there all python packages with the appropriate. Let's call this environnement halenv.

```bash
$> python3 -m venv halenv
```

After what you can enter the environnement through source

```bash
$> source halenv/bin/activate
```

Now that we work in halenv (as indicated in the terminal) install all packages from requirements.txt

```bash
(halenv) $> pip3 install PyQt5 pysnooper jsbeautifier numpy scipy matplotlib opencv-python pyqtgraph pyautogui opencv-python-headless
```

Now you can copy the start file in the folder where HAL is and go in it. It means that asking ls should returns some files an HAL and start : 

```bash
(halenv) $> ls
Documents Downloads  HAL  Images  start  
```

Finally, you can use HAL !!

```bash
(halenv) $> python3 start
```

