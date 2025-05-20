import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from utils import load_data, filter_data, get_summary_table

# Page config
st.set_page_config(page_title="Solar Potential Dashboard", layout="wide")
st.title("☀️ Solar Potential Dashboard")

# 💅 Custom CSS
st.markdown('''
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stButton>button {
        color: white;
        background: linear-gradient(90deg, #f7971e 0%, #ffd200 100%);
        border: none;
        border-radius: 8px;
        padding: 0.5em 2em;
        font-weight: bold;
        font-size: 1.1em;
        margin: 0.5em 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .stDataFrame, .stTable {
        background: #fffbe7;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .stSelectbox>div>div>div>div {
        background: #fffbe7;
    }
    </style>
''', unsafe_allow_html=True)

# 🚀 Load data
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Failed to load data: {e}")
    st.stop()

# 📚 Sidebar navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to:", ["Dashboard", "Summary Table", "Top GHI", "About"])

# 🌍 Country selection
countries = df["Country"].unique().tolist()
selected = st.multiselect("Select countries to compare:", countries, default=countries)

# 📉 Filtered data
filtered_df = filter_data(df, selected)

# 🧪 Interactive controls
if st.button("Show Data Sample"):
    st.write(filtered_df.head())

if st.button("Download Filtered Data as CSV"):
    st.download_button(
        label="Download CSV",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_solar_data.csv",
        mime="text/csv"
    )

# ✅ Basic info
st.write("✅ App loaded successfully")
st.write("Selected countries:", selected)
st.write("Filtered data shape:", filtered_df.shape)

# 🖼️ Main dashboard pages
if page == "Dashboard":
    metric = st.selectbox("Choose a metric to visualize:", ["GHI", "DNI", "DHI"])

    # 📦 Boxplot
    st.subheader(f"{metric} Distribution")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(x="Country", y=metric, data=filtered_df, palette="Set2", ax=ax)
    st.pyplot(fig)

    # 🎻 Violin plot
    st.subheader(f"{metric} Violin Plot")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.violinplot(x="Country", y=metric, data=filtered_df, palette="Set2", ax=ax2)
    st.pyplot(fig2)

    # ⏱️ Time series plot for GHI
    if "Timestamp" in filtered_df.columns:
        st.subheader("GHI Over Time (Sample)")
        for country in selected:
            country_df = filtered_df[filtered_df["Country"] == country]
            if not country_df.empty:
                sample = country_df.head(1000)  # Limit to 1000 for speed
                fig3, ax3 = plt.subplots(figsize=(10, 3))
                ax3.plot(pd.to_datetime(sample["Timestamp"]), sample["GHI"], label=country)
                ax3.set_title(f"GHI Over Time - {country} (First 1000 records)")
                ax3.set_xlabel("Time")
                ax3.set_ylabel("GHI")
                ax3.legend()
                st.pyplot(fig3)

    # 💡 Recommendation
    st.markdown("""
    ### 🌞 Recommendation: Where to Plant Solar Panels
    Based on the analysis of Global Horizontal Irradiance (GHI), the best country for solar panel installation is the one with the highest average GHI. See the 'Top GHI' page for ranking. 
    For optimal results, select open, unshaded areas in the top-ranked country. If regional data is available, further prioritize regions with the highest GHI values.
    """)

elif page == "Summary Table":
    st.subheader("📊 Summary Statistics")
    st.dataframe(get_summary_table(filtered_df))

elif page == "Top GHI":
    st.subheader("🌍 Top 5 Countries by Average GHI")
    top_countries = filtered_df.groupby("Country")["GHI"].mean().reset_index()
    top5 = top_countries.sort_values(by="GHI", ascending=False).head(5)
    st.table(top5)

elif page == "About":
    st.markdown("""
    ### ℹ️ About This Dashboard
    This interactive dashboard helps compare solar potential across countries using key metrics:
    
    - **GHI**: Global Horizontal Irradiance  
    - **DNI**: Direct Normal Irradiance  
    - **DHI**: Diffuse Horizontal Irradiance  

    **Features**:
    - Visual comparison (boxplots & violin plots)
    - Summary statistics
    - Top 5 countries by average GHI
    - Filtered data download
    """)
