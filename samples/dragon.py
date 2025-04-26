from winding.parser import Lark_StandAlone
from winding.transformer import WindingTransformer
from winding.ast import Winding
from pprint import pprint


parser = Lark_StandAlone()
sample = """---
dragons: portrait-oriented
---
A book about dragons

--
front-cover: portrait-oriented
--
Dragons

@center: large, landscape-oriented
![Flying Wind Dragon](dragon.png)
"""

tree = parser.parse(sample)
ast = WindingTransformer().transform(tree)
pprint(ast, indent=2)


