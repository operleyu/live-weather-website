import base64
import os
import requests
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Live Weather App", page_icon="🌤️", layout="wide") # Sets the main title

def get_base64_video(path): # Converts the MP4 into base64 so it can be used with streamlit
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

VIDEO_PATH = os.path.join(os.path.dirname(__file__), "F16.mp4") # Finds the video of F16.mp4 and makes it a background
video_base64 = get_base64_video(VIDEO_PATH)

st.markdown( # Changes the main title font
    """
    <style>
    .stApp h1 {
        font-family: 'Segoe Script', cursive;
    }

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stHeader"],
    .main, section.main, .block-container {
        background: transparent !important;
    }

    [data-testid="stAppViewContainer"] {
        position: relative !important;
        z-index: 2 !important;
    }

    iframe[title="st.iframe"] {
        position: fixed !important;
        top: 0;
        left: 0;
        width: 100vw !important;
        height: 100vh !important;
        z-index: -1;
        border: none;
    }

    .stApp, .stApp p, .stApp label, .stApp h1, .stapp h2, .stApp h3 {
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
                 
components.html( # - Autoplays, loop, and mutes and forces the video to play where it is exactly on the page
    f"""
    <video autoplay loop muted playsinline 
        style="position:fixed; top:0; left:0; width:100vw; height:100vh; object-fit:cover; z-index:-2;">
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
    </video>
    <div style="position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.45); z-index:-1;"></div>
    """,
    height=0,
)

st.title("Live Weather") # Title
st.write("Check current weather conditions from anywhere in the world!") # Description

st.markdown( # Description with clickable links
    'Don\'t have an API key? [Get your API key here](https://openweathermap.org/api)'
)
api_key = st.text_input( # Makes API key functional
    "Enter OpenWeatherMap API Key", type="default", autocomplete="new-password",
)

cities = [ # Each cities for selection box
    "Bangkok",
    "Jakarta",
    "Hanoi",
    "Manila",
    "Beijing",
    "Tokyo",
    "Seoul",
    "Moscow",
    "Abu Dhabi",
    "Doha",
    "Riyadh",
    "Baku",
    "New Delhi",
    "New York",
    "Los Angeles",
    "Clairo",
    "Rome",
    "London",
    "Paris",
    "Berlin",
    "Amsterdam",
    "Madrid",
    "Bratislava",
    "Prague",
    "Warsaw",
    "Vienna",
    "Kyiv",
    "Ottawa",
    "Mexico City",
    "Brasília",
    "Buenos Aires"
]
city = st.selectbox("Select a city or type out here!", cities) # Makes selectbox possible

if st.button("Get Weather"): # Gets the live weather data when the user selects a city and presses "Get Weather"
    if not api_key:
        st.error("Please enter your API key!")
    elif not city:
        st.error("Please enter a city name!")
    else:
        with st.spinner(f"Fetching weather for {city}..."):
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": api_key, "units": "metric"}
            response = requests.get(url, params=params)
            data = response.json()

            if response.status_code == 200:
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                description = data["weather"][0]["description"].title()

                st.success(f"Weather in {city}:")
                st.metric(label="Temperature", value=f"{temp}°C")
                st.metric(label="Humidity", value=f"{humidity}%")
                st.write(f"**Conditions:** {description}")
            else:
                st.error(f"Error: {data.get('message', 'Could not fetch weather')}")
