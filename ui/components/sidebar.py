import streamlit as st
NAV_ITEMS = [("Home","home"),("Chat","chat"),("Uploads","uploads"),("Settings","settings")]


def render_sidebar():
	st.title("Study Assistant")
	st.markdown("---")
	for label, _id in NAV_ITEMS:
		if st.button(label, key=f"nav_{_id}"):
			return label
	return "Home"