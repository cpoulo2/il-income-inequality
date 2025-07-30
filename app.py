# A look at income and inequality in Illinois

import os
import pandas as pd
import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    """Load IL income inequality dataset."""
    try:
        df = pd.read_csv(r"data.csv")
        # Make sure all columns except 'state' are numeric
        df = df.apply(pd.to_numeric, errors='ignore')
        return df
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}. Please ensure the CSV files are in the correct location.")
        return None
    
def main():    
    # Load data
    df = load_data()
    
    if df is None:
        return

    # Main app
    
    st.set_page_config(page_title="IL income ≠", layout="centered")

    st.title("Who gets Illinois' income and how do they get it?")
    st.markdown("""
The following analysis looks at distribution of reported income in Illinois using IRS [Statistics of Income (SOI) data]( https://www.irs.gov/statistics/soi-tax-stats-statistics-of-income). See ["Notes on data source"](#notes-on-data-source) at the bottom. I analyze the following:
- The share of total income versus share of tax returns filed 1) by income group ([Figure 1](#figure-1-share-of-illinois-total-income-versus-tax-returns-by-income-group-2022)), 2) for millionaire's and billionaire's over time ([Figure 2](#figure-2-millionaires-and-billionaires-share-of-illinois-total-income-versus-tax-returns-2012-2022)), and 3) by income percentile over time ([Figure 3](#figure-3-share-of-illinois-total-income-by-percentile-2013-2022)).
- Source of income and their share across income groups ([Figure 4](#figure-4-source-of-income-by-income-group-2022) and [Figure 5](#figure-5-share-of-income-source-by-income-group-2022)) and across income percentiles ([Figure 6](#figure-6-source-of-income-by-percentile-2022) and [Figure 7](#figure-7-share-of-income-source-by-percentile-2022)).
- The share of income by source over time ([Figure 8](#figure-8-share-of-income-by-source-over-time-2012-2022)).

Below I provide a summary of findings followed by the income distribution figures.
""", unsafe_allow_html=True)
    

    st.header("Summary of findings")
    
    # get agi's for top 01, 05, 10, and 50
    dfx = df[df['year'] == 2022]
    dfx = dfx[dfx['state'] == "IL"]
    top_01 = dfx['agi_01'].unique()[0]
    top_05 = dfx['agi_05'].unique()[0]
    top_10 = dfx['agi_10'].unique()[0]
    top_50 = dfx['agi_50'].unique()[0]
    
    # Get total agi change from 2012 to 2022
    y2022 = df[(df['year'] == 2022) & (df['state'] == "IL")]['agi'].sum() 
    y2012 = df[(df['year'] == 2012) & (df['state'] == "IL")]['agi'].sum()
    
    diff = y2022-y2012
    diff_m = diff/1000000  # Convert to millions
    y2022_b = y2022 / 1000000000  # Convert to billions
    change = (diff)/y2012

    st.markdown(f"""
                Between 2012 and 2022, total annual gross income in Illinois increased by \\${diff_m:.1f} million reaching \\${y2022_b:,.1f} billion. The growth in income, however, is shared unevenly across income groups.
                
                **In 2022, the top 1% and especially millionaires and billionaires (the top 0.5%) recieved a disproportionate share of Illinois' reported income.** 
                
                That year, **the top 1% of Illinois' tax filers claimed about 21% of Illinois's income** (Figure 3)--with a annual gross income threashold of \\${top_01:,.0f}. Millionaires and billionaires (the top one-half of one percent) took home 17% of Illinois' total income (Figure 1). 
                
                **Much of the income reported by the top 1%, didn't come from wages or salaries, but from owning things other than their labor (business, equity, and assets).**
                
                Roughly **three-quarters of the income of the top 1% came from "passive sources"**--which the IRS defines as activities in which the tax filer does not materially participate in, such as S corporation profits, divdends, or capital gains. By contrast, **about 80% of income reported by the bottom half of tax filers came from wages and salaries** (Figure 6). 
                
                Viewed from another perspective, the lion's share of passive income flowed to the very top. For example, **71% of all capital gains income and 65% of all S corporation income** went to millionaires and billionaires (Figure 5).  
                
                **Since 2020, the share of income going to the top 1% and the top 0.5% has grown.** 
                
                Prior to COVID, millionaires' and billionaires' averaged about 14% of total income between 2012 and 2020. That share increased to 20% between 2021 and 2022 (Figure 2). 
                
                Figure 8 provides context for the 2020-2022 trends. An increase in the share of income of capital gains contributed to the 2021 spike in the share of income going to the top 1%. In addition, the share of S corporation income as is slightly increasing. Millionaires and billionaires own about 65% of S corporation income (Figure 5 filtered for "S-Corp") and the top 1% own about 71% (Figure 7).
                """, unsafe_allow_html=True)
                
                
                
                
