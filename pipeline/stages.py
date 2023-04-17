import pprint
import subprocess as sp
import sys
import json
import tempfile
import numpy as np

from os import path
from .framework import add_finalizer
from .color import rgb


def create_temporary_folder():
    tmpdir = tempfile.TemporaryDirectory()

    add_finalizer(lambda: tmpdir.cleanup())

    return tmpdir.name


def create_image_data(results):
    tmpdir = results[create_temporary_folder.__name__]

    img = np.array([  # 2x2 image: red, green, blue, white pixels.
        rgb(255, 0, 0),
        rgb(0, 255, 0),
        rgb(0, 0, 255),
        rgb(255, 255, 255)
    ], dtype=np.uint32)

    img_path = path.join(tmpdir, "four-pixels.bin")

    with open(img_path, "wb") as f:
        f.write(img)

    return img_path


def create_gcf_description(results):
    tmpdir = results[create_temporary_folder.__name__]
    img_path = results[create_image_data.__name__]
    desc_path = path.join(tmpdir, "meta.json")

    desc = {
        "header": {"version": 2},
        "resources": [{
            "type": "image",
            "format": "R8G8B8_UINT",
            "width": 2,
            "height": 2,
            "flags": ["image2d"],
            "supercompression_scheme": "deflate",
            "mip_levels": [
                {
                    "row_stride": 8,
                    "layers": [img_path]
                }
            ]
        }]
    }

    with open(desc_path, "w") as f:
        json.dump(desc, f)

    return desc_path


def pack_gcf_file(results):
    tmpdir = results[create_temporary_folder.__name__]
    desc_path = results[create_gcf_description.__name__]
    gcf_path = path.join(tmpdir, "output.gcf")

    sp.run([
        sys.executable,
        "-mgcfpack",
        "create",
        "-i", desc_path,
        "-o", gcf_path
    ])

    return gcf_path


def print_results(results):
    pprint.pprint(results)


def wait_for_user_input():
    input("Press RETURN key to delete the temporary directory.")
