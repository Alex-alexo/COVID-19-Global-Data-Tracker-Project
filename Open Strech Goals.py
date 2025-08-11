

import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("owid-covid-data.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# -----------------------------
# Sidebar - User Inputs
# -----------------------------
st.sidebar.header("Filter Options")

# Country selection
countries = df['location'].unique().tolist()
selected_countries = st.sidebar.multiselect(
    "Select countries:",
    options=countries,
    default=["United States", "India", "Brazil"]
)

# Date range selection
min_date = df['date'].min()
max_date = df['date'].max()

date_range = st.sidebar.date_input(
    "Select date range:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# -----------------------------
# Filter Data
# -----------------------------
filtered_df = df[
    (df['location'].isin(selected_countries)) &
    (df['date'] >= pd.to_datetime(date_range[0])) &
    (df['date'] <= pd.to_datetime(date_range[1]))
]

# -----------------------------
# Charts
# -----------------------------
st.title("COVID-19 Global Data Tracker")

# Total Cases over Time
fig_cases = px.line(
    filtered_df,
    x="date",
    y="total_cases",
    color="location",
    title="Total COVID-19 Cases Over Time"
)
st.plotly_chart(fig_cases, use_container_width=True)

# Total Deaths over Time
fig_deaths = px.line(
    filtered_df,
    x="date",
    y="total_deaths",
    color="location",
    title="Total COVID-19 Deaths Over Time"
)
st.plotly_chart(fig_deaths, use_container_width=True)

# Vaccination Progress
fig_vacc = px.line(
    filtered_df,
    x="date",
    y="people_vaccinated",
    color="location",
    title="Vaccination Progress Over Time"
)
st.plotly_chart(fig_vacc, use_container_width=True)

# -----------------------------
# Optional: Hospitalizations & ICU
# -----------------------------
if 'hosp_patients' in df.columns:
    fig_hosp = px.line(
        filtered_df,
        x="date",
        y="hosp_patients",
        color="location",
        title="Hospitalized COVID-19 Patients Over Time"
    )
    st.plotly_chart(fig_hosp, use_container_width=True)

if 'icu_patients' in df.columns:
    fig_icu = px.line(
        filtered_df,
        x="date",
        y="icu_patients",
        color="location",
        title="ICU COVID-19 Patients Over Time"
    )
    st.plotly_chart(fig_icu, use_container_width=True)

# -----------------------------
# Summary Statistics
# -----------------------------
st.subheader("Summary Statistics")
st.write(filtered_df.groupby("location")[["total_cases", "total_deaths", "people_vaccinated"]].max())
