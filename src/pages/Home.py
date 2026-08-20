import streamlit as st


st.title("🏠 Home Dashboard")





col1,col2,col3,col4=st.columns(4)

col1.metric("Traffic Density","72%")
col2.metric("AQI","118")
col3.info("High congestion at Andheri")


st.divider()

st.title("🤖 AI Assistant")

question=st.text_area(
    "Ask about city traffic, AQI or complaints"
)

if st.button("Ask"):

    if question:

        st.chat_message("user").write(question)

        answer="""
Traffic is expected to increase near Powai during evening hours.

AQI remains moderate.

Suggested action:
• Divert traffic
• Increase signal timing
• Notify citizens
"""

        st.chat_message("assistant").write(answer)