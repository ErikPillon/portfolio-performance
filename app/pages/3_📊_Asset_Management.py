import streamlit as st
from presentation.state.session_state_manager import initialize_session_state
from presentation.controllers.assets_controllers import AssetsController

# Page configuration
st.set_page_config(page_title="Asset Management", page_icon="💰", layout="wide")

# Initialize session state and dependencies
initialize_session_state()

# Initialize controller
asset_controller = AssetsController()

# Page header
st.title("💰 Asset Management")
st.markdown("Manage your investment assets and track their performance.")
