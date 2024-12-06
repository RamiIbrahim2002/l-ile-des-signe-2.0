import streamlit as st
import openai
import base64
import random
import logging

# 3DS OUTSCALE's judge please provide an open ai key (trying this NLP model will onlyh cost 0.000001$) thank you for your time !!!!

openai.api_key = "" #here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", filename="debug.log")

# Character database
characters = {
    "Guybrush Threepwood": {
        "image": "assets/images/characters/Guybrush Threepwood.png",
        "tone": "You are witty, humorous, and often sarcastic. You have a knack for turning situations into jokes and always try to lighten the mood."
    },
    "LeChuck": {
        "image": "assets/images/characters/LeChuck.png",
        "tone": "You are menacing, vengeful, and dramatic. You speak with a tone of authority and an air of villainy, often making threats or boasting about your power."
    },
    "Elaine Marley": {
        "image": "assets/images/characters/Elaine Marley.png",
        "tone": "You are intelligent, confident, and resourceful. You have a calm and composed demeanor, with a touch of humor to disarm others."
    }
}

# Function to convert image to base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to encode font file to base64
def encode_font(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# Encode font
font_base64 = encode_font("assets/fonts/lucasarts-scumm-solid.otf")

def background_music(audio_file_path):
    audio_file_base64 = get_base64_of_bin_file(audio_file_path)
    return f"""
        <audio autoplay loop>
            <source src="data:audio/mp3;base64,{audio_file_base64}" type="audio/mp3">
        </audio>
    """

# Add background music
audio_file_path = "assets/sounds/background_music.mp3"  # Path to your music file
st.markdown(background_music(audio_file_path), unsafe_allow_html=True)


# Paths to background images
backgrounds = {
    "Grog Shop": "assets/images/backgrounds/grog_shop.png",
    "Treasure Island": "assets/images/backgrounds/treasure_island.png"
}

# Initialize session state
if 'current_background' not in st.session_state:
    st.session_state.current_background = "Grog Shop"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to toggle background
def toggle_background():
    current_bg = st.session_state.current_background
    st.session_state.current_background = "Treasure Island" if current_bg == "Grog Shop" else "Grog Shop"

# Function to fetch the relevant character name from OpenAI
def choose_relevant_character(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant from Monkey Island. Select the most relevant character to respond to the input."},
                {"role": "user", "content": f"Given the input '{user_input}', which character should respond? Choose from: Guybrush Threepwood, LeChuck, Elaine Marley."}
            ],
            temperature=0.7,
            max_tokens=10
        )
        # Strip any unwanted characters from the response
        character_name = response['choices'][0]['message']['content'].strip()
        character_name = character_name.rstrip(".,")  # Remove trailing '.' or ',' if present
        logging.info(f"Character selection response: {character_name}")
        
        # Ensure the name matches a key in the characters dictionary
        if character_name in characters:
            return character_name
        else:
            logging.warning(f"Invalid character name received: {character_name}. Falling back to random selection.")
            return random.choice(list(characters.keys()))
    
    except Exception as e:
        logging.error(f"Error selecting character: {e}")
        return random.choice(list(characters.keys()))  # Fallback to random selection

# Function to fetch response in character's tone
def fetch_openai_response(character, user_input):
    tone = characters.get(character, {}).get("tone", "You are a unique character from Monkey Island.")
    try:
        # Log the prompt
        logging.info(f"Generating response as {character} with tone: {tone} and input: {user_input}")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are {character}, a character from Monkey Island."},
                {"role": "system", "content": tone},
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
            max_tokens=150
        )
        
        # Log the response
        result = response['choices'][0]['message']['content'].strip()
        logging.info(f"Response from OpenAI as {character}: {result}")
        return result
    
    except Exception as e:
        logging.error(f"Error fetching response: {e}")
        return f"Sorry, I couldn't process that. Please try again!"

# Convert current background to base64
current_background_path = backgrounds[st.session_state.current_background]
background_base64 = get_base64_of_bin_file(current_background_path)

# Inject CSS
st.markdown(
    f"""
    <style>
    @font-face {{
        font-family: 'LucasArtsSCUMM';
        src: url(data:font/otf;base64,{font_base64}) format('opentype');
    }}
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                          url('data:image/jpeg;base64,{background_base64}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .title {{
        font-family: 'LucasArtsSCUMM', cursive;
        color: gold;
        font-size: 2.5rem;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 30px;
        text-shadow: 2px 2px 5px black;
    }}
    .character-icon {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid gold;
        margin-right: 10px;
    }}
    .message-container {{
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }}
    .response-box {{
        background-color: rgba(0, 0, 0, 0.7);
        padding: 15px;
        border-radius: 10px;
        font-size: 1.2rem;
        color: #ffffff;
        font-family: 'LucasArtsSCUMM', cursive;
        flex-grow: 1;
    }}
    .stTextInput input {{
        font-family: 'LucasArtsSCUMM', cursive !important;
        color: gold !important;
        font-size: 1.2rem !important;
        background-color: rgba(0, 0, 0, 0.7) !important;
        border: 2px solid gold !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Main layout
st.markdown("<div class='title'>☠️ Monkey Island Chatbot</div>", unsafe_allow_html=True)

# Background toggle
st.button("⚓ Switch Background", on_click=toggle_background)
st.markdown(f"**Current Background:** {st.session_state.current_background}")

# Easter egg for water-related button
if st.button("💧 Save Ocean Water", on_click=toggle_background):
    # Switch to ocean-themed background
    st.session_state.current_background = "Ocean View"
    st.markdown(f"**Current Background:** {st.session_state.current_background}")
    
    # Trigger ocean sound (or any additional water-themed functionality)
    audio_file_path = "assets/sounds/waves.mp3"  # Path to ocean sound
    st.markdown(background_music(audio_file_path), unsafe_allow_html=True)

    # Display motivational message about saving ocean water
    st.markdown("**Let's protect our oceans and save water!** 🌊💧")
    
    # Show ocean-related image
    ocean_image_base64 = get_base64_of_bin_file("assets/images/backgrounds/ocean.png")
    st.markdown(f"""
        <img src="data:image/png;base64,{ocean_image_base64}" style="width: 100%; max-width: 800px; border-radius: 10px;">
    """, unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Type your question...")

if user_input:
    # Select the most relevant character
    selected_character = choose_relevant_character(user_input)
    logging.info(f"Selected character: {selected_character}")
    
    # Fetch response from OpenAI
    response = fetch_openai_response(selected_character, user_input)
    
    # Get character icon
    character_icon_base64 = get_base64_of_bin_file(characters[selected_character]['image'])
    
    # Create message with icon
    message_html = f"""
    <div class="message-container">
        <img src="data:image/png;base64,{character_icon_base64}" class="character-icon">
        <div class='response-box'>
            🏴‍☠️ {selected_character}: {response}
        </div>
    </div>
    """
    
    # Add to chat history
    st.session_state.chat_history.append(message_html)

# Display chat history
for message in st.session_state.chat_history:
    st.markdown(message, unsafe_allow_html=True)
