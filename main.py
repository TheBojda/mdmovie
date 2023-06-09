import re

import markdown
import html.parser

from generators.SSMLGenerator import SSMLGenerator
from generators.SubtitleGenerator import SubtitleGenerator
from generators.VideoGenerator import VideoGenerator


def generate_html_tag(tag_name, attribute_list):
    html_attributes = ""
    for attribute in attribute_list:
        attribute_name, attribute_value = attribute
        html_attributes += f" {attribute_name}='{attribute_value}'"
    html_tag = f"<{tag_name}{html_attributes} />"
    return html_tag


class StorybookHTMLParser(html.parser.HTMLParser):

    def __init__(self):
        super().__init__()
        self.in_paragraph = False
        self.ssml = ''

    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag, attrs)
        if tag == 'p':
            self.in_paragraph = True
        if tag.startswith('ssml:'):
            self.ssml += generate_html_tag(tag[5:], attrs)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)
        if tag == 'p':
            self.in_paragraph = False

    def handle_data(self, data):
        print("Encountered some data  :", data)
        if self.in_paragraph:
            self.ssml += data + " "

    def get_ssml(self):
        return '<speak>' + self.ssml + '</speak>'


if __name__ == '__main__':
    with open('examples/the-first-moment-of-singularity/storybook.md', 'r') as f:
        storybook = f.read()

    md = markdown.Markdown(extensions=['markdown.extensions.attr_list', 'meta'])
    html = md.convert(storybook)
    html = re.sub('\n\s*', '', html)

    # parser = StorybookHTMLParser()
    # parser.feed(html)
    # print(parser.get_ssml())

    # generator = SSMLGenerator()
    # generator.feed(html)
    # print(generator.generate())

    # generator = VideoGenerator('examples/the-first-moment-of-singularity')
    # generator.feed(html)
    # generator.generate("test.mp4")

    generator = SubtitleGenerator()
    generator.generate('examples/the-first-moment-of-singularity/voice/a7b46f40-b767-4734-bccb-5f629e296ee0.marks', 'examples/the-first-moment-of-singularity/voice/a7b46f40-b767-4734-bccb-5f629e296ee0.sub')