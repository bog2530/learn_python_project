# -*- coding: utf-8 -*-

import pdfplumber

import re # noqa

alphabets = "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)" # noqa W605
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"


def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text) # noqa W605
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" "+suffixes+"[.] "+starters, " \\1<stop> \\2", text)
    text = re.sub(" "+suffixes+"[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text:
        text = text.replace(".”", "”.")
    if "\"" in text:
        text = text.replace(".\"", "\".")
    if "!" in text:
        text = text.replace("!\"", "\"!")
    if "?" in text:
        text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


def split_into_words(text):
    words = re.findall('[a-zа-яё]+', text, flags=re.IGNORECASE)
    return words


with pdfplumber.open('samplex.pdf') as pdf:
    pages = pdf.pages
    pdf_text = ''
    for page in pages:
        pdf_text += page.extract_text()

pdf_file = open('pdf_file.txt', 'w', encoding='utf-8')
pdf_file.write(pdf_text)
print('end')

with open('pdf_file.txt', 'r', encoding='utf-8') as file:
    pdf_text = file.read()
    pdf_word = split_into_words(pdf_text)
    pdf_word = '||'.join(pdf_word)
    pdf_text = split_into_sentences(pdf_text)
    pdf_text = '||'.join(pdf_text)
    pdf_text = pdf_text.replace('  ', ' ')
    pdf_text = pdf_text.replace('   ', ' ')
    pdf_text = pdf_text.replace('    ', ' ')
    pdf_text = pdf_text.replace('     ', ' ')
    pdf_text = pdf_text.replace('      ', ' ')
    pdf_text = pdf_text.replace('       ', ' ')
    pdf_text = pdf_text.replace('        ', ' ')


with open('new_pd.txt', 'w', encoding='utf-8') as write_file:
    write_file.write(pdf_text)
print('done')

with open('new_pd_words.txt', 'w', encoding='utf-8') as write_files:
    write_files.write(pdf_word)
print('done')
