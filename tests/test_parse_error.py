import os
import shutil
import sys

from six import StringIO

import eppy
from eppy import modeleditor
from eppy.runner.run_functions import parse_error, EnergyPlusRunError

from tests.pytest_helpers import safeIDDreset


def teardown_module(module):
    """new IDD has been set in the module. Here you tear it down"""
    safeIDDreset()

def test_capture_stderr():
    tmp_out = StringIO()
    sys.stderr = tmp_out
    sys.stderr.write("I am in stderr")
    msg = parse_error(tmp_out, "C:/notafile")
    assert "<File not found>" in msg
    assert "I am in stderr" in msg
    sys.stderr = sys.__stderr__


def test_capture_real_error(test_idf):
    test_idf.newidfobject(
        "HVACTemplate:Thermostat",
        Name="thermostat VRF",
        Heating_Setpoint_Schedule_Name=15,
        Constant_Cooling_Setpoint=25,
    )
    rundir = "test_capture_real_error"
    os.mkdir(rundir)
    try:
        test_idf.run(output_directory=rundir)
    except EnergyPlusRunError as e:
        assert "invalid Heating Setpoint Temperature Schedule" in str(e)
    finally:
        shutil.rmtree(rundir)
        safeIDDreset()
    