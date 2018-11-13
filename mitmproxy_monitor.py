from mitmproxy.http import HTTPFlow, HTTPResponse
from mitmproxy import ctx

from profanityfilter import ProfanityFilter
from constants import FILE_WEBSITE_VISITED, FILE_WHITELIST, FILE_BLACKLIST, FILE_PROFANITY_BLOCKLIST
from urllib.parse import urlparse
from analyze import analyze_page

import json


class Events:
    def request(self, flow: HTTPFlow):
        """The full HTTP request has been read."""
        client_ip = flow.client_conn.ip_address[0].split(':')[-1]
        url = urlparse(flow.request.url)

        base_url = "%s://%s" % (url.scheme, url.netloc)
        data = analyze_page(str(base_url))
        if data:
            score = {text.replace('\\', ''): score
                     for text, score in data
                     if text}

            existing_json = {}
            with open('files/words.json', 'r') as f:
                try:
                    existing_json = json.load(f)
                except ValueError:
                    existing_json = {}

            with open('files/words.json', 'w') as f:
                for text, val in score.items():
                    if text in existing_json:
                        existing_json[text] = (existing_json[text] + val) // 2
                    else:
                        existing_json[text] = val

                json.dump(existing_json, f)

        base_url = "%s://%s" % (url.scheme, url.netloc)

        json_data = None
        with open(FILE_WEBSITE_VISITED, "r") as f:
            json_data = json.load(f)

        if json_data is not None:
            with open(FILE_WEBSITE_VISITED, "w") as f:
                if client_ip not in json_data:
                    json_data[client_ip] = []

                if base_url not in json_data[client_ip]:
                    json_data[client_ip].append(base_url)

                json.dump(json_data, f)

        with open(FILE_WHITELIST) as f:
            white_list = [line.strip() for line in f.readlines()]
            if white_list:
                if base_url not in white_list:
                    flow.response = HTTPResponse.make(
                            200,
                            b"You are not permitted to view this website - %s" % bytes(flow.request.pretty_url, "utf8"),
                            {"Content-Type": "text/html"}
                    )

        with open(FILE_BLACKLIST) as f:
            if not white_list:
                black_list = [line.strip() for line in f.readlines()]
                if black_list:
                    if base_url in black_list:
                        flow.response = HTTPResponse.make(
                                200,
                                b"You are not permitted to view this website - %s" % bytes(flow.request.pretty_url,
                                                                                           "utf8"),
                                {"Content-Type": "text/html"}
                        )

    def response(self, flow: HTTPFlow):
        """The full HTTP response has been read."""
        data = ""
        try:
            data = flow.response.content.decode('utf8', errors='ignore')
        except UnicodeDecodeError as e:
            ctx.log.alert(str(e))

        with open(FILE_PROFANITY_BLOCKLIST) as f:
            profanity_filter_override = [line.strip()
                                         for line in f.readlines()]
            pf = ProfanityFilter(extra_censor_list=profanity_filter_override)
            flow.response.content = bytes(pf.censor(data), 'utf8')


addons = [
    Events()
]
