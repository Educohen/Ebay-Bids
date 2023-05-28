
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns 
from plotly.subplots import make_subplots
import matplotlib as mpl

bids_df = pd.read_csv("data/bids_df.csv")

###Graphs to be plotted on the Dashboard###


###Graph 1###

def with_hue(ax, feature, Number_of_categories, hue_categories):
    a = [p.get_height() for p in ax.patches]
    patch = [p for p in ax.patches]
    for i in range(Number_of_categories):
        total = feature.value_counts().values[i]
        for j in range(hue_categories):
            percentage = '{:.1f}%'.format(100 * a[(j*Number_of_categories + i)]/total)
            x = patch[(j*Number_of_categories + i)].get_x() + patch[(j*Number_of_categories + i)].get_width() / 2 - 0.15
            y = patch[(j*Number_of_categories + i)].get_y() + patch[(j*Number_of_categories + i)].get_height() 
            ax.annotate(percentage, (x, y), size = 12)

#Setting a palette of colors

hexa_colors = ["#E53238", "#F5AF02","#0064D3", "#86B817"]
customPalette = sns.color_palette(hexa_colors)

#Plotting data

interactive_df1 = ( bids_df[["Successive_Outbidding", "Class"]])

interactive_cp1 = plt.figure(figsize=(8,6))

ax=sns.countplot(data=interactive_df1, x='Successive_Outbidding', hue='Class', palette=customPalette)

# Customize the x and y axes and title
plt.title('Frequency Successive Outbidding vs Class', fontsize=16)
plt.xlabel('Successive Outbidding', fontsize=12)
plt.ylabel('Class', fontsize=12)

with_hue(ax, interactive_df1["Successive_Outbidding"], 2, 2)




###Graph 2###

interactive_df2 = ( bids_df[["Winning_Ratio", "Class"]])

plt.figure(figsize=(10,8))


interactive_sct2 = px.scatter(interactive_df2, x="Winning_Ratio", 
                 y="Class",
                 color="Class",
                 size="Winning_Ratio",
                 orientation="h",
                 opacity = .2,
                 color_continuous_scale=["#86B817", "#F5AF02"],
                 labels={
                     "Winning_Ratio": "Winning Ratio",
                     "Class": "Class"},
                )

interactive_sct2.update_layout(
    title=dict(text="Correlation between Winning Ratio vs Class", 
               font=dict(size=18), 
               xanchor='center', 
               x=0.48, 
              ),
    
    xaxis=dict( 
        rangeselector=dict( 
            buttons=list([ 
                dict(count=1, 
                    step="all", 
                    stepmode="backward"), 
            ]) 
        ), 
        rangeslider=dict( 
            visible=True
        ), 
    )
)

###End of Graphs###


#Building layout dashboard page

#Setting page configurations
st.set_page_config(
    page_title="Ebay Bids - Data Analytics Dashboard",
    page_icon="📊",
    layout="centered",
)

#Dashboard top title
st.title("Ebay Bids - Data Analytics Dashboard")

col1, col2 = st.columns(2)


chart_selector = st.sidebar.selectbox("Select the chart", ['Frequency Successive Outbidding vs Class ','Correlation between Winning Ratio vs Class'])


if chart_selector=='Frequency Successive Outbidding vs Class ':
  bar_chart = st.write(interactive_cp1),
  st.markdown(f"This plot shows the Frequency of value counts of {interactive_df1.columns[0]} from 0 to 1 and for the {interactive_df1.columns[1]} types from 0 to 1 (0 = Normal Bidding and 1 = Abnormal Bidding)")
else:
  scatter_chart = st.write(interactive_sct2)
  st.markdown(f"This plot shows the Correlation of the {interactive_df2.columns[0]} from 0 to 100 and the {interactive_df2.columns[1]} types from 0 to 1 (0 = Normal Bidding and 1 = Abnormal Bidding)")

#with col1:
#    st.write(interactive_cp1)

#with col2:
#    st.write(interactive_sct2)
