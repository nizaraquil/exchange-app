import streamlit as st
import requests
import pandas as pd


class Convert:
    def __init__(self):
        self.currencies_df = pd.read_csv("currencies.csv")
        self.crypto_df = pd.read_csv("cryptocurrencies.csv")
        self.url = "https://api.apilayer.com/fixer/convert"

    def convert(self, amount, from_currency, to_currency, dataframe, code_column):
        payload = {}
        params = {"from": from_currency, "to": to_currency, "amount": amount, "access_key": "gbeCz1SyMapJ7oDXGOzZbxoCaY9ze02X"}
        try:
            response = requests.request("GET", self.url, params=params, data=payload)
            response.raise_for_status()
            data = response.json()
            if "error" in data:
                st.error(f"An error occurred: {data['error']['info']}")
                return None
            return data
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
            return None


def main():
    st.header("Money Converter App")

    converter = Convert()
    currency_tab, crypto_tab = st.tabs(["Currencies", "Crypto"])

    with currency_tab:
        amount = st.number_input("Amount", 0.00)

        currency_options = converter.currencies_df["Currency Name"].tolist()

        column1, column2 = st.columns(2)

        currency_from_index = column1.selectbox("From", currency_options)
        currency_to_index = column2.selectbox("To", currency_options)

        if st.button("Convert"):
            currency_from_code = converter.currencies_df[
                converter.currencies_df["Currency Name"] == currency_from_index
            ]["Currency Code"].values[0]
            currency_to_code = converter.currencies_df[
                converter.currencies_df["Currency Name"] == currency_to_index
            ]["Currency Code"].values[0]

            conversion_result = converter.convert(
                amount,
                currency_from_code,
                currency_to_code,
                converter.currencies_df,
                "Currency Code",
            )
            if conversion_result:
                date = conversion_result.get("date")
                result = conversion_result.get("result")
                if date and result:
                    st.text(
                        f"Date: {date}\n{currency_from_code}: {amount:,.2f}\n{currency_to_code}: {result:,.2f}"
                    )
                else:
                    st.warning("Unable to retrieve valid conversion data.")

    with crypto_tab:
        st.info("Cryptocurrencies will get added in the next update :)")

        crypto_amount = st.number_input("Crypto Amount", 0.00000)

        crypto_options = converter.crypto_df["Crypto Name"].tolist()

        column3, column4 = st.columns(2)

        crypto_from_index = column3.selectbox("From ", crypto_options, disabled=True)
        crypto_to_index = column4.selectbox("To ", currency_options)

        if st.button("Convert "):
            crypto_from_code = converter.crypto_df[
                converter.crypto_df["Crypto Name"] == crypto_from_index
            ]["Crypto Code"].values[0]
            crypto_to_code = converter.currencies_df[
                converter.currencies_df["Currency Name"] == crypto_to_index
            ]["Currency Code"].values[0]

            crypto_result = converter.convert(
                crypto_amount,
                crypto_from_code,
                crypto_to_code,
                converter.crypto_df,
                "Crypto Code",
            )
            if crypto_result:
                c_date = crypto_result.get("date")
                c_result = crypto_result.get("result")
                if c_date and c_result:
                    st.text(
                        f"Date: {c_date}\n{crypto_from_code}: {crypto_amount:,.3f}\n{crypto_to_code}: {c_result:,.3f}"
                    )
                else:
                    st.warning("Unable to retrieve valid conversion data.")

    st.markdown(
        "<font color='gray' size='2'>By @nizaraquil on GitHub</font>",
        unsafe_allow_html=True,
    )

    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
