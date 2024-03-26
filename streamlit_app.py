import streamlit as st
from snowflake.snowpark.context import get_active_session


# Get the active Snowflake session
session = get_active_session()

# Execute query to retrieve regions from Snowflake
query_regions = "SELECT DISTINCT region FROM weather_db.weather_schema.indian_weather"
regions = session.sql(query_regions).to_pandas()['REGION'].tolist()

# Set page configuration with wide layout and title
st.set_page_config(
    layout="wide",
    page_title="INDIAN WEATHER :cloud: :sunny:"
)

# Rest of your Streamlit app code goes here
st.title("INDIAN WEATHER :cloud: :sunny:")  # This title can be removed if redundant


# Create dropdown menu to select region
selected_region = st.selectbox("Select Region", regions)

# Execute query to retrieve location names for the selected region from Snowflake
query_location_names = f"SELECT DISTINCT location_name FROM weather_db.weather_schema.indian_weather WHERE region = '{selected_region}'"
location_names = session.sql(query_location_names).to_pandas()['LOCATION_NAME'].tolist()

# Create dropdown menu to select location name within the selected region
selected_location_name = st.selectbox("Select Location Name", location_names)

# Execute query to retrieve data for the selected region and location_name
query_selected_data = f"""
SELECT *
FROM weather_db.weather_schema.indian_weather
WHERE region = '{selected_region}' AND location_name = '{selected_location_name}'
"""
selected_data = session.sql(query_selected_data).to_pandas()

# Display selected data
st.write("Selected Data:")
st.write(selected_data)


# Create a dropdown menu to select the parameter to plot
parameters = ["Temperature (Celsius)", "Temperature (Fahrenheit)", "Humidity", "Condition Text", "Wind Speed (kph)", "Visibility (km)", "Air Quality (Carbon Monoxide)", "Sunrise", "Sunset"]
selected_parameter = st.selectbox("Select Parameter to Plot", parameters)

# Plot the selected parameter
if selected_parameter == "Temperature (Celsius)":
    chart_data = selected_data[['LAST_UPDATED', 'TEMPERATURE_CELSIUS']]
    st.line_chart(data=chart_data.set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("Temperature (Celsius)")
elif selected_parameter == "Temperature (Fahrenheit)":
    chart_data = selected_data[['LAST_UPDATED', 'TEMPERATURE_FAHRENHEIT']]
    st.line_chart(data=chart_data.set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("Temperature (Fahrenheit)")
elif selected_parameter == "Humidity":
    chart_data = selected_data[['LAST_UPDATED', 'HUMIDITY']]
    st.line_chart(data=chart_data.set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("Humidity")
elif selected_parameter == "Condition Text":
    st.bar_chart(data=selected_data['CONDITION_TEXT'].value_counts())
    st.subheader("Condition Text")
elif selected_parameter == "Wind Speed (kph)":
    chart_data = selected_data[['LAST_UPDATED', 'WIND_KPH']]
    st.line_chart(data=chart_data.set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("Wind Speed (kph)")
elif selected_parameter == "Visibility (km)":
    chart_data = selected_data[['LAST_UPDATED', 'VISIBILITY_KM']]
    st.line_chart(data=chart_data.set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("Visibility (km)")
elif selected_parameter == "Air Quality (Carbon Monoxide)":
    chart_data = selected_data[['LAST_UPDATED', 'AIR_QUALITY_CARBON_MONOXIDE']]
    st.line_chart(data=chart_data.set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("Air Quality (Carbon Monoxide)")
elif selected_parameter == "Sunrise":
    chart_data = selected_data[['LAST_UPDATED', 'SUNRISE']]
    st.line_chart(data=chart_data.set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("Sunrise")
elif selected_parameter == "Sunset":
    chart_data = selected_data[['LAST_UPDATED', 'SUNSET']]
    st.line_chart(data=chart_data.set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("Sunset")

# Add another type of graph supported by Snowflake and Streamlit
if selected_parameter == "Humidity":  # Example: Bar chart for Humidity
    st.bar_chart(data=selected_data[['LAST_UPDATED', 'HUMIDITY']].set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("Humidity Bar Chart")

# Add another type of graph supported by Snowflake and Streamlit
if selected_parameter == "Temperature (Celsius)":  # Example: Bar chart for Humidity
    st.bar_chart(data=selected_data[['LAST_UPDATED', 'TEMPERATURE_CELSIUS']].set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("Temperature (Celsius) Bar Chart")

# Add another type of graph supported by Snowflake and Streamlit
if selected_parameter == "Wind Speed (kph)":  # Example: Bar chart for Humidity
    st.bar_chart(data=selected_data[['LAST_UPDATED', 'WIND_KPH']].set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("WIND_KPH Bar Chart")

# Add another type of graph supported by Snowflake and Streamlit
if selected_parameter == "Visibility (km)":  # Example: Bar chart for Humidity
    st.bar_chart(data=selected_data[['LAST_UPDATED', 'VISIBILITY_KM']].set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("Visibility (km) Bar Chart")

# Add another type of graph supported by Snowflake and Streamlit
if selected_parameter == "Air Quality (Carbon Monoxide)":  # Example: Bar chart for Humidity
    st.bar_chart(data=selected_data[['LAST_UPDATED', 'AIR_QUALITY_CARBON_MONOXIDE']].set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("Temperature (Celsius) Bar Chart")

# Add another type of graph supported by Snowflake and Streamlit
if selected_parameter == "Condition Text":  # Example: Bar chart for Humidity
    st.bar_chart(data=selected_data[['LAST_UPDATED', 'CONDITION_TEXT']].set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("Condition Text Bar Chart")

# Add another type of graph supported by Snowflake and Streamlit
if selected_parameter == "Sunrise":  # Example: Bar chart for Humidity
    st.bar_chart(data=selected_data[['LAST_UPDATED', 'SUNRISE']].set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("Sunrise Bar Chart")

# Add another type of graph supported by Snowflake and Streamlit
if selected_parameter == "Sunset":  # Example: Bar chart for Humidity
    st.bar_chart(data=selected_data[['LAST_UPDATED', 'SUNSET']].set_index('LAST_UPDATED'), use_container_width=True)
    st.subheader("Sunset Bar Chart")



# Interactive map with wider layout using CSS
st.subheader("Interactive Map")
st.map(selected_data)
