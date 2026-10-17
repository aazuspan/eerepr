from __future__ import annotations

import html
from collections.abc import Hashable
from datetime import datetime, timezone
from itertools import chain
from typing import Any

# Max characters to display for a list before truncating to "List (n elements)"
MAX_INLINE_LENGTH = 50
# Max elements in a list without definitely truncating, i.e. a list where each element
# takes 1 character plus brackets and delimiters.
MAX_LIST_LENGTH = MAX_INLINE_LENGTH // 3

# Sorting priority for Earth Engine properties
PROPERTY_PRIORITY = [
    "type",
    "id",
    "version",
    "bands",
    "columns",
    "geometry",
    "properties",
]
# Format for ee.Date and ee.DateRange
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def escape_object(obj: Any) -> Any:
    """Recursively escape HTML strings in a Python object."""
    if isinstance(obj, str):
        return html.escape(obj)
    if isinstance(obj, list):
        return [escape_object(element) for element in obj]
    if isinstance(obj, dict):
        return {escape_object(key): escape_object(value) for key, value in obj.items()}
    return obj


def convert_to_html(obj: Any, key: Hashable | None = None) -> str:
    """Converts a Python object (not list or dict) to an HTML <li> element.

    Parameters
    ----------
    obj : Any
        The object to convert to HTML.
    key : str, optional
        The key to prepend to the object value, in the case of a dictionary value or
        list element.
    """
    if isinstance(obj, list):
        return list_to_html(obj, key)
    if isinstance(obj, dict):
        return dict_to_html(obj, key)

    key_html = f"<span class='ee-k'>{key}:</span>" if key is not None else ""
    return f"<li>{key_html}<span class='ee-v'>{obj}</span></li>"


def list_to_html(obj: list, key: Hashable | None = None) -> str:
    """Convert a Python list to an HTML <li> element."""
    n = len(obj)
    header = f"{key}: " if key is not None else ""

    # Only stringify the list if it has few enough elements that it might not be
    # truncated.
    if n < MAX_LIST_LENGTH and len(contents := str(obj)) < MAX_INLINE_LENGTH:
        header += contents
    else:
        header += f"List ({n} {'element' if n == 1 else 'elements'})"

    children = [convert_to_html(item, key=i) for i, item in enumerate(obj)]
    return _make_collapsible_li(header, children)


def dict_to_html(obj: dict, key: Hashable | None = None) -> str:
    """Convert a Python dictionary to an HTML <li> element."""
    label = _summarize_collection(obj)
    header = (f"{key}: " if key is not None else "") + label

    # Sort properties by priority, then alphabetically
    sorted_keys = [k for k in PROPERTY_PRIORITY if k in obj] + sorted(
        [k for k in obj if k not in PROPERTY_PRIORITY]
    )

    children = [convert_to_html(obj[key], key=key) for key in sorted_keys]
    return _make_collapsible_li(header, children)


def _make_collapsible_li(header: str, children: list) -> str:
    """Package a header and children into a collapsible list element."""
    return (
        "<li>"
        "<details>"
        f"<summary>{header}</summary>"
        f"<ul>{''.join(children)}</ul>"
        "</details>"
        "</li>"
    )


def _summarize_image(obj: dict) -> str:
    obj_id = obj.get("id")
    id_label = f" {obj_id}" if obj_id else ""
    n = len(obj.get("bands", []))
    noun = "band" if n == 1 else "bands"
    return f"Image{id_label} ({n} {noun})"


def _summarize_imagecollection(obj: dict) -> str:
    obj_id = obj.get("id")
    id_label = f" {obj_id} " if obj_id else ""
    n = len(obj.get("features", []))
    noun = "element" if n == 1 else "elements"
    return f"ImageCollection{id_label} ({n} {noun})"


def _summarize_date(obj: dict) -> str:
    dt = datetime.fromtimestamp(obj.get("value", 0) / 1000, tz=timezone.utc)
    return f"Date ({dt.strftime(DATE_FORMAT)})"


def _summarize_feature(obj: dict) -> str:
    n = len(obj.get("properties", []))
    try:
        geom_type = obj["geometry"]["type"]
    except (TypeError, KeyError):
        geom_type = None

    type_label = f"{geom_type}, " if geom_type is not None else ""
    noun = "property" if n == 1 else "properties"
    return f"Feature ({type_label}{n} {noun})"


