import streamlit as st
from orchestrator import Orchestrator

# from matplotlib.backends.backend_agg import RendererAgg
# _lock = RendererAgg.lock

orchestrator = Orchestrator()

st.title("Portfolio Performance Analyser")

# Sidebar
st.sidebar.header("About")
st.sidebar.markdown(
    "Indipendent project developed by [Erik Pillon](https://ErikPillon.github.io) for the pricing evaluation of put-call options with different numerical and analytical methods."
)


st.sidebar.header("Additional Resources")
st.sidebar.markdown(
    """
    How to use this app:
    """
)

st.subheader("Time Series Performance")

# Plot
fig1 = orchestrator.visualize_portfolio_evolution()
st.plotly_chart(fig1)

with st.expander("Data"):
    # st.dataframe(orchestrator.processor.get_total_capital_invested())
    st.dataframe(orchestrator.assets)

# st.metric(
#     "Total Capital Invested",
#     orchestrator.processor.get_total_capital_invested()["Value"][-1],
# )

# st.metric(
#     "Portfolio Performance",
#     orchestrator.processor.get_portfolio_performance()[-1],
# )

# st.metric(
#     "Total Capital Invested",
#     orchestrator.processor.get_total_capital_invested()["Value"][-1],
# )
# st.dataframe(orchestrator.processor.get_total_capital_invested())
