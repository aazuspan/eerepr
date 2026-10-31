_unset = object()


def _factory(**kwargs) -> dict[str, object]:
    """Create a dictionary from every key, value pair, dropping the unset sentinel."""
    return {k: v for k, v in kwargs.items() if v is not _unset}


def PixelType(
    precision: str | None = _unset,
    min: str | None = _unset,
    max: str | None = _unset,
    dimensions: int | str | list | None = _unset,
) -> dict[str, object]:
    return _factory(
        type="PixelType", precision=precision, min=min, max=max, dimensions=dimensions
    )
