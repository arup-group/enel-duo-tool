# login:
from SessionState import get
from main import main
import streamlit as st
import os

session_state = get(password='')

if session_state.password != os.getenv("enelpassword"):
    pwd_placeholder = st.sidebar.empty()
    pwd = pwd_placeholder.text_input("Password:", value="", type="password")
    session_state.password = pwd
    if session_state.password == os.getenv("enelpassword"):
        pwd_placeholder.empty()
        main()
    elif session_state.password != '':
        st.error("the password you entered is incorrect")
else:
    main()