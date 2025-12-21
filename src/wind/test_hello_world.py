#!/usr/bin/env python3
"""Tests for hello_world.py"""

import unittest
from unittest.mock import patch
from io import StringIO
import hello_world


class TestHelloWorld(unittest.TestCase):
    
    def test_fancy_greeting_default(self):
        """Test greeting with default name"""
        result = hello_world.fancy_greeting()
        self.assertIn("Hello", result)
        self.assertIn("World", result)
        self.assertIn("Time:", result)
    
    @patch('sys.argv', ['hello_world.py', 'Alice'])
    def test_fancy_greeting_with_name(self):
        """Test greeting with custom name"""
        result = hello_world.fancy_greeting()
        self.assertIn("Hello", result)
        self.assertIn("Alice", result)
        self.assertIn("Time:", result)
    
    @patch('sys.argv', ['hello_world.py'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_execution(self, mock_stdout):
        """Test main execution"""
        hello_world.main()
        output = mock_stdout.getvalue()
        self.assertIn("Hello", output)


if __name__ == '__main__':
    unittest.main()
