import streamlit as st
from presentation.controllers.assets_controllers import AssetsController
from shared.portfolio_logger import print_log


def initialize_session_state():
    print_log("Retrieving session state")
    if "initialized" not in st.session_state:
        print_log("Initializing session state", type="SUCCESS")

        st.session_state.initialized = True

        st.session_state.assets_controller = AssetsController()

        print_log("Session state initialized", type="SUCCESS")
