import streamlit as st
from gensim.summarization import summarize, keywords
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.reduction import ReductionSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk; nltk.download('punkt')

# Header
### Set Title
st.title("Text Summarizer")
st.markdown("""Summarize a long paragraph based on [this reference](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf). You can summarize from either a website link or from plain text.""")

input_text_type = st.selectbox("Type of Input (Text or Link?)", ["Link", "Text"])


if input_text_type=="Text":
    
    # Ratio of words as summary output
    ratio = st.sidebar.slider("Summary Ratio: ", 0., 1., 0.2, 0.01)


    # Text input
    text = st.text_area("Input long paragraph:", """Thomas A. Anderson is a man living two lives. By day he is an average computer programmer and by night a hacker known as Neo. Neo has always questioned his reality, but the truth is far beyond his imagination. Neo finds himself targeted by the police when he is contacted by Morpheus, a legendary computer hacker branded a terrorist by the government. Morpheus awakens Neo to the real world, a ravaged wasteland where most of humanity have been captured by a race of machines that live off of the humans' body heat and electrochemical energy and who imprison their minds within an artificial reality known as the Matrix. As a rebel against the machines, Neo must return to the Matrix and confront the agents: super-powerful computer programs devoted to snuffing out Neo and the entire human rebellion.""", height=250)

    # Word count
    # word_count = st.sidebar.number_input("Summary Word Count", 0, len(text.split(" ")))

    # Summarize
    summary = summarize(text, ratio=ratio)
    keywords_list = keywords(text, ratio=ratio).split("\n")
    if not summary:
        st.write("Input a longer paragraph.")
    else:
        st.subheader("Summary")
        st.write(summary)
        st.markdown("**Keywords:** " + ", ".join("`" + i + "`" for i in keywords_list))
        
else:
    # Link input
    link = st.text_input("Input website/link here:", "https://www.osapabroad.com/academics/the-oxford-tutorial/")
    st.subheader("Summary")
    LANGUAGE = "english"
    SENTENCES_COUNT = st.sidebar.slider("Sentence Count", 1, 20, 10, 1)
    kw_ratio = st.sidebar.slider("Keyword Ratio: ", 0., 1., 0.2, 0.01)
#     SENTENCES_COUNT = 20
    try:
        parser = HtmlParser.from_url(link, Tokenizer(LANGUAGE))
        # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))

        stemmer = Stemmer(LANGUAGE)

        # summarizer = LsaSummarizer(stemmer)
        summarizer = ReductionSummarizer(stemmer)

        summarizer.stop_words = get_stop_words(LANGUAGE)

        sentences_list = [str(sentence) for sentence in summarizer(parser.document, SENTENCES_COUNT)]

        summary_text = "\n".join(sentences_list)
        st.write(summary_text)

        keywords_list = keywords(summary_text, ratio=kw_ratio).split("\n")

        st.markdown("**Keywords:** " + ", ".join("`" + i + "`" for i in keywords_list))
    except:
        st.write("Link cannot be parsed.")
