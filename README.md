# eerepr

[![Earth Engine Python](https://img.shields.io/badge/Earth%20Engine%20API-Python-green)](https://developers.google.com/earth-engine/tutorials/community/intro-to-python-api)
[![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.org/github/aazuspan/eerepr/blob/main/docs/notebooks/demo.ipynb)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/aazuspan/eerepr/HEAD?labpath=docs%2Fnotebooks%2Fdemo.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/aazuspan/eerepr/blob/main/docs/notebooks/demo.ipynb)

`eerepr` is an experimental project to add interactive, Code Editor-style HTML reprs to Earth Engine objects in a Jupyter environment.

![An HTML repr showing the details for an ee.Image in a Jupyter notebook](https://user-images.githubusercontent.com/50475791/200094168-324658b7-c97e-451b-b490-2ff580ac81ab.png)

## Setup

```bash
pip install git+https://github.com/aazuspan/eerepr
```

Installs through `PyPI` and `conda-forge` will be added soon.

## Usage

```python
import eerepr
```

Importing `eerepr` in a Jupyter notebook adds an HTML repr method to all Earth Engine objects. When you print them, you'll see an interactive HTML repr instead of a boring old string repr. Simple as that!

> **Note**
> Just like in the Code Editor, printing huge collections can be slow and may hit memory limits.

## Caching

`eerepr` uses caching to improve performance. Server data will only be requested once for each unique Earth Engine object, and all subsequent requests will be retrieved from the cache until the Jupyter session is restarted.

When you import `eerepr`, it is automatically initialized with an unlimited cache size. You can manually set the number of unique objects to cache using `eerepr.initialize(max_cache_size=n)`. A value of `None` sets an unlimited cache while a value of `0` disables caching. You can also clear out the cache contents to free memory with `eerepr.clear_cache()`.

> **Warning**
> There is a known bug when calling `ee.List.shuffle(seed=False)`. Because the method returns non-deterministic results from the same seed value, the incorrect cached result will be displayed if called multiple times. All other random methods use deterministic seeds and should work as expected.
