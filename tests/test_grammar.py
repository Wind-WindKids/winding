import os
import unittest
from winding import grammar

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
            from winding.ast import Winding
        except ImportError:
            self.skipTest("Required modules are not installed")

        parser = Lark_StandAlone()
        sample = """--
front-cover: portrait-oriented
--
Text

@top: large, landscape-oriented
![caption](http://url)
"""
        tree = parser.parse(sample)
        ast = WindingTransformer().transform(tree)
        self.assertIsInstance(ast, Winding)
        print(ast)

if __name__ == '__main__':
    unittest.main()