import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#  Page config must be the first Streamlit command
st.set_page_config(page_title="Sri Lanka Energy & Mining Dashboard", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_energy_and_mining_lka.csv')
    return df

df = load_data()

# Dashboard title
st.title("Sri Lanka Energy & Mining Dashboard")

# Sidebar navigation
analysis_option = st.sidebar.selectbox(
    'Select Analysis',
    (
        'Distribution by Indicator Name',
        'Yearly Comparison by Category',
        'Trend by Indicator'
    )
)

#  Distribution by Indicator
if analysis_option == 'Distribution by Indicator Name':
    st.header('Distribution of Values by Indicator Name')

    selected_category = st.selectbox("Select Category", sorted(df['indicator_category'].unique()))
    filtered_df = df[df['indicator_category'] == selected_category]

    selected_indicators = st.multiselect("Select Indicator(s)", sorted(filtered_df['indicator_name'].unique()))
    if selected_indicators:
        filtered_df = filtered_df[filtered_df['indicator_name'].isin(selected_indicators)]

    # Plot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='indicator_name', y='value', data=filtered_df)
    plt.xticks(rotation=45, ha='right')
    plt.title(f"Value Distribution in {selected_category}")
    plt.tight_layout() 
    st.pyplot(plt.gcf())

#  Yearly Comparison by Category
elif analysis_option == 'Yearly Comparison by Category':
    st.header('Compare Multiple Years for Selected Indicators')

    selected_years = st.multiselect(
        "Select Year(s)", sorted(df['year'].unique()), default=[df['year'].max()]
    )

    selected_category = st.selectbox("Choose Category", sorted(df['indicator_category'].unique()))
    category_df = df[(df['year'].isin(selected_years)) & (df['indicator_category'] == selected_category)]

    selected_indicators = st.multiselect(
        "Select Indicator(s)", sorted(category_df['indicator_name'].unique())
    )

    if selected_indicators:
        filtered_df = category_df[category_df['indicator_name'].isin(selected_indicators)]
    else:
        filtered_df = category_df

    # Create a consistent color palette for the selected years
    unique_years = sorted(filtered_df['year'].unique())
    colors = sns.color_palette("Set1", len(unique_years))
    year_color_map = dict(zip(unique_years, colors))

    # Determine y-axis label
    if filtered_df['indicator_name'].str.contains("investment", case=False).any():
        y_label = "Value (in million USD)"
    elif filtered_df['indicator_name'].str.contains("access to electricity|renewable energy consumption|firms using banks|value lost due to electrical outages", case=False).any():
        y_label = "Proportion (0–1 scale)"
    else:
        y_label = "Value"

    # Plot
    plt.figure(figsize=(12, 6))
    sns.barplot(data=filtered_df, x='indicator_name', y='value', hue='year', palette=year_color_map)
    plt.title(f"{selected_category} Indicators Across Year(s)")
    plt.ylabel(y_label)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(plt.gcf())

#  Trend by Indicator 
elif analysis_option == 'Trend by Indicator':
    st.header(' Trend Over Time for an Indicator')

    selected_indicator = st.selectbox("Select Indicator", sorted(df['indicator_name'].unique()))
    ind_df = df[df['indicator_name'] == selected_indicator]

    # Plot
    plt.figure(figsize=(10, 5))
    sns.lineplot(x='year', y='value', data=ind_df, marker='o')
    plt.title(f"Trend Over Time: {selected_indicator}")
    plt.xlabel("Year")
    plt.ylabel("Value")
    st.pyplot(plt.gcf())
