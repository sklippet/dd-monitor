# import streamlit as st
# import pandas as pd
# import numpy as np

# st.set_page_config(
#     page_title="DD Dash",
#     page_icon="📊",
#     layout="wide"
# )

# st.title("Wallstreet Bits")
# st.header("Latest Posts")
# # st.subheader("Subsection")

# if st.button("Click Me!"):
#     st.write("Button Clicked!")


# # name = st.text_input("Enter your name")
# # age = st.number_input("Age", min_value=1, max_value=100)
# # gender = st.radio("Gender", ["Male", "Female", "Other"])
# # agree = st.checkbox("I agree to the terms")
# # selected_option = st.selectbox("Pick an option", ["A", "B", "C"])
# # multi_select = st.multiselect("Pick multiple", ["X", "Y", "Z"])


# uploaded_file = st.file_uploader("Upload CSV", type=["png"])
# if uploaded_file:
#     st.write("File uploaded successfully!")


# df = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])
# st.line_chart(df)
# st.bar_chart(df)
# st.area_chart(df)


import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Sales Dashboard")
st.sidebar.header("Filters")
year = st.sidebar.selectbox("Select Year", [2022, 2023, 2024])

df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr"],
    "Sales": [1000, 1500, 1200, 1800]
})

fig = px.line(df, x="Month", y="Sales", title="Sales Over Time")

col1, col2 = st.columns([2, 1])
with col1:
    st.plotly_chart(fig)
with col2:
    st.metric(label="Total Sales", value="$5,500", delta="+10%")

st.dataframe(df)