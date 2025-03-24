import unittest
from pathlib import Path
import windIO

from jsonschema import Draft7Validator


class TestRegression(unittest.TestCase):
    def test_IEA_15_240_RWT(self):
        path2yaml = Path(__file__).parent / "IEA-15-240-RWT.yaml"

        # Validate the file
        windIO.validate(path2yaml, "turbine/IEAontology_schema")

        # Verify the file loads
        windIO.load_yaml(path2yaml)

    def test_IEA_15_240_RWT_VolturnUS_S(self):
        path2yaml = Path(__file__).parent / "IEA-15-240-RWT_VolturnUS-S.yaml"

        # Validate the file
        windIO.validate(path2yaml, "turbine/IEAontology_schema")

        # Verify the file loads
        windIO.load_yaml(path2yaml)
    
    def test_valid_schema(self):
        schema = windIO.load_yaml(
            Path(windIO.schemas.turbine.__file__).parent / "IEAontology_schema.yaml",
        )

        windIO.schemas.windIOMetaSchema.check_schema(schema)
