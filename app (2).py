
import streamlit as st
import random
import time
import pandas as pd

# Przygotowanie bodźwców
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

# Inicjalizacja
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

# Ekran początkowy
if not st.session_state.experiment_started:
    st.title("Eksperyment: Klasyfikacja słów")
    st.write("Twoim zadaniem będzie przyporządkowanie wyświetlanych słów do jednej z dwóch kategorii:")
    st.markdown("- **Prawdziwe słowa** (np. "dom", "cat")")
    st.markdown("- **Pseudowyrazy** (np. "klopar", "brimpol")")
    st.write("
Użyj przycisków, aby dokonać wyboru:")
    st.markdown("- **Z** - Prawdziwe słowo")
    st.markdown("- **M** - Pseudowyraz")
    st.write("Po naciśnięciu przycisku "Start", eksperyment się rozpocznie.")

    if st.button("Start"):
        st.session_state.experiment_started = True
        st.session_state.start_time = time.time()

# Ekran eksperymentu
elif st.session_state.current_index < len(stimuli):
    stimulus = stimuli[st.session_state.current_index]
    st.markdown(f"<h1 style='text-align: center; font-size: 4em;'>{stimulus['word']}</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Z (Prawdziwe słowo)"):
            record_response("z")
    with col2:
        if st.button("M (Pseudowyraz)"):
            record_response("m")

    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

# Ekran końcowy
else:
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

