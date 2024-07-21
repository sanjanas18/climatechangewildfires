# SANJANA SATAGOPAN

# MARCH 8 2023

# A VISUAL APPROACH - CLIMATE CHANGE AND WILDFIRES
# CODE SEGEMENT

# OVERVIEW
# This is the code that I use to produce a few different visualizations.
# The first visualization is a choropleth of all the US states and their respective acres burned.

# The second/third visualization are subplots on the same figure. One is a line graph representing the acres
# -> burned over time, and one is a bubble chart representing the acres over time with
# -> respect to the amount of fires happening in a time period.

# The fourth visualization has two diferent variations, one animated by year and one still (yet interactive) one.
# -> It showcases the different counties in california and amount of acres destroyed in specific counties by california
# -> fires in the last few years.

# The fifth and sixth visualization are on the same figure, but are toggled between using buttons.
# -> the fifth visualization is a pie chart of how many fires per region happened in 2022
# -> the sixth visualization is a bar chart of the same data.

# CODE

# imports necessary
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import chart_studio.plotly as py
import chart_studio
import plotly.tools as tls
from plotly.subplots import make_subplots

from urllib.request import urlopen

# I will want to at the end, embed all these visualizations into some sort of site.
# I did a Wix site as not all plotly functions are available in a pure HTML page 
# (which I was going to code a quick layout)
# Plotly Hover Text is not HTML, but it does work when you embed an iframe
# So, I push these to my plotly account, where I can get the code for the iframe and embed in Wix.

# binds this to my plotly account so i can push visualizations there
username = 'sanjanams'
# specific api key
api_key = '1HYbr3CiGDF6zERu2RwQ'
# sets the usernames and credentials so it pushes to my account
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)


# Many medium sized datasets, around 100 lines or so except for California Fires which had many rows
# Reads all of the different datasets in
# Every dataset is so niche and specific, I had to find different datasets since it wasn't all included
# Many sites just had visualizations (like government ones), not csvs or files to download with raw data
# I could have merged them, but it would have been a super large set and is easier to not
# This way I can keep track of what data I am using easier. 

california_fires = pd.read_csv(
   "path")
geohumancausedfires_number = pd.read_csv(
    "path")
states_fires = pd.read_csv(
    "path")
acres_over_time = pd.read_csv(
    "path")


# CLEANING

# states_fires cleaning
states_fires.drop_duplicates()

# This choropleth is generated by area code, specific areas don't have one
# Drop those, as well as the last column which is a total
states_fires.drop(states_fires.index[39], axis=0, inplace=True)
states_fires.drop(states_fires.index[-1], axis=0, inplace=True)
states_fires.drop(states_fires.index[8], axis=0, inplace=True)

# Creates a new column for hover text
states_fires['onhovertext'] = states_fires['State'] + '<br>' + \
    'Number of Fires: ' + states_fires['Number of fires']

# Removes commas and converts data types
states_fires['Number of fires'] = states_fires['Number of fires'].str.replace(
    ',', '')
states_fires['Number of acres burned '] = states_fires['Number of acres burned '].str.replace(
    ',', '')
states_fires['Number of acres burned '] = states_fires['Number of acres burned '].astype(
    float)

# acres_over_time cleaning
# Similar to above, removes commas and converts to floats
# This didn't have many columns, just rows, and was pretty clean
acres_over_time['Fires'] = acres_over_time['Fires'].str.replace(',', '')
acres_over_time['Acres'] = acres_over_time['Acres'].str.replace(',', '')
acres_over_time["Fires"] = acres_over_time["Fires"].astype(float)
acres_over_time["Acres"] = acres_over_time["Acres"].astype(float)

# geohumancausedfires_number cleaning

# Column name is supposed to be fires not acres, i accidentally changed something on excel and couldnt get it back
# Just change the name here and remove commas
geohumancausedfires_number['Fires'] = geohumancausedfires_number['Acres'].str.replace(
    ',', '')
# Convert to float
geohumancausedfires_number["Fires"] = geohumancausedfires_number["Fires"].astype(
    float)
