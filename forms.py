from flask_wtf import FlaskForm
from wtforms import TextAreaField


class WordListForm(FlaskForm):
    bannedWords = TextAreaField('Banned Words')
    whiteList = TextAreaField('White List')
    blackList = TextAreaField('Black List')
