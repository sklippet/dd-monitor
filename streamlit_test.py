import streamlit as st
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt_tab')
stop_words = set(stopwords.words('english'))


# Set page config
st.set_page_config(page_title="Tech Dictionary", layout="wide")

# Define dictionary of terms
# Dictionary of common trading and investment terms with concise explanations
# investment_terms = {
#     "Stock": "A share of ownership in a company, representing a claim on part of the company’s assets and earnings.",
#     "ETF": "An exchange-traded fund is a type of security that tracks an index, commodity, or a basket of assets.",
#     "Options": "A financial derivative that gives the holder the right (but not the obligation) to buy or sell an asset at a specified price within a specified time.",
#     "Call Option": "A type of options contract that gives the holder the right to buy an asset at a specific price before a certain date.",
#     "Put Option": "A type of options contract that gives the holder the right to sell an asset at a specific price before a certain date.",
#     "Strike Price": "The set price at which an option can be bought or sold when exercised.",
#     "Premium": "The price paid for an options contract, which is determined by various factors including volatility, time to expiration, and strike price.",
#     "Short Selling": "The practice of selling a security that is not owned by the seller, with the intention of buying it back at a lower price.",
#     "Margin": "Borrowed money used to purchase securities, allowing traders to amplify potential returns (or losses).",
#     "Leverage": "Using borrowed capital to increase the potential return on investment. Higher leverage means higher risk.",
#     "Dividend": "A portion of a company’s earnings distributed to shareholders, typically in cash or additional stock.",
#     "P/E Ratio": "The price-to-earnings ratio, calculated by dividing the market price per share by the earnings per share, used to assess if a stock is over or undervalued.",
#     "Market Order": "An order to buy or sell a security immediately at the current market price.",
#     "Limit Order": "An order to buy or sell a security at a specific price or better. It only executes at the specified price or a more favorable one.",
#     "Stop Loss": "A predetermined price point at which an investor sells a security to limit potential losses.",
#     "Take Profit": "A predetermined price point at which an investor sells a security to lock in profits.",
#     "Volatility": "The degree of variation in the price of an asset over time, used as a measure of risk.",
#     "Bull Market": "A market in which prices are rising or are expected to rise.",
#     "Bear Market": "A market in which prices are falling or are expected to fall.",
#     "Rally": "A period of sustained increases in the prices of securities.",
#     "Correction": "A short-term drop of 10% or more in the price of a security or market index from its peak.",
#     "Recession": "A significant decline in economic activity that lasts for months or even years.",
#     "Blue Chip Stocks": "Stocks of well-established and financially stable companies with a history of reliable performance.",
#     "IPO": "Initial Public Offering, the first sale of stock by a private company to the public.",
#     "Liquidity": "The ability to buy or sell an asset without affecting its price significantly.",
#     "Slippage": "The difference between the expected price of a trade and the actual price at which the trade is executed.",
#     "FOMO": "Fear Of Missing Out; the feeling that others are benefiting from an opportunity that you might miss.",
#     "Hedging": "A risk management strategy used to offset potential losses in one investment by taking an opposing position in another.",
#     "Diversification": "The strategy of spreading investments across different assets or sectors to reduce risk.",
#     "Arbitrage": "The practice of exploiting price differences of the same or similar financial instruments across different markets to make a profit.",
#     "Momentum Trading": "A strategy that involves buying securities that are trending up and selling those that are trending down.",
#     "Swing Trading": "A type of trading where positions are held for several days or weeks to capitalize on short- to medium-term price movements.",
#     "Day Trading": "The practice of buying and selling financial instruments within the same trading day, often multiple times.",
#     "Scalping": "A short-term strategy where traders make small profits from tiny price movements throughout the day.",
#     "Risk/Reward Ratio": "A measure of how much risk an investor is taking in relation to the potential reward. Higher ratios are generally more favorable.",
#     "Yield": "The income return on an investment, typically expressed as an annual percentage of the investment's cost or market value.",
#     "Return on Investment": "A performance metric that calculates the return relative to the investment's cost, often expressed as a percentage.",
#     "ROI": "A performance metric that calculates the return relative to the investment's cost, often expressed as a percentage.",
#     "Capital Gains": "Profits from the sale of an asset or investment, typically taxed at a different rate than regular income.",
#     "Dollar-Cost Averaging": "An investment strategy where a fixed amount is invested at regular intervals, regardless of the asset’s price.",
#     "Futures": "A standardized contract to buy or sell an asset at a specific future date and price, often used in commodities or indexes.",
#     "Beta": "A measure of a stock's volatility in relation to the market. A beta greater than 1 indicates higher volatility.",
#     "Alpha": "The measure of an investment's return relative to a market index or benchmark. Positive alpha indicates outperformance.",
#     "Liquidity Trap": "A situation where monetary policy becomes ineffective because people hoard cash rather than invest or spend.",
#     "Overbought": "A situation where the price of a security has risen too quickly and is considered due for a correction or pullback.",
#     "Oversold": "A situation where the price of a security has fallen too much and may be due for a rebound.",
#     "Pump and Dump": "A scheme where the price of an asset is artificially inflated (pumped) to attract investors, then sold off (dumped) to make a profit.",
#     "FUD": "Fear, Uncertainty, and Doubt; misinformation or negative news used to manipulate market sentiment.",
#     "Market Capitalization": "The total market value of a company's outstanding shares, calculated as stock price × total shares.",
#     "Bid-Ask Spread": "The difference between the highest price a buyer is willing to pay and the lowest price a seller is willing to accept.",
#     "Penny Stock": "A low-priced stock, usually under $5 per share, that is highly speculative and volatile.",
#     "Dividend Yield": "A financial ratio that shows how much a company pays in dividends relative to its stock price.",
#     "Ex-Dividend Date": "The date after which a stock is traded without the right to receive the next declared dividend.",
#     "Earnings Per Share (EPS)": "A company's net profit divided by the number of outstanding shares, used to measure profitability.",
#     "Book Value": "The total value of a company’s assets minus liabilities, often compared to market value.",
#     "Intrinsic Value": "The perceived true value of an asset based on fundamental analysis rather than market price.",
#     "Resistance Level": "A price level at which an asset struggles to rise above due to selling pressure.",
#     "Support Level": "A price level at which an asset tends to stop falling due to buying interest.",
#     "Breakout": "A price movement beyond a defined resistance or support level, often signaling a new trend.",
#     "Gamma": "A measure of the rate of change of delta in an options contract, affecting how sensitive it is to price movements.",
#     "Theta": "A measure of time decay in options pricing, representing the loss of value as expiration nears.",
#     "Vega": "A measure of an option's sensitivity to changes in implied volatility.",
#     "Implied Volatility": "The market's forecast of a likely movement in an asset’s price, often affecting option prices.",
#     "Sharpe Ratio": "A metric used to measure the risk-adjusted return of an investment.",
#     "VWAP (Volume Weighted Average Price)": "The average price of a stock over a period, weighted by trading volume, used by institutional traders.",
#     "Dark Pool": "A private exchange where large institutional investors trade stocks away from public markets to avoid affecting prices.",
#     "Circuit Breaker": "A temporary halt in trading triggered when stock indexes drop too quickly to prevent panic selling.",
#     "Roth IRA": "A retirement account where contributions are made post-tax, but withdrawals are tax-free.",
#     "SEC": "(Securities and Exchange Commission) The U.S. government agency that regulates financial markets and protects investors.",
#     "FED": "(Federal Reserve) The central bank of the U.S., responsible for monetary policy, interest rates, and economic stability.",
#     "Quantitative Easing (QE)": "A monetary policy where a central bank buys financial assets to inject liquidity into the economy.",
#     "Tapering": "The gradual reduction of central bank asset purchases, signaling a shift in monetary policy.",
#     "Yield Curve": "A graph showing the interest rates of bonds with different maturities, used to predict economic trends.",
#     "Inverted Yield Curve": "A situation where short-term interest rates are higher than long-term rates, often signaling a recession."
# }

