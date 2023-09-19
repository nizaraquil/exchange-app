import streamlit as st
import requests
import pandas as pd


# Load currencies from the "currencies.csv" file using pandas
currencies_df = pd.read_csv("currencies.csv")
currency_options = currencies_df["Currency Name"].apply(
    lambda name: f"{name}").tolist()

def main():
    st.title("Money Exchange App")

    amount = st.number_input("Amount", 0.00)
    currency1_index = st.selectbox("Exchange from", range(
        len(currency_options)), format_func=lambda i: currency_options[i], index=0)
    currency2_index = st.selectbox("Exchange to", range(
        len(currency_options)), format_func=lambda i: currency_options[i], index=0)

    # Extract currency codes based on user's selection
    currency1_code = currencies_df.loc[currency1_index]["Currency Code"]
    currency2_code = currencies_df.loc[currency2_index]["Currency Code"]

    # Create a function to handle currency conversion
    def convert_currency():
        url = "https://api.apilayer.com/fixer/convert"
        params = {
            "to": currency2_code,
            "from": currency1_code,
            "amount": amount,
        }
        headers = {"apikey": "gbeCz1SyMapJ7oDXGOzZbxoCaY9ze02X"}

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                st.error("Error: Too many people requested this service.")
            else:
                st.error(f"An error occurred: {e}")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
            return None

    if st.button("Convert"):
        conversion_result = convert_currency()
        if conversion_result:
            try:
                st.text(f'Date: {conversion_result["date"]}')
                st.text(f'{currency1_code}: {amount}')
                st.text(f'{currency2_code}: {conversion_result["result"]}')
            except KeyError:
                st.error(
                    "An error occurred while processing the conversion result.")

    # Display attribution
    st.toast("Made by @nizaraquil on GitHub")


if __name__ == '__main__':
    main()
