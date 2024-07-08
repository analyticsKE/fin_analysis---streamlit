import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO

# Function to load and process data from CSV
def load_data(uploaded_file):
    content = uploaded_file.getvalue().decode("utf-8")
    df = pd.read_csv(StringIO(content), thousands=',')
    df.set_index('Index', inplace=True)
    
    def convert_value(x):
        if pd.isna(x):
            return pd.np.nan
        if isinstance(x, str):
            if '%' in x:
                return pd.to_numeric(x.strip(' %'), errors='coerce') / 100
            else:
                return pd.to_numeric(x.replace(',', ''), errors='coerce')
        return x  # If it's already a number, just return it

    # Apply the conversion to all columns
    for col in df.columns:
        df[col] = df[col].apply(convert_value)
    
    return df

# Function to configure x-axis
def configure_xaxis(fig):
    fig.update_xaxes(
        tickmode='array',
        tickvals=list(range(2019, 2024)),  # Adjust this range as needed
        ticktext=[str(year) for year in range(2019, 2024)],
        tickangle=0
    )
    return fig

# Set page config
st.set_page_config(page_title="Financial Statement Analysis Dashboard", layout="wide")

# Sidebar for file upload
st.sidebar.title("Data Input")
uploaded_files = st.sidebar.file_uploader("Choose CSV files", accept_multiple_files=True, type="csv")

# Main content
st.title("Financial Statement Analysis Dashboard 📈📊")
st.markdown(
"""
Welcome to the Financial Statement Analysis Dashboard. This interactive tool allows you to explore and compare key financial performance metrics from their income statements of companies. By uploading CSV files containing financial data, you can visualize trends, compare companies, and gain insights into the financial landscape of various Companies.

## How to Use This Dashboard
1. Upload CSV files containing financial data for companies using the sidebar.
2. Explore various charts and metrics that will automatically populate based on your data.
3. Use the comparative analysis section to directly compare different companies and metrics.
4. For ease of use, take note of the datatypes used and how the data is oriented in the sample files.

Now, let's dive into what each section of this dashboard represents and why it's important.

"""
)

if not uploaded_files:
    st.info("Please upload CSV files to begin analysis.")
