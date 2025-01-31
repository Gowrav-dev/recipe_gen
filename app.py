import streamlit as st
import requests
import random
from streamlit_lottie import st_lottie

# Spoonacular API Key (Replace with your own key)
API_KEY = "your_api_key"
BASE_URL = "https://api.spoonacular.com/recipes"

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()    

# Load Lottie animation
lottie_cooking = load_lottieurl("https://lottie.host/09c65bcf-f7d5-47e4-94a6-0982e68bb50a/99n67ElJui.json")

# Function to fetch a random meal from Spoonacular
def get_random_meal():
    url = f"{BASE_URL}/random?apiKey={API_KEY}&number=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["recipes"][0]
    return None

# Function to fetch meal categories (Spoonacular uses cuisines instead of categories)
def get_meal_categories():
    return ["Italian", "Mexican", "Indian", "Chinese", "American", "French", "Japanese", "Mediterranean"]

# Function to fetch meals by cuisine
def get_meals_by_cuisine(cuisine):
    url = f"{BASE_URL}/complexSearch?apiKey={API_KEY}&cuisine={cuisine}&number=5"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["results"]
    return []

# Function to fetch a recipe by ID
def get_recipe_details(recipe_id):
    url = f"{BASE_URL}/{recipe_id}/information?apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Function to set background with wavy design
def set_background():
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(135deg, #d4fc79 10%, #96e6a1 100%);
                background-attachment: fixed;
                height: 100vh;
            }
            .wave {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 250px;
                background: url('https://www.transparenttextures.com/patterns/wavecut.png');
                opacity: 0.2;
            }
        </style>
        <div class='wave'></div>
        """, unsafe_allow_html=True
    )

# Apply background
set_background()

# Centered Lottie animation with adjusted width
col1, col2 = st.columns([2, 1])  # Left takes 2 parts, Right takes 1 part

with col2:  # Placing the animation in the right column
    if lottie_cooking:
        st_lottie(lottie_cooking, height=200, width=200, key="cooking_animation")
    else:
        st.error("Lottie animation failed to load.")


# Streamlit UI with enhanced styling
st.markdown(
    """
    <style>
        .title {
            font-size: 100px !important;
            font-weight: bold;
            text-align: center;
            color: brown;
            text-shadow: 3px 3px 5px rgba(0,0,0,0.3);
        }
        .subheader {
            font-size: 40px;
            font-weight: 500;
            color: #ff6347;
            text-align: center;
        }
        .text {
            font-size: 20px;
            font-weight: 300;
            color: #ffffff;
            text-align: center;
        }
        .stButton>button {
            background-color: #ff4500;
            color: white;
            font-size: 20px;
            border-radius: 10px;
            padding: 10px 20px;
            border: none;
        }
        .stSelectbox, .stTextInput {
            background-color: white;
            color: black;
            font-size: 18px;
        }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("<p class='title'> Food Generator</p>", unsafe_allow_html=True)
st.markdown("<p class='text'>Discover random meals or choose based on cuisines!</p>", unsafe_allow_html=True)

# Fetch and display a random meal
if st.button("🔄 Generate Random Meal"):
    meal = get_random_meal()
    if meal:
        st.markdown(f"<p class='subheader'>{meal['title']}</p>", unsafe_allow_html=True)
        st.image(meal["image"], caption=meal["title"], width=500)
        st.write("**Ready in:**", meal["readyInMinutes"], "minutes")
        st.write("**Instructions:**")
        instructions = meal.get("instructions", "No instructions available.").split('.')
        for step in instructions:
            if step.strip():
                st.write(f"- {step.strip()}.")
    else:
        st.error("Couldn't fetch a meal. Try again!")

# Dropdown for meal cuisines
cuisines = get_meal_categories()
selected_cuisine = st.selectbox("Choose a cuisine", cuisines)

if selected_cuisine:
    meals = get_meals_by_cuisine(selected_cuisine)
    meal_options = {meal['title']: meal['id'] for meal in meals}
    selected_meal = st.selectbox("Choose a dish", list(meal_options.keys()))

    if selected_meal:
        meal_id = meal_options[selected_meal]
        recipe_details = get_recipe_details(meal_id)
        if recipe_details:
            st.markdown(f"<p class='subheader'>{recipe_details['title']}</p>", unsafe_allow_html=True)
            st.image(recipe_details["image"], caption=recipe_details["title"], width=500)
            st.write("**Ready in:**", recipe_details["readyInMinutes"], "minutes")
            st.write("**Ingredients:**")
            for ingredient in recipe_details.get("extendedIngredients", []):
                st.write(f"- {ingredient['original']}")
            st.write("**Instructions:**")
            instructions = recipe_details.get("instructions", "No instructions available.").split('.')
            for step in instructions:
                if step.strip():
                    st.write(f"- {step.strip()}.")
        else:
            st.error("Could not fetch recipe details. Try again!")
