import markdown


def parse_to_html(content: str):
    return markdown.markdown(content)