# Fill null with 0s
geohumancausedfires_number['Fires'].fillna(0, inplace=True)
#Drop duplicates
california_fires.drop_duplicates()

# california_fires cleaning
# Fill any null values
california_fires['AcresBurned'].fillna(1, inplace=True)
california_fires['Active'].fillna(False, inplace=True)
# Hover text data column
california_fires['Additional Data '] = "<br>" + 'Acres Burned: ' + california_fires['AcresBurned'].astype(
    str) + '<br>' + 'Admin Unit: ' + california_fires['AdminUnit'] + '<br>' + "<br>" + "County: " + california_fires["Counties"]
# Renaming
california_fires['Year'] = california_fires["ArchiveYear"]
california_fires['StructuresEvacuated'].fillna(0, inplace=True)

# CREATING VISUALIZATIONS

# Vis One, the Choropleth of all US States 
# Plotly Graph Objects
choroplethstates = go.Figure(data=go.Choropleth(
    # Sets Locations and data
    # Locations in Plotly Built in US States Match By the State Code Name
    locations=states_fires['state code'],
    z=states_fires['Number of acres burned '].astype(float),
    locationmode='USA-states',
    colorbar_title="Number of Acres",
    hovertext=states_fires['onhovertext'],
    marker_line_color='grey',
    # Color Scale
    autocolorscale=False,
    colorscale=[[0, "rgb(255,186,186)"],
                [0.1, "rgb(255,123,123)"],
                [0.3, "rgb(255,82,82)"],
                [0.5, "rgb(255,82,82)"],
                [0.7, "rgb(255,0,0)"],
                [0.9, "rgb(167,0,0)"],
                [1, "rgb(167,0,0)"]]))

# Adds a title, and shows blue lakes
choroplethstates.update_layout(
    title_text='Number of Acres Burnt by State in 2021',
    geo=dict(
        scope='usa',
        showlakes=True,
        lakecolor='#1f77b4'
    )
)


# code for pushing this vis to plotly
# I also experimented with the choropleth's HTML being generated but that was a pain
py.plot(choroplethstates, filename = 'Fires in a state 2021', auto_open=True)
pio.write_html(choroplethstates, file="index.html", auto_open=True)
# Shows it
choroplethstates.show()

# Creation of visualization two and three

# Creates a new data set that has labels for years and acres

acresdf = pd.DataFrame(
    {'x': acres_over_time["Year"], 'y': acres_over_time["Acres"]})

# This figure has two subplots
line_chart = make_subplots(rows=2, cols=1)

# Adds a trace on the first subplot
# This trace is a line that shows the acres burnt over time
line_chart.add_trace(go.Line(
    x=acres_over_time['Year'], y=acres_over_time['Acres'], line=dict(color="orange")), row=1, col=1)

# Adds the title
line_chart.update_traces(go.Line(x=acres_over_time['Year'], y=acres_over_time['Acres'], line=dict(
    color="orange")), row=1, col=1, name="Number of US Acres Burned Over Time")
# Makes sure that the types are all floats and the y axis is in order
line_chart.update_layout(autotypenumbers='convert types')
# Adds a scatter line on top to highlight in red when the number of fires in that time period is more than 70k
line_chart.add_scattergl(x=acres_over_time['Year'], y=acres_over_time["Acres"].where(
    acres_over_time["Fires"] > 70000), mode='lines+markers', line={'color': 'red'}, name="More than 70k fires in the Time", row=1, col=1)

# part two of that visual
# Row Number two
# Adds a scatter chart - the bubbles size will depend on the number of fires, making it a bubble chart
line_chart.add_trace(go.Scatter(
    x=acres_over_time['Year'], y=acres_over_time['Acres'], mode='markers'), row=2, col=1)
# Puts the size and colors, scaled down the size 
line_chart.update_traces(go.Scatter(x=acres_over_time['Year'], y=acres_over_time['Acres'], mode='markers'),
                         marker=dict(
    size=acres_over_time['Fires'].astype(float)/1600,
    color='red'),
    name="Number of Fires",
    row=2,
    col=1
)
# Adds the scatter
line_chart.update_traces(go.Scatter(
    x=acres_over_time['Year'], y=acres_over_time['Acres']), row=2, col=1)