investment_terms = {
    "Stock": "A share of ownership in a company, representing a claim on part of the company’s assets and earnings.",
    "Stocks": "A share of ownership in a company, representing a claim on part of the company’s assets and earnings.",
    "Equity": "A share of ownership in a company, representing a claim on part of the company’s assets and earnings.",
    "Shares": "A share of ownership in a company, representing a claim on part of the company’s assets and earnings.",
    "ETF": "An exchange-traded fund is a type of security that tracks an index, commodity, or a basket of assets.",
    "ETFs": "An exchange-traded fund is a type of security that tracks an index, commodity, or a basket of assets.",
    "Exchange-Traded Fund": "An exchange-traded fund is a type of security that tracks an index, commodity, or a basket of assets.",
    "Options": "A financial derivative that gives the holder the right (but not the obligation) to buy or sell an asset at a specified price within a specified time.",
    "Option": "A financial derivative that gives the holder the right (but not the obligation) to buy or sell an asset at a specified price within a specified time.",
    "Call Option": "A type of options contract that gives the holder the right to buy an asset at a specific price before a certain date.",
    "Call Options": "A type of options contract that gives the holder the right to buy an asset at a specific price before a certain date.",
    "Put Option": "A type of options contract that gives the holder the right to sell an asset at a specific price before a certain date.",
    "Put Options": "A type of options contract that gives the holder the right to sell an asset at a specific price before a certain date.",
    "Strike Price": "The set price at which an option can be bought or sold when exercised.",
    "Strike Price/Exercise Price": "The set price at which an option can be bought or sold when exercised.",
    "Premium": "The price paid for an options contract, which is determined by various factors including volatility, time to expiration, and strike price.",
    "Option Premium": "The price paid for an options contract, which is determined by various factors including volatility, time to expiration, and strike price.",
    "Short Selling": "The practice of selling a security that is not owned by the seller, with the intention of buying it back at a lower price.",
    "Short Sale": "The practice of selling a security that is not owned by the seller, with the intention of buying it back at a lower price.",
    "Margin": "Borrowed money used to purchase securities, allowing traders to amplify potential returns (or losses).",
    "Leverage": "Using borrowed capital to increase the potential return on investment. Higher leverage means higher risk.",
    "Leverage Trading": "Using borrowed capital to increase the potential return on investment. Higher leverage means higher risk.",
    "Margin Trading": "Borrowed money used to purchase securities, allowing traders to amplify potential returns (or losses).",
    "Dividend": "A portion of a company’s earnings distributed to shareholders, typically in cash or additional stock.",
    "Dividends": "A portion of a company’s earnings distributed to shareholders, typically in cash or additional stock.",
    "Dividend Yield": "A financial ratio that shows how much a company pays in dividends relative to its stock price.",
    "P/E Ratio": "The price-to-earnings ratio, calculated by dividing the market price per share by the earnings per share, used to assess if a stock is over or undervalued.",
    "Price-to-Earnings Ratio": "The price-to-earnings ratio, calculated by dividing the market price per share by the earnings per share, used to assess if a stock is over or undervalued.",
    "Market Order": "An order to buy or sell a security immediately at the current market price.",
    "Limit Order": "An order to buy or sell a security at a specific price or better. It only executes at the specified price or a more favorable one.",
    "Stop Loss": "A predetermined price point at which an investor sells a security to limit potential losses.",
    "Stop-Loss Order": "A predetermined price point at which an investor sells a security to limit potential losses.",
    "Take Profit": "A predetermined price point at which an investor sells a security to lock in profits.",
    "Volatility": "The degree of variation in the price of an asset over time, used as a measure of risk.",
    "Bull Market": "A market in which prices are rising or are expected to rise.",
    "Bear Market": "A market in which prices are falling or are expected to fall.",
    "Rally": "A period of sustained increases in the prices of securities.",
    "Market Rally": "A period of sustained increases in the prices of securities.",
    "Correction": "A short-term drop of 10% or more in the price of a security or market index from its peak.",
    "Recession": "A significant decline in economic activity that lasts for months or even years.",
    "Blue Chip Stocks": "Stocks of well-established and financially stable companies with a history of reliable performance.",
    "IPO": "Initial Public Offering, the first sale of stock by a private company to the public.",
    "Initial Public Offering": "Initial Public Offering, the first sale of stock by a private company to the public.",
    "Liquidity": "The ability to buy or sell an asset without affecting its price significantly.",
    "Slippage": "The difference between the expected price of a trade and the actual price at which the trade is executed.",
    "FOMO": "Fear Of Missing Out; the feeling that others are benefiting from an opportunity that you might miss.",
    "Hedging": "A risk management strategy used to offset potential losses in one investment by taking an opposing position in another.",
    "Diversification": "The strategy of spreading investments across different assets or sectors to reduce risk.",
    "Arbitrage": "The practice of exploiting price differences of the same or similar financial instruments across different markets to make a profit.",
    "Momentum Trading": "A strategy that involves buying securities that are trending up and selling those that are trending down.",
    "Swing Trading": "A type of trading where positions are held for several days or weeks to capitalize on short- to medium-term price movements.",
    "Day Trading": "The practice of buying and selling financial instruments within the same trading day, often multiple times.",
    "Scalping": "A short-term strategy where traders make small profits from tiny price movements throughout the day.",
    "Risk/Reward Ratio": "A measure of how much risk an investor is taking in relation to the potential reward. Higher ratios are generally more favorable.",
    "Yield": "The income return on an investment, typically expressed as an annual percentage of the investment's cost or market value.",
    "Return on Investment": "A performance metric that calculates the return relative to the investment's cost, often expressed as a percentage.",
    "ROI": "A performance metric that calculates the return relative to the investment's cost, often expressed as a percentage.",
    "Capital Gains": "Profits from the sale of an asset or investment, typically taxed at a different rate than regular income.",
    "Dollar-Cost Averaging": "An investment strategy where a fixed amount is invested at regular intervals, regardless of the asset’s price.",
    "Futures": "A standardized contract to buy or sell an asset at a specific future date and price, often used in commodities or indexes.",
    "Beta": "A measure of a stock's volatility in relation to the market. A beta greater than 1 indicates higher volatility.",
    "Alpha": "The measure of an investment's return relative to a market index or benchmark. Positive alpha indicates outperformance.",
    "Liquidity Trap": "A situation where monetary policy becomes ineffective because people hoard cash rather than invest or spend.",
    "Overbought": "A situation where the price of a security has risen too quickly and is considered due for a correction or pullback.",
    "Oversold": "A situation where the price of a security has fallen too much and may be due for a rebound.",
    "Pump and Dump": "A scheme where the price of an asset is artificially inflated (pumped) to attract investors, then sold off (dumped) to make a profit.",
    "FUD": "Fear, Uncertainty, and Doubt; misinformation or negative news used to manipulate market sentiment.",
    "Futures Contract": "A standardized contract to buy or sell an asset at a specific future date and price, often used in commodities or indexes.",
    "Stop-Loss Order": "A predetermined price point at which an investor sells a security to limit potential losses.",
    "Trailing Stop": "A stop-loss order that moves with the market price of the security, locking in profits as the price rises."
}

