# eerepr

[![Earth Engine Python](https://img.shields.io/badge/Earth%20Engine%20API-Python-green)](https://developers.google.com/earth-engine/tutorials/community/intro-to-python-api)
[![PyPI version](https://badge.fury.io/py/eerepr.svg)](https://badge.fury.io/py/eerepr)
[![conda-forge link](https://img.shields.io/conda/vn/conda-forge/eerepr)](https://anaconda.org/conda-forge/eerepr)
[![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.org/github/aazuspan/eerepr/blob/main/docs/notebooks/demo.ipynb)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aazuspan/eerepr/HEAD?labpath=docs%2Fnotebooks%2Fdemo.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aazuspan/eerepr/blob/main/docs/notebooks/demo.ipynb)

Add interactive Code Editor-style HTML reprs to Earth Engine objects in a Jupyter environment.

![eerepr demo expanding the metadata for an image collection](assets/eerepr.gif)


## Features

- **⚡ Async**: `eerepr` uses threading to grab data asynchronously from Earth Engine, meaning that you can display big objects without blocking execution!
- **📦 Caching**: Earth Engine objects are automatically cached to speed up subsequent prints.
- **⚠️ Error Handling**: `eerepr` handles Earth Engine errors gracefully, displaying the message instead of crashing the notebook.

## Setup

Install from PyPI:

```bash
$ pip install eerepr
```

Install from Conda-Forge:

```bash
$ conda install -c conda-forge eerepr
```

## Usage

```python
import eerepr
```

Importing `eerepr` in a Jupyter notebook adds an HTML repr method to all Earth Engine objects. When you print them, you'll see an interactive HTML repr instead of a boring old string repr. Simple as that!

> **Note**
> Just like in the Code Editor, printing huge collections can be slow and may hit memory limits.
