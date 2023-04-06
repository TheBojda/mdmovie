import html.parser


class GeneratorBase(html.parser.HTMLParser):

    def __init__(self):
        super().__init__()

    def generate(self):
        pass