# Example text where terms will be highlighted
text = """
The major upcoming catalyst for this stock will be their earnings 11th of March. The company has been closing stores to free up liquidity to make up one big debt repayment. If they fail, the stock will drop lower because bankruptcy will be imminent. In this case I do not expect shareholders to receive anything.
"""



from fuzzywuzzy import process
import re


# Example input
x = "This is a sample This string with 2 sample"
words = ["This", "sample"]
replacement = ["|this replace with sample|", "|sample replacement|"]


# for i, w in enumerate(words):
#     x = re.sub(rf"\b{w}\b", f"__PLACEHOLDER_{i}__", x)

# print(x)

# for i in range(len(words)):
#     print(i)
#     x = re.sub(rf"__PLACEHOLDER_{i}__", replacement[i], x)  

# print(x)



# Function to perform fuzzy matching on input text
def fuzzy_match_and_highlight(text, terms):
    highlighted_text = text  # Initialize with the original text
    # Split the text into words and apply fuzzy matching for each word
    wordlist = set(re.findall(r"\b\w+(?:\[-'\]\w+)*\b", text))
    replacements = {}
    for index, word in enumerate(wordlist):
        # Make sure we don't match terms already in HTML (i.e., already highlighted)
        
        if word.lower() not in stop_words:
            match = process.extractOne(word, terms.keys())  # Get the best fuzzy match
            
            if match and match[1] >= 95: 
                print(f"{word}:{match}") # Only match if the similarity is above 80%
                matched_term = match[0]
                matched_definition = terms[matched_term]
                replacements[index] = [word, matched_term, matched_definition]

                highlighted_text = re.sub(
                    rf"\b{re.escape(word)}\b",
                    f"__PLACEHOLDER_{index}__",
                    highlighted_text
                )
    
    for key, (word, title, body) in replacements.items():
        highlighted_text = re.sub(
                    rf"__PLACEHOLDER_{key}__",
                    f"<span class='highlight tooltip'>{word}<span class='tooltiptext'><h3>{title}</h3>{body}</span></span>",
                    highlighted_text
        )
    return highlighted_text
    
