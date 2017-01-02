import scrapy
# from scrapy.http import HtmlResponse

import json
from build_object import build_object

with open('10698834') as f:
    body = f.read()

print(json.dumps(build_object(body), indent=4))