# First, I show the share of tax filers by income categoery versus their share of income.")
#     st.markdown(" - Those making $1M or more make up one-half of one percent of tax filers but have about 17% of all income (Fig. 1).")
#     st.markdown(" - Pre-COVID, millionaires\' and billionaires\' share of income was about 14% (2012-2020). Their average share (2021 and 2022) increased to 20% (Fig. 2).")
#     st.markdown(f" - In 2022, the top 1% of tax files held about 21% of all income in Illinois. The top 5% held about 36%. And the top 10% held 47% (Fig. 3). For reference, to the annual gross income (AGI) cut off for individuals to be part of the top 1% in 2022 was \\${top_01:,.0f}. For the top 5% it was \\${top_05:,.0f}. For the top 10% it was \\${top_10:,.0f}. And for the top 50% it was \\${top_50:,.0f}.")
#     st.markdown(" - Post-COVID income shares among the top 1%, 5%, and 10% seem to have increased slightly post-COVID (Fig. 3).")
        
    # Income categoery data
    st.subheader("Figure 1: Share of Illinois' Total Income Versus Tax Returns by Income Group (2022)")
    # Remove agi_stub_cat = 0
    amt_dist = df[df['agi_stub'] != 0]
    amt_dist = amt_dist[(amt_dist['year'] == 2022) & (amt_dist['state'] == "IL")]
    amt_dist = amt_dist[["state","agi_stub_cat","agi_stub","returns","inc"]]
    amt_dist['Tax returns'] = amt_dist['returns'] / amt_dist['returns'].sum()
    amt_dist['Income'] = amt_dist['inc'] / amt_dist['inc'].sum()
    
    # Sort by agi_stub to ensure proper order
    amt_dist = amt_dist.sort_values('agi_stub')
    
    # Reshape data for plotly - need long format
    amt_dist = pd.melt(amt_dist, 
                           id_vars=['agi_stub_cat', 'agi_stub'], 
                           value_vars=['Tax returns', 'Income'],
                           var_name='Legend',
                           value_name='Percentage')
    
    # Create plotly bar chart
    fig = px.bar(amt_dist,
                x='agi_stub_cat',
                y='Percentage',
                color='Legend',
                labels={'agi_stub_cat': 'Income Group', 
                       'Percentage': 'Percent of Total'},
                barmode='group',
                color_discrete_map={'Tax returns': 'blue', 'Income': 'red'},
                hover_data={'agi_stub_cat': True, 'Percentage': ':.1%'})
    
    # Update layout for better appearance and formatting
    fig.update_layout(xaxis_tickangle=-45,
                     yaxis_tickformat='.0%')
    
    # Custom hover template
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>" +
                     "%{fullData.name} share: %{y:.1%}" +
                     "<extra></extra>"
    )
    
    # Show the chart
    st.plotly_chart(fig, use_container_width=True)
     
    
    st.subheader("Figure 2: Millionaires' and Billionaires' Share of Illinois' Total Income Versus Tax Returns (2012-2022)")
    
    # Millionaire and billionaire share of income over time
    
    # Exclude agi_stub_cat = 0
    amt_dist = df[df['agi_stub'] != 0]
    
    amt_dist = amt_dist[(amt_dist['state'] == "IL")]
    amt_dist = amt_dist[["state",'year',"agi_stub_cat","agi_stub","returns","inc"]]
    
    # Get millionaire data separately
    amt_dist_mil = amt_dist[amt_dist['agi_stub'] == 10].groupby('year')[['returns','inc']].sum().reset_index()
    amt_dist_mil = amt_dist_mil.rename(columns={'returns': 'returns_10', 'inc': 'inc_10'})
    
    # Get total data (all income categories)
    amt_dist = amt_dist.groupby('year')[['returns','inc']].sum().reset_index()
    
    # Merge millionaire and total data
    amt_dist = amt_dist.merge(amt_dist_mil, on='year')
    
    # Calculate shares
    amt_dist['Tax returns'] = amt_dist['returns_10'] / amt_dist['returns']
    amt_dist['Income'] = amt_dist['inc_10'] / amt_dist['inc']

    # Show a line graph comparing share of income (Income) and share of tax returns (Tax returns) for millionaires over time
    fig = px.line(amt_dist, 
                  x='year', 
                  y='Income', 
                  labels={'year': 'Year', 'Income': 'Share of Income'},
                  markers=True)

    # Update the first trace (Income line)
    fig.update_traces(name='Share of Income', 
                     line=dict(color='red'),
                     hovertemplate="<b>%{x}</b><br>Share of Income: %{y:.1%}<extra></extra>")
    
    # Add the second trace (Tax returns line)
    fig.add_scatter(x=amt_dist['year'], 
                    y=amt_dist['Tax returns'], 
                    mode='lines+markers', 
                    name='Share of Tax Returns', 
                    line=dict(color='blue'),
                    hovertemplate="<b>%{x}</b><br>Share of Tax Returns: %{y:.1%}<extra></extra>")
    
    # Update layout for better appearance and formatting
    fig.update_layout(yaxis_tickformat='.0%')
    fig['data'][0]['showlegend']=True

    # Show the chart
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Figure 3: Share of Illinois\' Total Income by Percentile (2013-2022)")
    
    # Percentile data
    
    # Keep only one row of percentile data per year
    pctile_dist = df[df['agi_stub'] == 0]
    pctile_dist = pctile_dist[(pctile_dist['state'] == "IL")]
    pctile_dist['bottom_50'] = pctile_dist['total_agi'] - pctile_dist['sum_agi_50']
    pctile_dist['bottom_50_sal'] = pctile_dist['total_sal_amt'] - pctile_dist['sum_sal_50']  
    pctile_dist['bottom_50_int'] = pctile_dist['total_int_amt'] - pctile_dist['sum_int_50']
    pctile_dist['bottom_50_div'] = pctile_dist['total_div_amt'] - pctile_dist['sum_div_50']
    pctile_dist['bottom_50_businc'] = pctile_dist['total_businc_amt'] - pctile_dist['sum_businc_50']
    pctile_dist['bottom_50_cpgain'] = pctile_dist['total_cpgain_amt'] - pctile_dist['sum_cpgain_50']
    pctile_dist['bottom_50_scorp'] = pctile_dist['total_scorp_amt'] - pctile_dist['sum_scorp_50']
    
    pctile_dist['Top 1%'] = pctile_dist['sum_agi_01'] / pctile_dist['total_agi']
    pctile_dist['Top 5%'] = pctile_dist['sum_agi_05'] / pctile_dist['total_agi']
    pctile_dist['Top 10%'] = pctile_dist['sum_agi_10'] / pctile_dist['total_agi']
    pctile_dist['Bottom 50%'] = pctile_dist['bottom_50'] / pctile_dist['total_agi']
    
    
    pctile_dist_inc = pctile_dist.copy()
    pctile_dist_inc = pctile_dist_inc[['year', 'Top 1%', 'Top 5%', 'Top 10%', 'Bottom 50%']]
    
    inc_share_df = pctile_dist.copy()
    inc_share_df = inc_share_df[inc_share_df['year'] == 2022]
    inc_share_df = inc_share_df[["total_sal_amt","total_int_amt","total_div_amt","total_businc_amt", 
                                 "total_cpgain_amt","total_scorp_amt","sum_agi_01","sum_agi_05", 
                                 "sum_agi_10", "bottom_50", "sum_sal_01","sum_sal_05", 
                                 "sum_sal_10", "bottom_50_sal","sum_int_01","sum_int_05",
                                 "sum_int_10", "bottom_50_int","sum_div_01","sum_div_05",
                                 "sum_div_10", "bottom_50_div","sum_businc_01","sum_businc_05",
                                 "sum_businc_10", "bottom_50_businc","sum_cpgain_01","sum_cpgain_05",
                                 "sum_cpgain_10", "bottom_50_cpgain","sum_scorp_01","sum_scorp_05",
                                 "sum_scorp_10", "bottom_50_scorp"]]

    # Create plotly line chart
    fig = px.line(pctile_dist, 
                  x='year', 
                  y=['Top 1%', 'Top 5%', 'Top 10%', 'Bottom 50%'],
                  labels={'year': 'Year', 'value': 'Share of Income', 'variable': 'Percentile'},
                  markers=True,
                  color_discrete_map={'Top 1%': 'blue', 'Top 5%': 'orange', 'Top 10%': 'green', 'Bottom 50%': 'red'})
    
    # Update layout for better appearance and formatting
    fig.update_layout(yaxis_tickformat='.0%')
    
    # Custom hover template
    fig.update_traces(
        hovertemplate="The %{fullData.name} had %{y:.1%} share of Illinois income<extra></extra>"
    )
    
    # Show the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # Share of income
    st.subheader("Figure 4: Source of Income by Income Group (2022)")
    # Create a 2022 dataframe with IL data on source of income by income group
    source_income = df.copy()
    source_income = source_income[(source_income['year'] == 2022) & (source_income['state'] == "IL")]
    source_income = source_income[source_income['agi_stub'] != 0]
    source_income = source_income[["agi_stub_cat","agi_stub","agi","inc","wages","interest",
                                   "dividends","business","capital_gains","s_corp"]]
    
        # Change variable names for clarity
    source_income = source_income.rename(columns={"wages":"Wages and Salaries",
                                                  "interest":"Interest",
                                                  "dividends":"Dividends",
                                                  "business":"Business",
                                                  "capital_gains":"Capital Gains",
                                                  "s_corp":"S-Corp"})
    
    source_income = source_income.melt(id_vars=['agi_stub_cat', 'agi_stub', 'inc'], 
                                   value_vars=['Wages and Salaries', 'Interest', 'Dividends', 
                                               'Business', 'Capital Gains', 'S-Corp'],
                                   var_name='Income Source',
                                       value_name='Amount')

    source_income['Source of Income (%)'] = source_income['Amount']/source_income['inc']
    
    # Find the sum of income for each source
    share = source_income.groupby(['Income Source']).sum('Amount').reset_index()
    share = share[["Income Source", "Amount"]]
    share.columns = ['Income Source', 'Share of Income']
    # Merge with ource_income DataFrame
    source_income = pd.merge(source_income, share, on='Income Source', how='left')
    source_income['Share of Income (%)'] = source_income['Amount'] / source_income['Share of Income']
    
    # Create a bar chart showing the income by source of income for each income group (like  the first bar chart)
    # Add a filters to select by income source
    selected_source = st.selectbox("Select Income Source", options=source_income['Income Source'].unique(), index=0)
    source_income = source_income[source_income['Income Source'] == selected_source]
    fig = px.bar(source_income, 
                 x='agi_stub_cat', 
                 y='Source of Income (%)', 
                 color='Income Source',
                 labels={'agi_stub_cat': 'Income Group', 'Source of Income (%)': 'Share of Income'},
                 barmode='group',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    # Update layout for better appearance and formatting
    fig.update_layout(xaxis_tickangle=-45, yaxis_tickformat='.0%')
    # Custom hover template
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>" +
                     "%{fullData.name} share: %{y:.1%}" +
                     "<extra></extra>"
    )
    # Show the chart
    st.plotly_chart(fig, use_container_width=True)
    
    
    st.subheader("Figure 5: Share of Income Source by Income Group (2022)")
    # Create a bar chart showing the share of income by source of income for each income group
    fig = px.bar(source_income, 
                 x='agi_stub_cat', 
                 y='Share of Income (%)', 
                 color='Income Source',
                 labels={'agi_stub_cat': 'Income Group', 'Share of Income (%)': 'Share of Income'},
                 barmode='group',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    # Update layout for better appearance and formatting
    fig.update_layout(xaxis_tickangle=-45, yaxis_tickformat='.0%')
    # Custom hover template
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>" +
                     "%{fullData.name} share: %{y:.1%}" +
                     "<extra></extra>"
    )
    # Show the chart
    st.plotly_chart(fig, use_container_width=True)

    # Income by source for percentiles
    
    st.subheader("Figure 6. Source of Income by Percentile (2022)")
    
    inc_share_df = pctile_dist.copy()
    inc_share_df = inc_share_df[inc_share_df['year'] == 2022]
    inc_share_df = inc_share_df[["total_sal_amt","total_int_amt","total_div_amt","total_businc_amt", 
                                 "total_cpgain_amt","total_scorp_amt","sum_agi_01","sum_agi_05", 
                                 "sum_agi_10", "bottom_50", "sum_sal_01","sum_sal_05", 
                                 "sum_sal_10", "bottom_50_sal","sum_int_01","sum_int_05",
                                 "sum_int_10", "bottom_50_int","sum_div_01","sum_div_05",
                                 "sum_div_10", "bottom_50_div","sum_businc_01","sum_businc_05",
                                 "sum_businc_10", "bottom_50_businc","sum_cpgain_01","sum_cpgain_05",
                                 "sum_cpgain_10", "bottom_50_cpgain","sum_scorp_01","sum_scorp_05",
                                 "sum_scorp_10", "bottom_50_scorp"]]
    
    wages = [(inc_share_df['bottom_50_sal']/ inc_share_df['bottom_50']).iloc[0],
         (inc_share_df['sum_sal_01']/ inc_share_df['sum_agi_01']).iloc[0],
         (inc_share_df['sum_sal_05']/ inc_share_df['sum_agi_05']).iloc[0],
         (inc_share_df['sum_sal_10']/ inc_share_df['sum_agi_10']).iloc[0]]

    interest = [(inc_share_df['bottom_50_int']/ inc_share_df['bottom_50']).iloc[0],
                (inc_share_df['sum_int_01']/ inc_share_df['sum_agi_01']).iloc[0],
                (inc_share_df['sum_int_05']/ inc_share_df['sum_agi_05']).iloc[0],
                (inc_share_df['sum_int_10']/ inc_share_df['sum_agi_10']).iloc[0]]

    dividends = [(inc_share_df['bottom_50_div']/ inc_share_df['bottom_50']).iloc[0],
                 (inc_share_df['sum_div_01']/ inc_share_df['sum_agi_01']).iloc[0],
                 (inc_share_df['sum_div_05']/ inc_share_df['sum_agi_05']).iloc[0],
                 (inc_share_df['sum_div_10']/ inc_share_df['sum_agi_10']).iloc[0]]

    business = [(inc_share_df['bottom_50_businc']/ inc_share_df['bottom_50']).iloc[0],
                (inc_share_df['sum_businc_01']/ inc_share_df['sum_agi_01']).iloc[0],
                (inc_share_df['sum_businc_05']/ inc_share_df['sum_agi_05']).iloc[0],
                (inc_share_df['sum_businc_10']/ inc_share_df['sum_agi_10']).iloc[0]]

    capital_gains = [(inc_share_df['bottom_50_cpgain']/ inc_share_df['bottom_50']).iloc[0],
                     (inc_share_df['sum_cpgain_01']/ inc_share_df['sum_agi_01']).iloc[0],
                     (inc_share_df['sum_cpgain_05']/ inc_share_df['sum_agi_05']).iloc[0],
                     (inc_share_df['sum_cpgain_10']/ inc_share_df['sum_agi_10']).iloc[0]]

    s_corp = [(inc_share_df['bottom_50_scorp']/ inc_share_df['bottom_50']).iloc[0],
              (inc_share_df['sum_scorp_01']/ inc_share_df['sum_agi_01']).iloc[0],
              (inc_share_df['sum_scorp_05']/ inc_share_df['sum_agi_05']).iloc[0],
              (inc_share_df['sum_scorp_10']/ inc_share_df['sum_agi_10']).iloc[0]]
    cats = ['Bottom 50%', 'Top 1%', 'Top 5%', 'Top 10%']
    # Create a DataFrame for the income shares
    income_shares = pd.DataFrame({
        'Percentile': cats,
        'Wages and Salaries': wages,
        'Interest': interest,
        'Dividends': dividends,
        'Business': business,
        'Capital Gains': capital_gains,
        'S-Corp': s_corp
    })
    
    # Melt the DataFrame to long format for Plotly
    income_shares_long = income_shares.melt(id_vars='Percentile', var_name='Income Source', value_name='Share')

    # Use plotly to create a bar chart
    fig = px.bar(income_shares_long, x='Percentile', y='Share', color='Income Source')
    fig.update_layout(barmode='group', xaxis_title='Income Percentile', yaxis_title='Share of Income')
    fig.update_traces(hovertemplate="<b>%{x}</b><br>" +
                     "%{fullData.name} share: %{y:.1%}" +
                     "<extra></extra>")
    # Update y-axis to show percentage format no decimals
    fig.update_layout(yaxis_tickformat='%')
    fig.update_yaxes(tickformat='.0%')
    st.plotly_chart(fig)
    
    st.subheader("Figure 7. Share of Income Source by Percentile (2022)")
    
    wages_share = [(inc_share_df['bottom_50_sal']/ inc_share_df['total_sal_amt']).iloc[0],
         (inc_share_df['sum_sal_01']/ inc_share_df['total_sal_amt']).iloc[0],
         (inc_share_df['sum_sal_05']/ inc_share_df['total_sal_amt']).iloc[0],
         (inc_share_df['sum_sal_10']/ inc_share_df['total_sal_amt']).iloc[0]]

    interest_share = [(inc_share_df['bottom_50_int']/ inc_share_df['total_int_amt']).iloc[0],
                (inc_share_df['sum_int_01']/ inc_share_df['total_int_amt']).iloc[0],
                (inc_share_df['sum_int_05']/ inc_share_df['total_int_amt']).iloc[0],
                (inc_share_df['sum_int_10']/ inc_share_df['total_int_amt']).iloc[0]]

    dividends_share = [(inc_share_df['bottom_50_div']/ inc_share_df['total_div_amt']).iloc[0],
                 (inc_share_df['sum_div_01']/ inc_share_df['total_div_amt']).iloc[0],
                 (inc_share_df['sum_div_05']/ inc_share_df['total_div_amt']).iloc[0],
                 (inc_share_df['sum_div_10']/ inc_share_df['total_div_amt']).iloc[0]]

    business_share = [(inc_share_df['bottom_50_businc']/ inc_share_df['total_businc_amt']).iloc[0],
                (inc_share_df['sum_businc_01']/ inc_share_df['total_businc_amt']).iloc[0],
                (inc_share_df['sum_businc_05']/ inc_share_df['total_businc_amt']).iloc[0],
                (inc_share_df['sum_businc_10']/ inc_share_df['total_businc_amt']).iloc[0]]

    capital_gains_share = [(inc_share_df['bottom_50_cpgain']/ inc_share_df['total_cpgain_amt']).iloc[0],
                     (inc_share_df['sum_cpgain_01']/ inc_share_df['total_cpgain_amt']).iloc[0],
                     (inc_share_df['sum_cpgain_05']/ inc_share_df['total_cpgain_amt']).iloc[0],
                     (inc_share_df['sum_cpgain_10']/ inc_share_df['total_cpgain_amt']).iloc[0]]

    s_corp_share = [(inc_share_df['bottom_50_scorp']/ inc_share_df['total_scorp_amt']).iloc[0],
              (inc_share_df['sum_scorp_01']/ inc_share_df['total_scorp_amt']).iloc[0],
              (inc_share_df['sum_scorp_05']/ inc_share_df['total_scorp_amt']).iloc[0],
              (inc_share_df['sum_scorp_10']/ inc_share_df['total_scorp_amt']).iloc[0]]
    cats = ['Bottom 50%', 'Top 1%', 'Top 5%', 'Top 10%']
    # Create a DataFrame for the income shares
    income_shares_share = pd.DataFrame({
        'Percentile': cats,
        'Wages and Salaries': wages_share,
        'Interest': interest_share,
        'Dividends': dividends_share,
        'Business': business_share,
        'Capital Gains': capital_gains_share,
        'S-Corp': s_corp_share
    })
    
    # Melt the DataFrame to long format for Plotly
    income_shares_share_long = income_shares_share.melt(id_vars='Percentile', var_name='Income Source', value_name='Share')

    # Use plotly to create a bar chart
    fig = px.bar(income_shares_share_long, x='Percentile', y='Share', color='Income Source')
    fig.update_layout(barmode='group', xaxis_title='Income Percentile', yaxis_title='Share of Income Type')
    fig.update_traces(hovertemplate="<b>%{x}</b><br>" +
                     "%{fullData.name} share: %{y:.1%}" +
                     "<extra></extra>")
    # Update y-axis to show percentage format no decimals
    fig.update_layout(yaxis_tickformat='%')
    fig.update_yaxes(tickformat='.0%')
    st.plotly_chart(fig)
    
    
    # Show all income sources over time
    st.subheader("Figure 8: Share of Income by Source Over Time (2012-2022)")
    income_sources_dist = df.copy()
    income_sources_dist = income_sources_dist[(income_sources_dist['state'] == "IL")]
    income_sources_dist = income_sources_dist[["year", 'agi_stub', "inc", "wages", "interest", 
                                              "dividends", "business", "capital_gains", "s_corp"]]
    income_sources_dist = income_sources_dist[income_sources_dist['agi_stub'] != 0]
    income_sources_dist = income_sources_dist.groupby(['year']).sum().reset_index()

    # Calculate share of income for each source
    income_sources_dist['Wages'] = income_sources_dist['wages'] / income_sources_dist['inc']
    income_sources_dist['Interest'] = income_sources_dist['interest'] / income_sources_dist['inc']
    income_sources_dist['Dividends'] = income_sources_dist['dividends'] / income_sources_dist['inc']
    income_sources_dist['Business'] = income_sources_dist['business'] / income_sources_dist['inc']
    income_sources_dist['Capital Gains'] = income_sources_dist['capital_gains'] / income_sources_dist['inc']
    income_sources_dist['S-Corp'] = income_sources_dist['s_corp'] / income_sources_dist['inc']

    # Create a line chart showing the share of income from all sources over time
    fig = px.line(income_sources_dist, 
                  x='year', 
                  y=['Wages', 'Interest', 'Dividends', 'Business', 'Capital Gains', 'S-Corp'],
                  labels={'year': 'Year', 'value': 'Share of Income', 'variable': 'Income Source'},
                  markers=True)

    # Update layout for better appearance
    fig.update_layout(
        xaxis_title='Year', 
        yaxis_title='Share of Income',
        yaxis_tickformat='.0%'
    )

    # Custom hover template
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>" +
                     "Year: %{x}<br>" +
                     "Share of Income: %{y:.1%}" +
                     "<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Notes on data source")
    st.markdown("""Tax return data is generally understood as more accurate source of data on income than survey data (i.e. the Consumer Population Survey or the American Community Survey), due to issues like of top coding which underreports income at the top. However, only a fraction of income is reported. In 2018, only about 60% of income was reported in the US. See [Saez, Emmanuel and Gabriel Zucman. 2020. "The Rise of Income and Wealth Inequality in America: Evidence from Distributional Macroeconomic Accounts." Journal of Economic Perspectives, 34 (4)](https://gabriel-zucman.eu/files/SaezZucman2020JEP.pdf). 
                
                """, unsafe_allow_html=True)
if __name__ == "__main__":
    main()