def match_and_highlight(text, terms):
    matches = []
    for term, description in terms.items():
        score = fuzz.partial_ratio(text, term)  # Gets similarity score between the input and word
        matches.append((term, score))


# Sort by similarity score (descending order)
    return matches

# print(match_and_highlight(text, investment_terms))
# Inject minimal CSS for seamless integration with Streamlit

# input_text = """Hey everyone, I'm sharing this DD because, compared to other analyses I've seen, there are some key differences and divergences. This is based on my own research, and I wanted to provide a more complete perspective on Gorilla Technology (GRRR) based on what I found . I’m just a regular small investor (not a financial advisor), currently holding 1,200 shares along with call options ahead of their webinar. I’ve spent a significant amount of time digging into their background, SEC filings, and the controversy surrounding short-seller allegations. If I’ve missed anything or if someone has a different take, I’d be happy to discuss it."""
tooltip_style = """
    <style>
    .highlight {
        background-color:#323d52;
        padding: 0 4px;
        border-radius: 3px;
        cursor: pointer;
        font-weight: bold;
    }

    .highlight:hover {
        background-color: #4c5e7d;
    }

    .tooltip {
        position: relative;
        display: inline-block;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        background: #252e3d;
        color: #fff;
        text-align: left;
        border-radius: 10px;
        padding: 8px 20px 20px 20px;
        position: absolute;
        z-index: 9999;
        top: 120%; /* Position above the term */
        left: -50%;
        transform: translateY(50%);
        margin: 8px 0;
        width: 400px;
        font-size: 16px; /* Streamlit default text size */
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; /* Streamlit default font stack */
        line-height: 1.6; /* Default line height in Streamlit */
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.4);
        opacity: 0;
        transition: opacity 0.3s ease-in-out, transform 0.2s ease-in-out;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
        transform: scale(1);
    }
    p {
        margin: 8px 0;
        font-size: 16px; /* Streamlit default text size */
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; /* Streamlit default font stack */
        line-height: 1.6; /* Default line height in Streamlit */
    }

    </style>
"""

from rapidfuzz import process

# Example input 
#string
input_string = "I am looking for a call option to buy in the stock market"

# List of words you are looking for


# Find the nearest matches for each word in the list
fuz = process.extract(text.lower(), [t.lower() for t in investment_terms.keys()])

# Output the best matches
print(fuz)

# Display text with tooltips in Streamlit
body = fuzzy_match_and_highlight(text, investment_terms)


    # Display post with highlighted terms
st.markdown(tooltip_style + f"<div>{body}</div>", unsafe_allow_html=True)
    
    # Optionally, display the matches
# if matches_title or matches_body:
#     st.write("### Matched Terms and Definitions")
#     for match in matches_title + matches_body:
#         word, term, definition = match
#         st.write(f"**{term}**: {definition}")
