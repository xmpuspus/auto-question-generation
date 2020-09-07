import streamlit as st
from gensim.summarization import summarize, keywords
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.reduction import ReductionSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk; nltk.download('punkt')
from text2text.text_generator import TextGenerator

# Load QuestionGen model
qg = TextGenerator(output_type="question")


# Header
### Set Title
st.title("Question Generator")
st.markdown("""Generates questions from a long paragraph based on [this reference](https://arxiv.org/abs/1810.04805). The AI can generate questions from either a website link or from plain text.""")

# Question Count
question_count = st.slider('Number of questions to generate', 1, 20, 3, 1)

input_text_type = st.selectbox("Type of Input (Text or Link?)", ["Text", "Link"])


if input_text_type=="Text":

    # Text input
    text = st.text_area("Input long paragraph:", """Thomas A. Anderson is a man living two lives. By day he is an average computer programmer and by night a hacker known as Neo. Neo has always questioned his reality, but the truth is far beyond his imagination. Neo finds himself targeted by the police when he is contacted by Morpheus, a legendary computer hacker branded a terrorist by the government. Morpheus awakens Neo to the real world, a ravaged wasteland where most of humanity have been captured by a race of machines that live off of the humans' body heat and electrochemical energy and who imprison their minds within an artificial reality known as the Matrix. As a rebel against the machines, Neo must return to the Matrix and confront the agents: super-powerful computer programs devoted to snuffing out Neo and the entire human rebellion.""", height=250)
    

    questions_generator = qg.predict([text]*question_count)
    questions_list = [i[0] for i in questions_generator]
    answers_list = [i[1] for i in questions_generator]
    st.subheader("Generated Questions")
    
    for i in range(len(questions_list)):
        st.write(questions_list[i])
        st.text(f"Possible answer is along the lines of: {answers_list[i]}")
        
else:
    # Link input
    link = st.text_input("Input website/link here:", "https://www.osapabroad.com/academics/the-oxford-tutorial/")
    st.subheader("Generated Questions")
    LANGUAGE = "english"
    SENTENCES_COUNT = 100

    try:
        parser = HtmlParser.from_url(link, Tokenizer(LANGUAGE))
        # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))

        stemmer = Stemmer(LANGUAGE)

        # summarizer = LsaSummarizer(stemmer)
        summarizer = ReductionSummarizer(stemmer)

        summarizer.stop_words = get_stop_words(LANGUAGE)

        sentences_list = [str(sentence) for sentence in summarizer(parser.document, SENTENCES_COUNT)]

        summary_text = "\n".join(sentences_list)

        questions_generator = qg.predict([summary_text]*question_count)
        questions_list = [i[0] for i in questions_generator]

        for i in range(len(questions_list)):
            st.write(questions_list[i])
            st.text(f"Possible answer is along the lines of: {answers_list[i]}")
    except:
        st.write("Link cannot be parsed.")
