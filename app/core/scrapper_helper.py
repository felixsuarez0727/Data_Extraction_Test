from urllib.parse import urljoin

import re


def transform_anchor(url, anchor):
    if "page" in url:
        url = re.sub(r"(\?page=\d+)", "", url)

    if "category" in url and "page" in anchor:
        return f"{url}{anchor.replace('/products', '')}"
    else:
        return urljoin(url, anchor)
