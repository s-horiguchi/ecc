# ecc (easy cell counter)
For more information, read the documentation at https://dspsleeporg.github.io/ecc/.

## What is it?
ecc is a small Python program to perform cell detection. It will identify the XYZ position, expression amount, and volume of the targeted cells from 3D mouse brain image. It is based on [ilastik](https://www.ilastik.org/), a machine-learning framework to train pixel classifiers.


## Installation

### System requirements
ecc has been developed and tested on Linux platforms (Ubuntu 16.04 LTS and CentOS 7). The code requires Python 3.7 or later.

To run the program, we recommend at least 8GB of system RAM and four cores of CPUs. No other specific hardware are required.

### Install ilastik
ecc uses [ilastik](https://www.ilastik.org/) to train a pixel classifier. Follow [this page](https://www.ilastik.org/documentation/basics/installation) to install ilastik. For the best compatibility, it is recomennded to use **version 1.3.0 or 1.3.2**.

Be sure to remember where you installed ilastik. We will need that path when we run ecc.

### Install ecc
ecc uses [conda](https://docs.conda.io/projects/conda/en/latest/index.html) to replicate virtual python environment. If you do not have conda installed in your system, you can download miniconda [here](https://docs.conda.io/en/latest/miniconda.html).

First, clone the repo:
```bash
$ git clone https://github.com/DSPsleeporg/ecc.git
```

Then, go to the directory and create a new conda environment:

```bash
$ cd ecc
$ conda env create -f environment.yml
```

This will create a new conda environment named `ecc-env`, with Python version 3.7.

Now activate the new environment by:
```bash
$ conda activate ecc-env
```

Then, **within the virtual environment**, install ecc:
```bash
(ecc-env) $ pip install .
```

With good internet connection, the whole installation should be finished in about 10 minutes.

Now you are ready to use ecc. To check that the installation was successful, launch python interpreter and type the following command:
```python
>>> import ecc
>>> help(ecc)
```
This will print out the help information about the package.

---

To learn how to use ecc, please read the [documentation](https://dspsleeporg.github.io/ecc/).

## GUI for Windows Users

There is a simple GUI based program `ecc_gui.py`.

It creates `settings_ecc.txt` in the same directory to save your last settings.

You can download the installer [here](https://github.com/s-horiguchi/ecc/releases/tag/v0.1).

### Building executables

For building a executable files,
1. Install Anaconda3 and manually install some libraries because `environment.yml` does not work on Windows.
2. Install [Pyinstaller](http://www.pyinstaller.org/) with pip command.
3. Just run `pyinstall ecc_gui.py`. The executable and other files are created in `dist/ecc-gui` directory. If you prefer single exe file, add `--onefile` option to the command, though the single exe will be very large and slow on each startup.

### Building Installer

4. Install [NSIS](https://nsis.sourceforge.io/)
5. Launch NSIS and compie `install.nsi` in our repository, which produces `install-ecc.exe`.
