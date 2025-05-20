import streamlit as st
import streamlit.components.v1 as components
from orchestrator import Orchestrator

orchestrator = Orchestrator()

st.markdown("# Bonds Tracker")

# Plot
bonds_distribution = orchestrator.visualize_bonds_distribution()
st.plotly_chart(bonds_distribution, use_container_width=True)

st.write(
    f"""
    The total amount of bonds invested in the portfolio is: **{orchestrator.get_total_bonds_invested()}**
    """
)