def _summarize_featurecollection(obj: dict) -> str:
    obj_id = obj.get("id")
    id_label = f" {obj_id} " if obj_id else ""
    ncols = len(obj.get("columns", []))
    nfeats = len(obj.get("features", []))
    col_noun = "column" if ncols == 1 else "columns"
    feat_noun = "element" if nfeats == 1 else "elements"
    return f"FeatureCollection{id_label} ({nfeats} {feat_noun}, {ncols} {col_noun})"


def _summarize_point(obj: dict) -> str:
    x, y = obj.get("coordinates", [None, None])
    xstr = f"{x:.2f}" if isinstance(x, (int, float)) else "NaN"
    ystr = f"{y:.2f}" if isinstance(y, (int, float)) else "NaN"
    return f"Point ({xstr}, {ystr})"


def _summarize_polygon(obj: dict) -> str:
    n = len(obj.get("coordinates", [[]])[0])
    noun = "vertex" if n == 1 else "vertices"
    return f"Polygon ({n} {noun})"


def _summarize_multipolygon(obj: dict) -> str:
    coords = obj.get("coordinates", [])[0]
    flat = list(chain.from_iterable(coords))
    n = len(flat)
    noun = "vertex" if n == 1 else "vertices"
    return f"MultiPolygon ({n} {noun})"


def _summarize_multipoint(obj: dict) -> str:
    """This also works for LineString and LinearRing."""
    obj_type = obj.get("type")
    n = len(obj.get("coordinates", []))
    noun = "vertex" if n == 1 else "vertices"
    return f"{obj_type} ({n} {noun})"


def _summarize_pixeltype(obj: dict) -> str:
    prec = obj.get("precision", "")
    minimum = str(obj.get("min", ""))
    maximum = str(obj.get("max", ""))
    val_range = f"[{minimum}, {maximum}]"

    type_ranges = {
        "[-128, 127]": "signed int8",
        "[0, 255]": "unsigned int8",
        "[-32768, 32767]": "signed int16",
        "[0, 65535]": "unsigned int16",
        "[-2147483648, 2147483647]": "signed int32",
        "[0, 4294967295]": "unsigned int32",
        "[-9.223372036854776e+18, 9.223372036854776e+18]": "signed int64",
    }

    if prec in ["double", "float"]:
        return prec
    try:
        return type_ranges[val_range]
    except KeyError:
        return f"{prec} ∈ {val_range}"


def _summarize_band(obj: dict) -> str:
    band_id = obj.get("id", "")
    if band_id:
        band_id = f'"{band_id}"'
    dtype = _summarize_pixeltype(obj.get("data_type", {}))
    dims = obj.get("dimensions")
    dimensions = f"{dims[0]}x{dims[1]} px" if dims else ""
    crs = obj.get("crs", "")

    return ", ".join(filter(None, [band_id, dtype, crs, dimensions]))


def _summarize_daterange(obj: dict) -> str:
    start, end = obj.get("dates", [0, 0])
    dt_start = datetime.fromtimestamp(start / 1000, tz=timezone.utc)
    dt_end = datetime.fromtimestamp(end / 1000, tz=timezone.utc)
    return (
        f"DateRange [{dt_start.strftime(DATE_FORMAT)}, {dt_end.strftime(DATE_FORMAT)}]"
    )


def _summarize_object(obj: dict) -> str:
    """Build a label for a generic JS object."""
    n = len(obj.keys())
    noun = "property" if n == 1 else "properties"
    return f"Object ({n} {noun})"


def _summarize_typed(obj: dict) -> str:
    """Build a label for an object with an unrecognized type."""
    obj_type = obj.get("type")
    obj_id = obj.get("id", "")
    id_label = f" {obj_id} " if obj_id else ""
    return f"{obj_type}{id_label}"


def _summarize_collection(obj: dict) -> str:
    """Generate a summary of a collection.

    These labels attempt to be consistent with outputs from the Code Editor.
    """
    labelers = {
        "Image": _summarize_image,
        "ImageCollection": _summarize_imagecollection,
        "Date": _summarize_date,
        "Feature": _summarize_feature,
        "FeatureCollection": _summarize_featurecollection,
        "Point": _summarize_point,
        "MultiPoint": _summarize_multipoint,
        "LineString": _summarize_multipoint,
        "LinearRing": _summarize_multipoint,
        "Polygon": _summarize_polygon,
        "MultiPolygon": _summarize_multipolygon,
        "PixelType": _summarize_pixeltype,
        "DateRange": _summarize_daterange,
    }

    obj_type = obj.get("type", "")
    if not obj_type:
        if "data_type" in obj and "id" in obj:
            return _summarize_band(obj)
        return _summarize_object(obj)
    try:
        return labelers[obj_type](obj)
    except KeyError:
        return _summarize_typed(obj)
