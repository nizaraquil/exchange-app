import streamlit as st
import requests


st.title("Money Exchange App")

amount = st.number_input("Amount", 0.00)

# Load currencies from the "currencies.txt" file
with open("currencies.txt", "r") as file:
    options = [line.strip() for line in file]

currency1 = st.selectbox("Exchange from", options, index=0)
currency2 = st.selectbox("Exchange to", options, index=0)

st.toast("by @nizaraquil on GitHub")
try:
    if st.button("Convert"):
        # API URL & KEY
        url = f"https://api.apilayer.com/fixer/convert?to={currency2}&from={currency1}&amount={amount}"
        payload = {}
        key = {"apikey": "YWWnPlQ7n7cPFnsqBFmY0S5zAcnbyYCA"}

        # REQUESTING RESPONSE AND CONVERTING IT TO JSON
        response = requests.request("GET", url, headers=key, data=payload)
        response = response.json()

        st.text(f'Date: {response["date"]}')
        st.text(f"{currency1}: {amount}")
        st.text(f'{currency2}: {response["result"]}')

except:
    st.error("Error!")
