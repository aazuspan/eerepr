# eerepr

[![Earth Engine Python](https://img.shields.io/badge/Earth%20Engine%20API-Python-green)](https://developers.google.com/earth-engine/tutorials/community/intro-to-python-api)
[![PyPI version](https://badge.fury.io/py/eerepr.svg)](https://badge.fury.io/py/eerepr)
[![conda-forge link](https://img.shields.io/conda/vn/conda-forge/eerepr)](https://anaconda.org/conda-forge/eerepr)
[![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.org/github/aazuspan/eerepr/blob/main/docs/notebooks/demo.ipynb)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aazuspan/eerepr/HEAD?labpath=docs%2Fnotebooks%2Fdemo.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aazuspan/eerepr/blob/main/docs/notebooks/demo.ipynb)

Add interactive Code Editor-style HTML reprs to Earth Engine objects in a Jupyter environment.

![eerepr demo expanding the metadata for an image collection](assets/eerepr.gif)

## Setup

> [!TIP]
> `eerepr` is pre-installed in [Google Colab](https://colab.research.google.com/)!

Install from PyPI:

```bash
$ pip install eerepr
```

Install from Conda-Forge:

```bash
$ conda install -c conda-forge eerepr
```

## Usage

### Activating eerepr

```python
import eerepr
```

Importing `eerepr` in a Jupyter notebook adds an HTML repr method to all Earth Engine objects. When you print them, you'll see an interactive HTML repr instead of a boring old string repr. Simple as that!

> [!TIP]
> If you're using [geemap](https://github.com/gee-community/geemap), `eerepr` is automatically imported and activated by default!

### Manually Rendering Objects

Jupyter only automatically displays the last object in a cell. To manually render an HTML repr anywhere in a code block, use `IPython.display.display`.

```python
from IPython.display import display
import ee
import eerepr

ee.Initialize()

display(ee.FeatureCollection("LARSE/GEDI/GEDI02_A_002_INDEX").limit(3))
```

### Large Objects

> [!CAUTION]
> Just like in the Code Editor, printing huge collections can be slow and may hit memory limits. If a repr exceeds 100 Mb, `eerepr` will fallback to a string repr to avoid freezing the notebook. Adjust `eerepr.options.max_repr_mbs` to print larger objects.

## Caching

`eerepr` uses caching to improve performance. Server data will only be requested once for each unique Earth Engine object, and all subsequent requests will be retrieved from the cache until the Jupyter session is restarted.

When you import `eerepr`, it is automatically initialized with an unlimited cache size. You can manually set the number of unique objects to cache using `eerepr.initialize(max_cache_size=n)`. A value of `None` sets an unlimited cache while a value of `0` disables caching.
