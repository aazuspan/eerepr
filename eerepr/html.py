import datetime
import uuid
from functools import singledispatch
from itertools import chain
from typing import Any

MAX_INLINE_LENGTH = 50


@singledispatch
def convert_to_html(obj: Any, key=None) -> str:
    """Converts a Python object (not list or dict) to an HTML <li> element.

    Parameters
    ----------
    obj : Any
        The object to convert to HTML.
    key : str, optional
        The key to prepend to the object value, in the case of a dictionary value or list element.
    """
    key_html = f"<span class='eerepr-key'>{key}:</span>" if key is not None else ""
    return (
        "<li class='eerepr-terminal'>"
        f"{key_html}"
        f"<span class='eerepr-val'>{obj}</span>"
        "</li>"
    )


@convert_to_html.register(list)
def list_to_html(obj: list, key=None) -> str:
    """Convert a Python list to an HTML <li> element."""
    contents = str(obj)
    n = len(obj)
    noun = "element" if n == 1 else "elements"
    header = f"{key}: " if key is not None else ""
    header += f"List ({n} {noun})" if len(contents) > MAX_INLINE_LENGTH else contents
    children = [convert_to_html(item, key=i) for i, item in enumerate(obj)]

    return make_collapsible_li(header, children)


@convert_to_html.register(dict)
def dict_to_html(obj: dict, key=None) -> str:
    """Convert a Python dictionary to an HTML <li> element."""
    obj = _sort_dict(obj)
    label = build_object_label(obj)

    header = f"{key}: " if key is not None else ""
    header += label
    children = [convert_to_html(value, key=key) for key, value in obj.items()]

    return make_collapsible_li(header, children)


def _sort_dict(obj: dict) -> dict:
    """Sort the properties of an Earth Engine object.

    This follows the Code Editor standard where priority keys are sorted first and the rest are
    returned in alphabetical order.
    """
    prop_priority = [
        "type",
        "id",
        "version",
        "bands",
        "columns",
        "geometry",
        "properties",
    ]

    priority_keys = [k for k in prop_priority if k in obj]
    start = {k: obj[k] for k in priority_keys}
    end = {k: obj[k] for k in sorted(obj)}
    return {**start, **end}


def make_collapsible_li(header, children) -> str:
    """Package a header and children into a collapsible list element"""
    data_id = "section-" + str(uuid.uuid4())

    return (
        "<li>"
        f"<input id='{data_id}' type='checkbox' class='eerepr-collapser'>"
        f"<label for='{data_id}' class='eerepr-header'>{header}</label>"
        f"<ul class='eerepr-list'>{''.join(children)}</ul>"
        "</li>"
    )


def build_image_label(obj: dict) -> str:
    obj_id = obj.get("id")
    id_label = f" {obj_id}" if obj_id else ""
    n = len(obj.get("bands", []))
    noun = "band" if n == 1 else "bands"
    return f"Image{id_label} ({n} {noun})"


def build_imagecollection_label(obj: dict) -> str:
    obj_id = obj.get("id")
    id_label = f" {obj_id} " if obj_id else ""
    n = len(obj.get("features", []))
    noun = "element" if n == 1 else "elements"
    return f"ImageCollection{id_label} ({n} {noun})"


def build_date_label(obj: dict) -> str:
    dt = datetime.datetime.utcfromtimestamp(obj.get("value", 0) / 1000)
    return f"Date ({dt})"


def build_feature_label(obj: dict) -> str:
    n = len(obj.get("properties", []))
    geom_type = obj.get("geometry", {}).get("type")
    type_label = f"{geom_type}, " if geom_type is not None else ""
    noun = "property" if n == 1 else "properties"
    return f"Feature ({type_label}{n} {noun})"


def build_featurecollection_label(obj: dict) -> str:
    obj_id = obj.get("id")
    id_label = f" {obj_id} " if obj_id else ""
    ncols = len(obj.get("columns", []))
    nfeats = len(obj.get("features", []))
    col_noun = "column" if ncols == 1 else "columns"
    feat_noun = "element" if nfeats == 1 else "elements"
    return f"FeatureCollection{id_label} ({nfeats} {feat_noun}, {ncols} {col_noun})"


