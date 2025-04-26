from .parser import Transformer, v_args
from .ast import Image, Markdown, Winding

@v_args(inline=True)
class WindingTransformer(Transformer):
    def IDENTIFIER(self, tk):
        return tk.value

    def URI(self, tk):
        return tk.value

    def TEXT_LINE(self, tk):
        return tk.value.strip()

    def attributes(self, *ids):
        return list(ids)

    def image(self, caption, url):
        return Image(caption=caption, url=url)

    def markdown(self, *items):
        nodes = []
        for it in items:
            nodes.append(Markdown(content=it))
        return nodes if len(nodes) > 1 else nodes[0]

    def inline_winding(self, at, attrs, *content):
        body = []
        for c in content:
            if isinstance(c, list):
                body.extend(c)
            else:
                body.append(c)
        return Winding(at=at, attributes=attrs, content=body)

    def space_winding(self, at, attrs, *content):
        return self.inline_winding(at, attrs, *content)

    def start(self, *items):
        doc = Winding(at="document", attributes=[], content=list(items))
        return doc
