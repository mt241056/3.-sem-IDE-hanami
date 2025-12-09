import altair as alt
import pandas as pd

# Load the dataset
df = pd.read_csv("all_cities_cat.csv")
df['seasonal_year'] = df['seasonal_year'].astype(int)

# 1. Define the interactive slider for the year
year_slider = alt.binding_range(
    min=1981,
    max=2025,
    step=1,
    name='Select Year:'
)

# 2. Define the selection linked to the slider
select_year = alt.selection_single(
    name="YearFilter",
    fields=['seasonal_year'],
    bind=year_slider,
    init={'seasonal_year': 2025}
)

# 3. Create the base map chart
chart = alt.Chart(df).mark_circle(size=100).encode(
    # X and Y represent the map coordinates (longitude and latitude)
    x=alt.X('longitude',
            scale=alt.Scale(domain=[128, 146]), # Constrained for Japan
            axis=None),

    y=alt.Y('latitude',
            scale=alt.Scale(domain=[30, 46]), # Constrained for Japan
            axis=None),

    # Color encodes the value we want to display
    color=alt.Color('bloom_day_of_year',
                    title='Bloom Day of Year',
                    scale=alt.Scale(range='heatmap', domain=[80, 140]), # Distinct color scheme
                    legend=alt.Legend(orient='bottom', titleLimit=400)),

    # Tooltips for interactivity
    tooltip=[
        alt.Tooltip('city_name', title='City'),
        alt.Tooltip('seasonal_year', title='Year'),
        alt.Tooltip('bloom_day_of_year', title='Day of Year')
    ],

).properties(
    title="Cherry Blossom Bloom Day (Days Since Jan 1) by City"
).add_selection(
    select_year # Add the year filter selection
).transform_filter(
    select_year # Apply the filter to the data
)

# Save the chart as a JSON file
chart.save("japan_bloom_map_by_year.json")