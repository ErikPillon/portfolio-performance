import pytest

import plotly.graph_objects as go
import pandas as pd

from visualiser import Visualiser


@pytest.fixture(autouse=True)
def visualizer():
    return Visualiser()


def test_get_bonds_distribution(visualizer):
    # Use the visualizer object in your test
    assert visualizer is not None

    bonds = pd.DataFrame(
        {
            "Name": ["Bond 1", "Bond 2"],
            "BondType": ["Type 1", "Type 2"],
            "Invested": [1000, 2000],
        }
    )
    fig = visualizer.get_bonds_distribution(bonds)
    assert isinstance(fig, go.Figure)