else:
    # Load data from uploaded files
    all_data = {}
    for file in uploaded_files:
        company_name = file.name.split('.')[0].upper()
        all_data[company_name] = load_data(file)

    # Dashboard content goes here
    # 1. Revenue Growth
    st.header("1. Revenue Growth 💵")
    st.markdown(
    """
    Revenue growth is a fundamental indicator of a company's expansion and market performance. It shows the year-over-year increase in a company's sales. In the tech sector for this instance, strong and consistent revenue growth often indicates:

    - Successful product launches or service expansions
    - Increased market share
    - Effective pricing strategies
    - Overall business health and potential for future growth

    The chart below compares the revenue growth trajectories of the selected tech companies from 2019 to 2023, allowing you to identify industry leaders and emerging players.   

    """)
    fig_revenue = go.Figure()
    for company, data in all_data.items():
        fig_revenue.add_trace(go.Scatter(x=data.columns, y=data.loc['Revenue'], name=company, mode='lines+markers'))
    fig_revenue.update_layout(title="Revenue Growth (2019-2023)", xaxis_title="Year", yaxis_title="Revenue ($)")
    fig_revenue = configure_xaxis(fig_revenue)
    st.plotly_chart(fig_revenue, use_container_width=True)

    # 2. Profitability Analysis
    st.header("2. Profitability Analysis 💸")
    st.markdown(
    """
    Profitability ratios are crucial metrics that reveal a company's ability to generate profit relative to its revenue, assets, or equity. We focus on three key ratios:

    1. Gross Profit Ratio: (Revenue - Cost of Goods Sold) / Revenue
    - Indicates the efficiency of the production process and pricing strategy
    
    2. Operating Income Ratio: Operating Income / Revenue
    - Reflects the company's profitability from its core business operations
    
    3. Net Income Ratio: Net Income / Revenue
    - Shows the overall profitability after all expenses and taxes

    Higher ratios generally indicate better financial health, but it's important to compare these within the context of the tech industry and each company's business model.
    """
    )
    profitability_metrics = ['Gross Profit Ratio', 'Operating Income Ratio', 'Net Income Ratio']
    fig_profitability = go.Figure()
    for metric in profitability_metrics:
        for company, data in all_data.items():
            if metric in data.index:
                fig_profitability.add_trace(go.Bar(x=data.columns, y=data.loc[metric], name=f"{company} - {metric}"))
    fig_profitability.update_layout(title="Profitability Ratios (2019-2023)", xaxis_title="Year", yaxis_title="Ratio", barmode='group')
    fig_profitability = configure_xaxis(fig_profitability)
    st.plotly_chart(fig_profitability, use_container_width=True)

    # 3. Return on Equity (ROE)
    st.header("3. Return on Equity 💰(ROE)")
    st.markdown(
    """
    Return on Equity (ROE) is a key profitability metric that measures how effectively a company uses its shareholders' equity to generate profits. It's calculated as:

    ROE = Net Income / Shareholders' Equity

    A higher ROE suggests that a company is more efficient at using its equity to create profits. In the tech sector, ROE can vary widely due to factors like:

    - Capital intensity of the business model
    - Stage of company growth
    - Dividend policies and stock buybacks

    When analyzing ROE, consider it alongside other metrics and the company's overall strategy.
    """    
    )
    fig_roe = go.Figure()
    for company, data in all_data.items():
        if 'Net Income' in data.index and 'Basic Average Shares' in data.index:
            roe = data.loc['Net Income'] / data.loc['Basic Average Shares']
            fig_roe.add_trace(go.Scatter(x=data.columns, y=roe, name=company, mode='lines+markers'))
    fig_roe.update_layout(title="Return on Equity (2019-2023)", xaxis_title="Year", yaxis_title="ROE")
    fig_roe = configure_xaxis(fig_roe)
    st.plotly_chart(fig_roe, use_container_width=True)

    # 4. Operational Efficiency
    st.header("4. Operational Efficiency 💼")
    st.markdown(
    """
    Operational efficiency is crucial in any business operation. This is true in the tech sector, where innovation and market dynamics can rapidly change. This chart focuses on two key expense categories as a percentage of revenue:

    1. Operating Expenses: Includes costs like sales, marketing, and general administrative expenses
    2. Research and Development (R&D) Expenses: Critical for tech companies to stay competitive

    Lower percentages generally indicate better efficiency, but it's important to note:

    - High R&D spending might be necessary for long-term growth and competitiveness
    - Tech companies in different sub-sectors or growth stages may have vastly different expense structures

    This chart helps you understand how companies allocate their resources and their potential for future innovation and market expansion.
    """    
    )
    efficiency_metrics = ['Operating Expenses', 'Research And Development Expenses']
    fig_efficiency = go.Figure()
    for metric in efficiency_metrics:
        for company, data in all_data.items():
            if metric in data.index and 'Revenue' in data.index:
                efficiency = data.loc[metric] / data.loc['Revenue']
                fig_efficiency.add_trace(go.Scatter(x=data.columns, y=efficiency, name=f"{company} - {metric}", mode='lines+markers'))
    fig_efficiency.update_layout(title="Expenses as % of Revenue (2019-2023)", xaxis_title="Year", yaxis_title="Ratio")
    fig_efficiency = configure_xaxis(fig_efficiency)
    st.plotly_chart(fig_efficiency, use_container_width=True)

    # 5. Key Insights
    st.header("5. Key Insights 🧐")
    st.markdown(
    """
    This section provides a snapshot of key financial metrics for each company in the most recent fiscal year. These insights allow for quick comparisons and highlight areas of strength or potential concern. Key metrics include:

    - Year-over-Year Revenue Growth: Indicates the company's sales momentum
    - Profitability Ratios: Show the company's ability to convert revenue into profits at various stages
    - R&D Expenses: Reflect the company's investment in innovation and future products

    Use these insights as starting points for deeper analysis and to identify trends across the tech sector.
    """
    )
    for company, data in all_data.items():
        st.subheader(company)
        latest_year = data.columns[-1]
        previous_year = data.columns[-2]
        
        metrics = {
            "Revenue Growth (YoY)": (data.loc['Revenue', latest_year] - data.loc['Revenue', previous_year]) / data.loc['Revenue', previous_year] * 100,
            "Gross Profit Ratio": data.loc['Gross Profit Ratio', latest_year] * 100 if 'Gross Profit Ratio' in data.index else None,
            "Operating Income Ratio": data.loc['Operating Income Ratio', latest_year] * 100 if 'Operating Income Ratio' in data.index else None,
            "Net Income Ratio": data.loc['Net Income Ratio', latest_year] * 100 if 'Net Income Ratio' in data.index else None,
            "R&D Expenses": data.loc['Research And Development Expenses', latest_year] / 1e9 if 'Research And Development Expenses' in data.index else None
        }
        
        for metric, value in metrics.items():
            if value is not None:
                if metric == "R&D Expenses":
                    st.write(f"{metric}: ${value:.2f} billion")
                else:
                    st.write(f"{metric}: {value:.2f}%")
            else:
                st.write(f"{metric}: Data not available")

    # 6. Raw Data
    st.header("6. Raw Data")
    st.markdown(
    """
    This section provides access to the underlying data used to generate the visualizations and insights. You can:

    - View the complete dataset for each company
    - Verify specific data points
    - Identify additional trends or metrics not covered in the main dashboard

    Use this raw data to conduct your own analyses or to better understand the source of the insights presented throughout the dashboard.
    """
    )
    selected_company = st.selectbox("Select a company to view raw data", list(all_data.keys()))
    st.dataframe(all_data[selected_company])

    # 7. Comparative Analysis
    st.header("7. Comparative Analysis")
    st.markdown(
    """
    The Comparative Analysis tool allows you to dive deeper into specific metrics across multiple companies. This feature is particularly useful for:

    - Benchmarking performance against industry peers
    - Identifying sector-wide trends
    - Spotting companies that outperform or underperform in specific areas

    Select the companies and metrics you're interested in to generate custom visualizations and summary tables. This allows for a more nuanced understanding of how different tech companies stack up against each other in key financial areas.
    """
    )
    companies_to_compare = st.multiselect("Select companies to compare", list(all_data.keys()))

    if companies_to_compare:
        available_metrics = set.intersection(*[set(data.index) for data in all_data.values()])
        metrics_to_compare = st.multiselect("Select metrics to compare", list(available_metrics))

        if metrics_to_compare:
            for metric in metrics_to_compare:
                fig = go.Figure()
                for company in companies_to_compare:
                    fig.add_trace(go.Bar(
                        x=all_data[company].columns,
                        y=all_data[company].loc[metric],
                        name=company
                    ))
                fig.update_layout(
                    title=f"Comparison of {metric}",
                    xaxis_title="Year",
                    yaxis_title=metric,
                    barmode='group'
                )
                fig = configure_xaxis(fig)
                st.plotly_chart(fig, use_container_width=True)

            # Display a summary table
            st.subheader("Summary Table")
            summary_data = {}
            for company in companies_to_compare:
                company_data = all_data[company]
                latest_year = company_data.columns[-1]
                summary_data[company] = {metric: company_data.loc[metric, latest_year] for metric in metrics_to_compare}
            
            summary_df = pd.DataFrame(summary_data).T
            st.dataframe(summary_df)
    
    st.header("Conclusion")        
    st.markdown(
    """
    This dashboard provides a comprehensive overview of financial performance in the tech sector. Remember that while these metrics offer valuable insights, they should be considered alongside qualitative factors such as:

    - Market conditions and competitive landscape
    - Technological innovations and product pipelines
    - Regulatory environment and geopolitical factors
    - Management strategy and corporate governance

    Use this tool as a starting point for deeper analysis and always consider the broader context when making financial assessments or investment decisions.
    """    
    )