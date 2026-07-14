"""Fixtures for t.rast.mapcalc tests.

(C) 2025 by the GRASS Development Team
This program is free software under the GNU General Public
License (>=v2). Read the file COPYING that comes with GRASS
for details.
"""

import os

import pytest

import grass.script as gs
from grass.tools import Tools


@pytest.fixture(scope="session")
def mapcalc_session(tmp_path_factory):
    """GRASS session with prec_1..prec_3 rasters and precip_abs1/2 STRDS.

    Session-scoped: setup (region, rasters, STRDS, TGIS init) runs once for
    the whole test run. Tests use overwrite=True for their outputs and
    test_failure_on_missing_map restores its rename in a finally block, so
    sharing across modules is safe.
    """
    tmp_path = tmp_path_factory.mktemp("t_rast_mapcalc")
    project = tmp_path / "test"
    gs.create_project(project)
    with gs.setup.init(project, env=os.environ.copy()) as session:
        tools = Tools(session=session, overwrite=True)
        tools.g_gisenv(set="TGIS_USE_CURRENT_MAPSET=1")
        tools.g_region(s=0, n=80, w=0, e=120, b=0, t=50, res=10, res3=10)
        for name, val in [("prec_1", 100), ("prec_2", 200), ("prec_3", 300)]:
            tools.r_mapcalc(expression=f"{name} = {val}")
        tools.t_create(
            type="strds",
            temporaltype="absolute",
            output="precip_abs1",
            title="A test",
            description="A test",
        )
        tools.t_register(
            flags="i",
            type="raster",
            input="precip_abs1",
            maps="prec_1,prec_2,prec_3",
            start="2001-01-01",
            increment="3 months",
        )
        yield session


@pytest.fixture
def assert_color_info():
    """Return a helper that checks the color table of a raster map."""

    def _assert(tools, map_name, expected):
        actual = tools.r_colors_out(map=map_name, format="json").json
        for key, value in expected.items():
            assert key in actual, f"missing key {key!r} in t.info output"
            assert actual[key] == value, (
                f"{key}: expected {value!r}, got {actual[key]!r}"
            )

    return _assert
