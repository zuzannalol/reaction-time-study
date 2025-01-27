
import streamlit as st
import random
import time
import pandas as pd
from streamlit_keypress import keypress

# Przygotowanie bodźców
polish_words = ["dom", "pies", "kot", "las", "stół", "krzesło", "okno", "droga", "szkoła", "miasto"]
english_words = ["house", "dog", "cat", "forest", "table", "chair", "window", "road", "school", "city"]
polish_pseudowords = ["klopar", "szytok", "pruszel", "brutol", "flepoz", "gonter"]
english_pseudowords = ["brimpol", "shoklin", "blonker", "frodle", "plirke", "gonkle"]

stimuli = (
    [{"word": word, "language": "polish", "is_real": True} for word in polish_words] +
    [{"word": word, "language": "english", "is_real": True} for word in english_words] +
    [{"word": word, "language": "polish", "is_real": False} for word in polish_pseudowords] +
    [{"word": word, "language": "english", "is_real": False} for word in english_pseudowords]
)
random.shuffle(stimuli)

# Inicjalizacja stanu aplikacji
if "results" not in st.session_state:
    st.session_state.results = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "experiment_started" not in st.session_state:
    st.session_state.experiment_started = False

# Funkcja do zapisania odpowiedzi
def record_response(key):
    if st.session_state.current_index < len(stimuli):
        stimulus = stimuli[st.session_state.current_index]
        reaction_time = time.time() - st.session_state.start_time
        is_correct = (key == "z" and stimulus["is_real"]) or (key == "m" and not stimulus["is_real"])

        st.session_state.results.append({
            "word": stimulus["word"],
            "language": stimulus["language"],
            "is_real": stimulus["is_real"],
            "reaction_time": round(reaction_time, 3),
            "correct": is_correct
        })

        st.session_state.current_index += 1
        st.session_state.start_time = time.time()

# Wprowadzenie i ekran startowy
if not st.session_state.experiment_started:
    st.title("Eksperyment: Decyzje leksykalne")
    st.write(
        "Celem tego eksperymentu jest zmierzenie czasu reakcji na różne słowa.
"
        "Będziesz widzieć na ekranie słowo. Twoim zadaniem jest ocenienie, czy jest to prawdziwe słowo, czy pseudowyraz.
"
        "
Instrukcje:
"
        "- Naciśnij **Z**, jeśli uważasz, że słowo jest prawdziwe.
"
        "- Naciśnij **M**, jeśli uważasz, że jest to pseudowyraz."
    )
    if st.button("START"):
        st.session_state.experiment_started = True
        st.session_state.start_time = time.time()
else:
    # Wyświetlanie bodźców
    if st.session_state.current_index < len(stimuli):
        stimulus = stimuli[st.session_state.current_index]

        st.markdown(f"<h1 style='text-align: center; font-size: 72px;'>{stimulus['word']}</h1>", unsafe_allow_html=True)

        # Obsługa klawiatury
        key = keypress()
        if key in ["z", "m"]:
            record_response(key)
            st.experimental_rerun()

    else:
        # Koniec eksperymentu
        st.write("Dziękujemy za udział w eksperymencie!")
        st.write("Wyniki:")
        df = pd.DataFrame(st.session_state.results)
        st.dataframe(df)

        # Pobierz wyniki jako CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Pobierz wyniki jako CSV",
            data=csv,
            file_name="wyniki.csv",
            mime="text/csv"
        )

