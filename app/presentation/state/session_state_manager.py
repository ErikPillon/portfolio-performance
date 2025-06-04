import streamlit as st
from presentation.controllers.assets_controllers import AssetsController


def initialize_session_state():
    if "initialized" not in st.session_state:
        st.session_state.initialized = True

        st.session_state.assets_controller = AssetsController()
