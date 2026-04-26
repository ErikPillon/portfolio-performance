import streamlit as st
from datetime import datetime
from presentation.controllers.portfolio_controller import PortfolioController
from presentation.state.session_state_manager import initialize_session_state

# Page configuration
st.set_page_config(
    page_title="Portfolio Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_session_state()

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


# Custom CSS for better styling
st.markdown(
    """
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""",
    unsafe_allow_html=True,
)


def main():
    portfolio: PortfolioController = st.session_state.portfolio_controller

    st.sidebar.title("Portfolio Manager")

    # portfolio_evolution_fig = portfolio.get_portfolio_evolution_figure()
    # st.plotly_chart(portfolio_evolution_fig)

    expected_return = st.slider(
        "Expected Portfolio Return (in %)",
        min_value=-2.0,
        max_value=10.0,
        step=0.1,
        value=6.0,
    )

    col0_1, col0_2, col0_3 = st.columns(3)
    col1_1, col1_2, col1_3 = st.columns(3)
    col2_1, col2_2, col2_3 = st.columns(3)
    # # summary = {
    # #     "Total Investment": {
    # #         "Value": orchestrator.get_total_investment(),
    # #         "Percentage": orchestrator.get_total_investment_percentage(),
    # #     },
    # #     "Portfolio Performance": {
    # #         "Value": orchestrator.get_portfolio_performance(),
    # #         "Percentage": orchestrator.get_portfolio_performance_percentage(),
    # #     },
    # #     "Portfolio Estimated Performance": {
    # #         "Value": orchestrator.get_portfolio_performance(),
    # #         "Percentage": orchestrator.get_portfolio_performance_percentage(),
    # #     },
    # #     "Total Capital Invested": {
    # #         "Value": orchestrator.processor.get_total_capital_invested()["Value"][-1],
    # #         "Percentage": orchestrator.processor.get_total_capital_invested()["Value"][-1],
    # #     },
    # # }

    capital_invested = portfolio.get_total_capital_invested()
    if capital_invested == 0:
        capital_invested = 1
    col0_1.metric(
        label="Total Investment in Bonds",
        value=f"{capital_invested:.2f}€",
    )
    col0_2.metric(
        label="Present Value",
        value=f"{portfolio.get_portfolio_size_on_date(datetime.now()):.2f}€",
        delta=f"{(portfolio.get_portfolio_size_on_date(datetime.now()) - capital_invested):.2f}€",
    )
    col0_3.metric(
        label="Present Estimated Value",
        value=f"{portfolio.get_estimated_portfolio_size_on_date(datetime.now()):.2f}€",
        delta=f"{(portfolio.get_estimated_portfolio_size_on_date(datetime.now()) - capital_invested):.2f}€",
    )

    col1_1.metric(
        label="Total Investment",
        value=f"{capital_invested:.2f}€",
    )
    col1_2.metric(
        label="Present Value",
        value=f"{portfolio.get_portfolio_size_on_date(datetime.now()):.2f}€",
        delta=f"{(portfolio.get_portfolio_size_on_date(datetime.now()) - capital_invested):.2f}€",
    )
    col1_3.metric(
        label="Present Estimated Value",
        value=f"{portfolio.get_estimated_portfolio_size_on_date(datetime.now()):.2f}€",
        delta=f"{(portfolio.get_estimated_portfolio_size_on_date(datetime.now()) - capital_invested):.2f}€",
    )
    col2_1.metric(label="Total Dividends Earned", value="0€", delta="0€")
    col2_2.metric(label="Expected Portfolio Value", value="0€", delta="0€")
    col2_3.metric(
        label="Actual Portfolio Return",
        value=f"{100 * (-1 + portfolio.get_portfolio_size_on_date(datetime.now()) / capital_invested):.2f}%",
        delta="0€",
    )

    with st.expander("Stocks and ETFs"):
        # st.dataframe(portfolio.processor.get_total_capital_invested())
        st.dataframe([asset.__dict__ for asset in portfolio.get_assets()])

    with st.expander("Bonds"):
        st.dataframe([bond.__dict__ for bond in portfolio.get_bonds()])

    # st.metric(
    #     "Total Capital Invested",
    #     portfolio.processor.get_total_capital_invested()["Value"][-1],
    # )

    # st.metric(
    #     "Portfolio Performance",
    #     portfolio.processor.get_portfolio_performance()[-1],
    # )

    # st.metric(
    #     "Total Capital Invested",
    #     portfolio.processor.get_total_capital_invested()["Value"][-1],
    # )
    # st.dataframe(portfolio.processor.get_total_capital_invested())


if __name__ == "__main__":
    main()
