# -*- coding: utf-8 -*-
import re # noqa

import nltk.data

import pdfplumber


def split_into_sentences(text):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sentences = [sent.replace('\n', '') for sent in tokenizer.tokenize(text)]
    return sentences


def split_into_words(text):
    words = re.findall('[a-zа-яё]+', text, flags=re.IGNORECASE)
    return words


def open_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        pages = pdf.pages
        pdf_text = ''.join(page.extract_text() for page in pages)
    return pdf_text
