import os
import unittest
from winding import grammar
from pprint import pprint, pformat


class TestGrammar(unittest.TestCase):
    
    def test_grammar_structure(self):
        # Test if the grammar is loaded correctly
        self.assertIsNotNone(grammar)

    def test_lark_grammar_parsing(self):
        """Test that the Lark grammar can parse a sample input."""
        try:
            from lark import Lark
        except ImportError:
            self.skipTest("Lark is not installed")

        parser = Lark(grammar, start='start', parser='lalr')

        sample = """--
page: landscape-oriented
--
Text

@top: large, landscape-oriented
![caption](http://url)

@right: small, cursive, !black
Other Text

@background: colorful
An image of a cat. 

@cat.tail: 
Up with a curl

@cat.eyes: green, shining
"""

        try:
            tree = parser.parse(sample)
        except Exception as e:
            self.fail(f"Parsing failed: {e}")

    def test_transformer_ast(self):
        """Test that the transformer produces a Winding AST root."""
        try:
            from winding.parser import Lark_StandAlone
            from winding.transformer import WindingTransformer
            from winding.ast import Winding, Markdown, Image
        except ImportError:
            self.skipTest("Required modules are not installed")

        parser = Lark_StandAlone()
        sample = """===
book: portrait-oriented
filename: test.md
===
The book

--
front-cover: portrait-oriented
--
Text

@top: large, landscape-oriented
![caption](http://url)

![Another caption](another.png)

![Yet another]()

![](other.png)

![]()

--
spread: landscape-oriented
theme: colorful
--
Text

@right.bottom: small, cursive, !black

"""
        tree = parser.parse(sample)
        ast = WindingTransformer().transform(tree)
        self.assertIsInstance(ast, Winding)
        pprint(ast)

        expected = Winding(receivers=['this'],
        arguments=[],
        windings=[Winding(receivers=['book'],
                         arguments=['portrait-oriented'],
                         windings=[Winding(receivers=['filename'],
                                          arguments=['test.md'],
                                          windings=[]),
                                  Markdown(content='The book\n\n')]),
                 Winding(receivers=['front-cover'],
                         arguments=['portrait-oriented'],
                         windings=[Markdown(content='Text\n\n'),
                                  Winding(receivers=['top'],
                                          arguments=['large',
                                                      'landscape-oriented'],
                                          windings=[Markdown(content=Image(caption='caption',
                                                                          url='http://url')),
                                                   Markdown(content='\n\n'),
                                                   Markdown(content=Image(caption='Another '
                                                                                  'caption',
                                                                          url='another.png')),
                                                   Markdown(content='\n\n'),
                                                   Markdown(content=Image(caption='Yet '
                                                                                  'another',
                                                                          url='')),
                                                   Markdown(content='\n\n'),
                                                   Markdown(content=Image(caption='',
                                                                          url='other.png')),
                                                   Markdown(content='\n\n'),
                                                   Markdown(content=Image(caption='',
                                                                          url='')),
                                                   Markdown(content='\n\n')])]),
                 Winding(receivers=['spread'],
                         arguments=['landscape-oriented'],
                         windings=[Winding(receivers=['theme'],
                                          arguments=['colorful'],
                                          windings=[]),
                                  Markdown(content='Text\n\n'),
                                  Winding(receivers=['right.bottom'],
                                          arguments=['small',
                                                      'cursive',
                                                      '!black'],
                                          windings=[Markdown(content='\n')])])])
        
        # Compare the generated AST with the expected structure
        if ast != expected:
            # pretty print to a string and find first difference
            for a,e in zip(pformat(ast, indent=2).splitlines(),
                           pformat(expected, indent=2).splitlines()):
                if a != e:
                    print(f"Difference found:\n{a}\n{e}")
                    break
            

        self.assertEqual(ast, expected)

    

if __name__ == '__main__':
    unittest.main()