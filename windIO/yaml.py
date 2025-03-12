import os
from typing import Any

import numpy as np
from ruamel.yaml import YAML
import xarray as xr


def get_YAML(
    typ: str = "safe",
    write_numpy: bool = True,
    read_include: bool = True,
    n_list_flow_style: int = 1,
) -> YAML:
    yaml_obj = YAML(typ=typ)
    yaml_obj.default_flow_style = False
    yaml_obj.width = 1e6
    yaml_obj.indent(mapping=4, sequence=6, offset=3)
    yaml_obj.allow_unicode = False

    # Write nested list of numbers with flow-style
    def list_rep(dumper, data):
        try:
            npdata = np.asanyarray(data)  # Convert to numpy
            if np.isdtype(npdata.dtype, "numeric"):  # Test if data is numeric
                if n_list_flow_style >= len(
                    npdata.shape
                ):  # Test if n_list_flow_style is larger or equal to array shape
                    return dumper.represent_sequence(
                        "tag:yaml.org,2002:seq", data, flow_style=True
                    )
        except ValueError:
            pass
        return dumper.represent_sequence(
            "tag:yaml.org,2002:seq", data, flow_style=False
        )

    yaml_obj.Representer.add_representer(list, list_rep)

    if write_numpy:
        # Convert numpy types to build in data types
        yaml_obj.Representer.add_multi_representer(
            np.str_, lambda dumper, data: dumper.represent_str(str(data))
        )
        yaml_obj.Representer.add_multi_representer(
            np.number,
            lambda dumper, data: dumper.represent_float(float(data)),
        )
        yaml_obj.Representer.add_multi_representer(
            np.integer, lambda dumper, data: dumper.represent_int(int(data))
        )

        # Convert numpy array to list
        def ndarray_rep(dumper, data):
            return list_rep(dumper, data.tolist())

        yaml_obj.Representer.add_representer(np.ndarray, ndarray_rep)

    if read_include:

        def include(constructor, node):
            filename = os.path.join(
                os.path.dirname(constructor.loader.reader.stream.name), node.value
            )
            ext = os.path.splitext(filename)[1].lower()
            if ext in [".yaml", ".yml"]:
                return load_yaml(
                    filename, get_YAML()
                )  # TODO: Make `get_YAML()` dynamic to make it possible to update
            elif ext in [".nc"]:

                def fmt(v: Any) -> dict | list | str | float | int:
                    """
                    Formats a dictionary appropriately for yaml.load by converting Tuples to Lists.

                    Args:
                        v (Any): Initially, a dictionary of inputs to format. Then, individual
                            values within the dictionary.
                    """
                    if isinstance(v, dict):
                        return {k: fmt(v) for k, v in v.items() if fmt(v) != {}}
                    elif isinstance(v, tuple):
                        return list(v)
                    else:
                        return v

                def ds2yml(ds: xr.Dataset) -> dict:
                    """
                    Converts the input xr.Dataset to a format compatible with yaml.load.

                    Args:
                        ds (xr.Dataset): NetCDF data loaded as a xr.Dataset
                    """
                    d = ds.to_dict()
                    return fmt(
                        {
                            **{k: v["data"] for k, v in d["coords"].items()},
                            **d["data_vars"],
                        }
                    )

                return ds2yml(xr.open_dataset(filename))
            else:
                raise ValueError(f"Unsupported file extension: {ext}")

        yaml_obj.constructor.add_constructor("!include", include)

    return yaml_obj


def load_yaml(filename: str, loader=None) -> dict:
    """
    Opens ``filename`` and loads the content into a dictionary with the ``yaml.load``
    function from pyyaml.

    Args:
        filename (str): Path to the local file to be loaded.
        loader (yaml.SafeLoader, optional): Defaults to XrResourceLoader.

    Returns:
        dict: Dictionary representation of the YAML file given in ``filename``.
    """
    if loader is None:
        loader = get_YAML()
    with open(filename, "r") as fid:
        return loader.load(fid)
