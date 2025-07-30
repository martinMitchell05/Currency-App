# 💱 CurrencyApp

A Python application that allows you to check and convert exchange rates between different currencies, including the official and "blue" (informal market) USD and EUR in Argentina.

## 🧰 Features

- ✅ Get exchange rates using the [ExchangeRate API](https://exchangerate.host/)
- ✅ Get **Dólar Blue** and **Euro Blue** (Argentina) rates from [Bluelytics API](https://api.bluelytics.com.ar/)
- ✅ Perform currency conversions (e.g., ARS → USD, EUR → ARS)
- ✅ Get historical rates (official and blue)
- ✅ Convert using blue market buy/sell prices
- ✅ Search for currency codes by name
- ✅ Secure API key and URL handling via `.env`

---

## :moneybag: Usage

You can try different methods like:
- convert("USD", "ARS", 100)
- getDolarBlue()
- convertARSToDolarBlue(10000)
- getCurrencies("EUR", ["USD", "ARS", "CAD"])

There are some example calls included in the "__main__" section of "app.py".

---

## :pushpin: Notes

- This app uses two APIs:
    - ExchangeRate Host : for official rates
    - Bluelytics API : for blue USD/EUR rates in Argentina
- All sensitive data is handled using environment variables.

---

## :wrench: Future improvements

- Add command-line or web interface
- Add tests

---

## Thanks for reading!
