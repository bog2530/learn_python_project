# -*- coding: utf-8 -*-
import nltk.data

import pdfplumber

import re # noqa


def split_into_sentences(text):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = []
    for sentence in tokenizer.tokenize(text):
        sent = sentence.replace('\n', '')
        sentences.append(sent)
    return sentences


def split_into_words(text):
    words = re.findall('[a-zа-яё]+', text, flags=re.IGNORECASE)
    return words


def open_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        pages = pdf.pages
        pdf_text = ''
        for page in pages:
            pdf_text += (page.extract_text())
        pdf_text = pdf_text.strip(' ')
        pdf_text = pdf_text.strip('\n')
    return pdf_text
