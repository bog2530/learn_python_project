from app import app, db # noqa
from app.models import Book, Dictionary, Sentence, Translation, User, Word, book_word, dictionary_word


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Book': Book, 'BookWord': book_word,
            'Dictionary': Dictionary, 'DictionaryWord': dictionary_word, 'Sentence': Sentence,
            'Translation': Translation, 'Word': Word}
