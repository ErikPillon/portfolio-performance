import streamlit as st
import plotly.graph_objects as go
from fg_index import FGIndex
from datetime import datetime


fg_index = FGIndex()

# Streamlit app layout
st.title("📈 Fear & Greed Index Gauge")

st.markdown(
    """
    This section is freely inspired by the wonderful tool freely available at [https://www.cnn.com/markets/fear-and-greed](https://www.cnn.com/markets/fear-and-greed).
    
    I make no claims of ownership or originality.
    Though, the entire codebase and interfaces have been developed autonomously. 
    """
)


st.subheader("Market Momentum")
fig = fg_index.get_market_momentum_fig()
left_col, right_col = st.columns([2, 1])
with left_col:
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.write("""
        It’s useful to look at stock market levels compared to where they’ve been over the past few months.
        When the S&P 500 is above its moving or rolling average of the prior 125 trading days, 
        that’s a sign of positive momentum. But if the index is below this average, 
        it shows investors are getting skittish. The Fear & Greed Index uses slowing momentum as a signal for Fear 
        and a growing momentum for Greed.
    """)
st.caption(f"Last updated {datetime.now().strftime('%B %d at %-I:%M:%S %p %Z')}")


st.subheader("Market Volatility")
fig = fg_index.get_market_volatility_fig()

left_col, right_col = st.columns([2, 1])
with left_col:
    st.plotly_chart(fig, use_container_width=True)

with right_col:
    st.write(
        """
        The most well-known measure of market sentiment is the CBOE Volatility Index, or VIX. 
        The VIX measures expected price fluctuations or volatility in the S&P 500 Index options over the next 30 days. 
        The VIX often drops on days when the broader market rallies and soars when stocks plunge. 
        But the key is to look at the VIX over time. 
        It tends to be lower in bull markets and higher when the bears are in control. 
        The Fear & Greed Index uses increasing market volatility as a signal for Fear.
    """,
        width=1000,
    )
st.caption(
    f"Last updated {datetime.now().strftime('%B %d at %-I:%M:%S %p %Z')}",
)
