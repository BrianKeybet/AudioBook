import streamlit as st # Streamlit is used to create the Streamlit application
import gtts
from gtts import gTTS  # (Google’s Text-to-Speech) is used to convert text to speech
import pdfplumber      # pdfplumber is used to extract text from PDF files,
import docx            # docx is used to extract text from DOCX files
import ebooklib        # 
from ebooklib import epub #ebooklib and epub are used to extract text from EPUB files


st.title("AudioBook App - Text to Speech")
st.info('Convert your E-book to audiobook')
#Uploader Widget
book = st.file_uploader('Please upload your file', type=['pdf', 'txt', 'docx', 'epub'])


def extract_text_from_docx(file):
    doc = docx.Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_text_from_epub(file):
    book = epub.read_epub(file)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return '\n'.join(chapters)

if book:
    if book.type == 'application/pdf':
        all_text = ""
        with pdfplumber.open(book) as pdf:
            for text in pdf.pages:
                single_page_text = text.extract_text()
                all_text = all_text + '\n' + str(single_page_text)
    elif book.type == 'text/plain':
            all_text = book.read().decode("utf-8")
    elif book.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            all_text = extract_text_from_docx(book)
    elif book.type == 'application/epub+zip':
            all_text = extract_text_from_epub(book)
    else:
        st.error("Unsupported file type. Please upload a valid PDF, TXT, DOCX, or EPUB file.")
else:
    st.warning("Please upload a file to convert to audiobook.")

lang = "en" #Choose voice, "sw" is swahili, the list can be found here: http://gtts.readthedocs.org/ or print them out on the cli using > gtts-cli --all
tld = "co.uk" #Localised accents, "co.ke" is Kenyan, List found here: https://www.google.com/supported_domains


# Check if all_text is defined before creating the TTS object
if 'all_text' in locals():
    tts = gTTS(all_text, lang=lang)
    tts.save('audiobook.mp3')

    audio_file = open('audiobook.mp3', 'rb')
    audio_bytes = audio_file.read()

    st.audio(audio_bytes, format='audio/mpeg', start_time=0)