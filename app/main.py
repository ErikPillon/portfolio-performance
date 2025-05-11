import streamlit as st
from orchestrator import Orchestrator
from datetime import datetime

orchestrator = Orchestrator()

st.title("Portfolio Performance Analyser")

# Sidebar
st.sidebar.header("About")
st.sidebar.markdown(
    "Indipendent project developed by [Erik Pillon](https://ErikPillon.github.io) for assets tracking, financial analysis and portfolio performance."
)


st.sidebar.header("How to use this app")
st.sidebar.markdown(
    """
    1. Export the assets allocation template as an Excel file.
    2. List all of the assets that you want to track (Tickers, Date, Quantity). Tickers need to follow the (Yahoo finance)[https://finance.yahoo.com/lookup/] convention.
    3. Upload your file through the dedicated import tool.
    4. Enjoy!
    """
)

st.subheader("Time Series Performance")


# Plot
fig1 = orchestrator.visualize_portfolio_evolution()
st.plotly_chart(fig1)

expected_return = st.slider(
    "Expected Portfolio Return (in %)",
    min_value=-2.0,
    max_value=10.0,
    step=0.1,
    value=6.0,
)

col1_1, col1_2, col1_3 = st.columns(3)
col2_1, col2_2, col2_3 = st.columns(3)
# summary = {
#     "Total Investment": {
#         "Value": orchestrator.get_total_investment(),
#         "Percentage": orchestrator.get_total_investment_percentage(),
#     },
#     "Portfolio Performance": {
#         "Value": orchestrator.get_portfolio_performance(),
#         "Percentage": orchestrator.get_portfolio_performance_percentage(),
#     },
#     "Portfolio Estimated Performance": {
#         "Value": orchestrator.get_portfolio_performance(),
#         "Percentage": orchestrator.get_portfolio_performance_percentage(),
#     },
#     "Total Capital Invested": {
#         "Value": orchestrator.processor.get_total_capital_invested()["Value"][-1],
#         "Percentage": orchestrator.processor.get_total_capital_invested()["Value"][-1],
#     },
# }


col1_1.metric(
    label="Total Investment",
    value=f"{orchestrator.get_total_capital_invested():.2f}€",
)
col1_2.metric(
    label="Present Value",
    value=f"{orchestrator.get_portfolio_size_on_date(datetime.now()):.2f}€",
    delta=f"{(orchestrator.get_portfolio_size_on_date(datetime.now()) - orchestrator.get_total_capital_invested()):.2f}€",
)
col1_3.metric(
    label="Present Estimated Value",
    value=f"{orchestrator.get_estimated_portfolio_size_on_date(datetime.now()):.2f}€",
    delta=f"{(orchestrator.get_estimated_portfolio_size_on_date(datetime.now()) - orchestrator.get_total_capital_invested()):.2f}€",
)
col2_1.metric(label="Total Dividends Earned", value="0€", delta="0€")
col2_2.metric(label="Expected Portfolio Value", value="0€", delta="0€")
col2_3.metric(
    label="Actual Portfolio Return",
    value=f"{100 * (-1 + orchestrator.get_portfolio_size_on_date(datetime.now()) / orchestrator.get_total_capital_invested()):.2f}%",
    delta="0€",
)

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
