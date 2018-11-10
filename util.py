from urllib.parse import urlparse
from forms import WordListForm
import re

url_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def process_text(text, url_check=False):
    words = (w.strip()
             for word in text.split('\n')
             for w in word.split(' ')
             if w not in ('', '\r', '\n'))

    if url_check:
        words = [url
                 for url in words
                 if url_regex.match(url)]

    return words


def add_text_to_file(text, file_, **kwargs):
    words = process_text(text, **kwargs)

    with open(file_, 'w') as f:
        f.close()

    with open(file_, 'a') as f:
        for word in words:
            f.write("%s\n" % word)

    return words


def get_text_from_file(file_):
    with open(file_) as f:
        return [line.strip() for line in f.readlines()]


def _construct_form(banned_words, white_list, blackList):
    form = WordListForm()

    longest_banned_word = max([len(word) for word in banned_words]) + 1
    longest_white_url = max([len(word) for word in banned_words]) + 1
    longest_black_url = max([len(word) for word in banned_words]) + 1

    columns = max(longest_banned_word, longest_white_url, longest_black_url)

    form.bannedWords.render_kw = {'rows': len(banned_words) + 1, 'cols': columns + 1}
    form.bannedWords.data = '\n'.join(banned_words)

    form.whiteList.render_kw = {'rows': len(white_list) + 1, 'cols': columns + 1}
    form.whiteList.data = '\n'.join([urlparse(url).geturl() for url in white_list])

    form.blackList.render_kw = {'rows': len(blackList) + 1, 'cols': columns + 1}
    form.blackList.data = '\n'.join([urlparse(url).geturl() for url in blackList])

    return form
