import html.parser


def generate_html_tag(tag_name, attribute_list):
    html_attributes = ""
    for attribute in attribute_list:
        attribute_name, attribute_value = attribute
        html_attributes += f" {attribute_name}='{attribute_value}'"
    html_tag = f"<{tag_name}{html_attributes} />"
    return html_tag


class SSMLGenerator(html.parser.HTMLParser):

    def __init__(self):
        super().__init__()
        self.in_paragraph = False
        self.ssml = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.in_paragraph = True
        if tag.startswith('ssml:'):
            self.ssml += generate_html_tag(tag[5:], attrs)

    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_paragraph = False

    def handle_data(self, data):
        if self.in_paragraph:
            self.ssml += data.strip() + " "

    def generate(self):
        return '<speak>' + self.ssml + '</speak>'
