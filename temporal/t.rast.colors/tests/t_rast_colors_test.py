"""Test t.rast.colors functionality.

(C) 2026 by the GRASS Development Team
This program is free software under the GNU General Public
License (>=v2). Read the file COPYING that comes with GRASS
for details.
"""

import pytest

import grass.exceptions
from grass.tools import Tools


def test_basic_color_assignment(mapcalc_session, assert_color_info):
    """Test basic color definition from table."""
    tools = Tools(session=mapcalc_session, overwrite=True)
    tools.t_rast_colors(
        input="precip_abs1",
        color="grey",
    )

    assert_color_info(
        tools,
        "prec_1",
        {
        "table": [
            {'value': 100, 'color': '#000000'},
            {'value': 300, 'color': '#FFFFFF'}
        ],
        "nv": "#FFFFFF",
        "default": "#FFFFFF"
    },
    )

def test_w_flag(mapcalc_session, assert_color_info):
    """Test that colortable is unchanged with -w flag."""
    tools = Tools(session=mapcalc_session, overwrite=True)
    tools.t_rast_colors(
        input="precip_abs1",
        color="grey",
    )
    tools.t_rast_colors(
        input="precip_abs1",
        color="random",
        flags="w",
    )

    assert_color_info(
        tools,
        "prec_1",
        {
        "table": [
            {'value': 100, 'color': '#000000'},
            {'value': 300, 'color': '#FFFFFF'}
        ],
        "nv": "#FFFFFF",
        "default": "#FFFFFF"
    },
    )