def build_point_label(obj: dict) -> str:
    x, y = obj.get("coordinates", [None, None])
    xstr = f"{x:.2f}" if isinstance(x, (int, float)) else "NaN"
    ystr = f"{y:.2f}" if isinstance(x, (int, float)) else "NaN"
    return f"Point ({xstr}, {ystr})"


def build_polygon_label(obj: dict) -> str:
    n = len(obj.get("coordinates", [[]])[0])
    noun = "vertex" if n == 1 else "vertices"
    return f"Polygon ({n} {noun})"


def build_multipolygon_label(obj: dict) -> str:
    coords = obj.get("coordinates", [])[0]
    flat = list(chain.from_iterable(coords))
    n = len(flat)
    noun = "vertex" if n == 1 else "vertices"
    return f"MultiPolygon ({n} {noun})"


def build_multipoint_label(obj: dict) -> str:
    """This also works for LineString and LinearRing."""
    obj_type = obj.get("type")
    n = len(obj.get("coordinates", []))
    noun = "vertex" if n == 1 else "vertices"
    return f"{obj_type} ({n} {noun})"


def build_pixeltype_label(obj: dict) -> str:
    prec = obj.get("precision", "")
    minimum = str(obj.get("min", ""))
    maximum = str(obj.get("max", ""))
    range = f"[{minimum}, {maximum}]"

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
        return type_ranges[range]
    except KeyError:
        return f"{prec} ∈ {range}"


def build_band_label(obj: dict) -> str:
    band_id = obj.get("id", "")
    if band_id:
        band_id = f'"{band_id}"'
    dtype = build_pixeltype_label(obj.get("data_type", {}))
    dims = obj.get("dimensions")
    dimensions = f"{dims[0]}x{dims[1]} px" if dims else ""
    crs = obj.get("crs", "")

    parts = list(filter(lambda k: k, [band_id, dtype, crs, dimensions]))
    return ", ".join(parts)


def build_daterange_label(obj: dict) -> str:
    start, end = obj.get("dates", [0, 0])
    dt_start = datetime.datetime.utcfromtimestamp(start / 1000)
    dt_end = datetime.datetime.utcfromtimestamp(end / 1000)
    return f"DateRange [{dt_start}, {dt_end}]"


def build_object_label(obj: dict) -> str:
    """Take an info dictionary from Earth Engine and return a header label.

    These labels attempt to be consistent with outputs from the Code Editor.
    """
    obj_type = obj.get("type", "")

    if obj_type == "Image":
        return build_image_label(obj)
    if obj_type == "ImageCollection":
        return build_imagecollection_label(obj)
    if obj_type == "Date":
        return build_date_label(obj)
    if obj_type == "FeatureCollection":
        return build_featurecollection_label(obj)
    if obj_type == "Feature":
        return build_feature_label(obj)
    if obj_type == "Point":
        return build_point_label(obj)
    if obj_type in ("MultiPoint", "LineString", "LinearRing"):
        return build_multipoint_label(obj)
    if obj_type == "Polygon":
        return build_polygon_label(obj)
    if obj_type == "MultiPolygon":
        return build_multipolygon_label(obj)
    if obj_type == "PixelType":
        return build_pixeltype_label(obj)
    if obj_type == "DateRange":
        return build_daterange_label(obj)
    if obj_type:
        obj_id = obj.get("id", "")
        id_label = f" {obj_id} " if obj_id else ""
        return f"{obj_type}{id_label}"
    # Band objects don't have a `type` property, so this is how the Code Editor matches them.
    if "data_type" in obj.keys() and "id" in obj.keys():
        return build_band_label(obj)

    n = len(obj.keys())
    noun = "property" if n == 1 else "properties"
    return f"Object ({n} {noun})"
