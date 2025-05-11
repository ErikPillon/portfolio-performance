import streamlit as st
import plotly.graph_objects as go

# Streamlit app layout
st.set_page_config()
st.title("📈 Fear & Greed Index Gauge")

st.markdown(
    """
    This section is freely inspired by the wonderful tool freely available at [https://www.cnn.com/markets/fear-and-greed](https://www.cnn.com/markets/fear-and-greed).
    
    I make no claims of ownership or originality.
    Though, the entire codebase and interfaces have been developed autonomously. 
    """
)


# Function to create the gauge chart
def draw_fear_greed_gauge(value):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": "Fear & Greed Index"},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "darkgray"},
                "bar": {"color": "black"},
                "steps": [
                    {"range": [0, 20], "color": "#f7f7f7"},  # Extreme Fear
                    {"range": [20, 40], "color": "#f7f7f7"},  # Fear
                    {"range": [40, 60], "color": "#f7f7f7"},  # Neutral
                    {"range": [60, 80], "color": "#f7f7f7"},  # Greed
                    {"range": [80, 100], "color": "#f7f7f7"},  # Extreme Greed
                ],
                "threshold": {
                    "line": {"color": "black", "width": 4},
                    "thickness": 0.75,
                    "value": value,
                },
            },
        )
    )

    fig.update_layout(margin={"t": 20, "b": 0, "l": 0, "r": 0}, height=400)

    return fig


# Simulated index value
index_value = st.slider("Select index value:", 0, 100, 62)

# Render gauge
fig = draw_fear_greed_gauge(index_value)
st.plotly_chart(fig)