# Adds the x axes
line_chart.update_yaxes(title_text="Acres", row=1, col=1)
line_chart.update_xaxes(title_text="Year", row=1, col=1)

line_chart.update_yaxes(title_text="Acres", row=2, col=1)
line_chart.update_xaxes(title_text="Year", row=2, col=1)
# Height and width of the 
line_chart.update_layout(height=680, width=1380,
                         title_text="Acres Burnt Over Time Due to Climate Change Sparked Wildfires")
# SHows the chart
line_chart.show()
# Pushes to plotly
py.plot(line_chart, filename = 'Acres Burnt Over Time Due to Climate Change Sparked Wildfires', auto_open=True)

# Creates the fourth visualization
# california chart is the one with animations
# Renames this column
california_fires["Acres Burned"] = california_fires["AcresBurned"]
# Scatter Geo allows you to positiion by lat/lon
# Adds hover data
# This one is animated by year
californiachart = px.scatter_geo(
    california_fires,
    lat=california_fires["Latitude"],
    lon=california_fires["Longitude"],
    hover_name="Name",
    size=california_fires["Acres Burned"].astype(float),
    hover_data=[california_fires['Additional Data ']],
    animation_frame="Year",
    color="Acres Burned",
    color_continuous_scale="sunsetdark"

)

# Adds title
californiachart.update_layout(
    title='Animated Chart of California Fires with Size Burned in Acres',
    geo_scope='usa'

)
# Zoom start and projection scale
californiachart.update_geos(center=dict(lon=-119, lat=36))
californiachart.update_geos(projection_scale=2)

# Essentially the same code but without the animation to created a non-animated variation
# Hover data is the column for additional data
californiachartnoani = px.scatter_geo(
    california_fires,
    lat=california_fires["Latitude"],
    lon=california_fires["Longitude"],
    hover_name="Name",
    size=california_fires["Acres Burned"].astype(float),
    hover_data=[california_fires['Additional Data ']],
    color="Year",
    color_continuous_scale="sunsetdark"

)

# Adds title
californiachartnoani.update_layout(
    title='California Fires with Size Burned in Acres',
    geo_scope='usa'

)
# Zoom
californiachartnoani.update_geos(center=dict(lon=-119, lat=36))
californiachartnoani.update_geos(projection_scale=2)
# Shows both of them
californiachartnoani.show()
californiachart.show()

# Pushes to Plotly
py.plot(californiachartnoani, filename = 'California Fires Chart', auto_open=True)
py.plot(californiachart, filename='California Fires Chart Animated', auto_open=True)

# Creates a new df with only the year being 2022
dftwentytwo = geohumancausedfires_number.query("Year == 2022")

# Array of colors
colors = ['lightgoldenrodyellow', 'orange', 'salmon', 'orangered', 'tomato', 'palevioletred',
          'yellow', 'coral', 'darkred', 'red', 'crimson']

# creates a pie chart with the labels being each of the regions, but the values are the 2022 values
pie = go.Figure(data=[go.Pie(labels=['Alaska', 'Northwest', 'Northern California', 'Southern California', 'Northern Rockies', 'Great Basin', 'Western Great Basin', 'Southwest', 'Rocky Mountains', 'Eastern Area', 'Southern Area'],
                             values=dftwentytwo["Fires"])])
# Updates the graph with the colors to match with the labels
pie.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
# Title
pie.update_layout(
    title_text='Makeup of Human Sparked Wildfires By Location in the US, 2022', title_x=0.5, title_y=0.9)

# Code to create buttons to switch between pie and a bar version of this
# The method is restyle to use the same data
pie.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",

            buttons=list([
                dict(
                    args=["type", "pie"],
                    label="Pie Chart",
                    method="restyle"
                ),
                dict(
                    args=["type", "bar"],
                    label="Bar Chart",
                    method="restyle",


                )
            ]),
        ),
    ]
)
# Shows and pushes to plotly
pie.show()
py.plot(pie, filename = 'Makeup of Human Sparked Wildfires By Location in the US, 2022', auto_open=True)