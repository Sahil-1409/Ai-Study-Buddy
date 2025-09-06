import streamlit as st
from utils import summarize_text, generate_mcqs, generate_flashcards, export_flashcards_csv

st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="wide")

st.markdown("# 📚 AI Study Buddy")
st.caption("Turn your notes into Summaries, MCQs, and Flashcards — perfect for fast revision.")

with st.sidebar:
    st.header("⚙️ Settings")
    num_sentences = st.slider("Summary length (sentences)", 2, 10, 5)
    num_mcqs = st.slider("How many MCQs?", 3, 15, 5)
    num_cards = st.slider("How many flashcards?", 5, 30, 10)

st.info("Paste your lecture notes below, or use the sample notes.", icon="✍️")

sample = st.checkbox("Use sample notes")
if sample:
    with open("assets/sample_notes.txt", "r", encoding="utf-8") as f:
        default_text = f.read()
else:
    default_text = ""

text = st.text_area("Your notes", value=default_text, height=260)

tab1, tab2, tab3 = st.tabs(["📝 Summary", "🧠 MCQs", "🎴 Flashcards"])

with tab1:
    if st.button("Generate Summary"):
        if not text.strip():
            st.warning("Please paste some text.")
        else:
            summary = summarize_text(text, max_sentences=num_sentences)
            st.success("Summary:")
            st.write(summary)

with tab2:
    if st.button("Generate MCQs"):
        if not text.strip():
            st.warning("Please paste some text.")
        else:
            mcqs = generate_mcqs(text, n=num_mcqs)
            for i, q in enumerate(mcqs, 1):
                st.markdown(f"**Q{i}.** {q['question']}")
                choice = st.radio("Choose:", q['options'], index=None, key=f"q{i}")
                if choice:
                    if choice == q['answer']:
                        st.success("✅ Correct")
                    else:
                        st.error(f"❌ Wrong. Answer: {q['answer']}")

with tab3:
    if st.button("Generate Flashcards"):
        if not text.strip():
            st.warning("Please paste some text.")
        else:
            cards = generate_flashcards(text, n=num_cards)
            for i, card in enumerate(cards, 1):
                with st.expander(f"Card {i}: {card['front']}"):
                    st.write(card["back"])
            csv_bytes = export_flashcards_csv(cards)
            st.download_button("⬇️ Download CSV", data=csv_bytes,
                               file_name="flashcards.csv", mime="text/csv")

st.markdown("---")
st.caption("Made by Sahil — BTech 1st Year")
