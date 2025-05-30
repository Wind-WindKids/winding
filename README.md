# Winding Python Module

[Wind for Kids](https://wind.kids) | [Wind for Developers](https://wind.dev) | [Winding Markdown Spec](https://winding.md) ([plain text](https://winding.md/winding.md)) | [GitHub](https://github.com/Wind-WindKids/winding)
<!-- | [Wind Language Foundation](https://wind-lang.org) -->

[Winding Markdown Specification](https://winding.md) ([plain text](https://winding.md/winding.md)) | [GitHub](https://github.com/Wind-WindKids/winding)

A Python implementation of Winding Markdown - a lightweight CommonMark extension for creating artifacts via concise prompts.

## Introduction to Evaluating Winding Expressions

Winding lets you write concise programs that can be "illuminated" into full implementations. Instead of verbose templates or complex configurations, you prompt (send messages) to agents:

```markdown
---
hello_world: file, py
---
Make it shine.

@style: pythonic, minimal
```

If you run this Winding Markdown, it will produce a Python file that prints "Hello, World!" in a minimalistic style. Like this:

```python
#!/usr/bin/env python3

def main():
    # Print a shining Hello, World! with ANSI sparkle
    print("\033[1;33m✨ Hello, World! ✨\033[0m")

if __name__ == "__main__":
    main()
```

You have just evaluated your first Winding expression! You sent a message to the 'hello_world' agent with arguments message ['file', 'py'], followed by a message containing a list of Windings:
* The Markdown text "Make it shine."
* A Winding that sends a message to the 'style' agent (in the space of 'hello_world') with arguments ['pythonic', 'minimal']

The hello_world agent, as a receiver, was newly invoked and decided what to do with these messages. It looked up its methods for handling `file` and `py` messages and responded appropriately.

> If you talk to Smalltalkers for a while, you will quickly notice that
> they generally do not use expressions like “call an operation” or “invoke
> a method”, but instead they will say “send a message”. This reflects the
> idea that objects are responsible for their own actions. You never tell an
> object what to do — instead, you politely ask it to do something by sending
> it a message. The object, not you, selects the appropriate method for
> responding to your message ... [Getting Started: Squeak by Example](https://squeak.org/documentation/)

With Winding, it is the same: you send messages to agents within the context of a space, and they decide how to produce artifacts.



## Features

- Provides `illuminate` that executes Winding Markdown files and produces artifacts.
- Defines EBNF grammar for the Winding Markdown, for use with vLLM, Lark etc.
- Defines a pure Python parser, based on the Lark standalone parser.
- Defines AST and WindingTransformer, to facilitate the parsing.

## Installation

You can install the Winding module from PyPI using pip:

```bash
pip install winding
```


## Usage

```markdown
---
winding: cli, tools
---
Winding Markdown CLI suite

@messages.vm:  
illuminate, wind, unwind, deluminate

@arguments:  
files, intent, pipes, include, exclude, context

@messages:  
fresh, freshen, draft, dry, wet, kiss, brush, lift, cool, heat, safe

@messages.dev:  
aloha, whisper, whine, lull, towel, wing, kite, kid, boy, girl, Wind, Sophie, please, help

@messages.experimental:  
venturi, whirl, whirling, whirlwind, reilluminate, rewind

@kid:  
I’m a kid, ELI5.

--
examples
--
aloha | illuminate "Hello World!"
```



## Development

You can find runnable examples in the `samples/` directory.

Here is a simple example of printing the grammar:

```python
>>> from winding import grammar
>>> print(grammar)

start: (winding | markdown)+

winding: meta_winding | space_winding | inline_winding
meta_winding: "---\n" receivers ":" arguments header_winding* "\n---\n" windings? 
space_winding: "--\n" receivers ":" arguments header_winding* "\n--\n" windings?
header_winding: "\n" receivers ":" arguments
inline_winding: "@" receivers ":" arguments "\n" markdown

windings: (inline_winding | markdown)+
markdown: (image | TEXT)+
image: "![" CAPTION? "]" "(" URI? ")"

receivers: IDENTIFIER ("," IDENTIFIER)*
arguments: (IDENTIFIER ("," IDENTIFIER)*)?


IDENTIFIER: /!?[A-Za-z0-9][ A-Za-z0-9_.-]*/
URI: /[^\)\n]+/
TEXT: /(?:(?!@\w+[A-Za-z0-9_.,-]*:|--|!\[).)*\n+/ 
CAPTION: /[^\]]+/
    
%ignore /[ \t]+/
%ignore "\r"  
```

## Example of parsing a Winding Markdown file

See `samples/dragon.py` for a complete example.

```python
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
```

This will output the following AST:
```python
Winding(receivers=['this'],
        arguments=[],
        windings=[ Winding(receivers=['dragons'],
                           arguments=['portrait-oriented'],
                           windings=[ Markdown(content='A book about dragons\n'
                                                       '\n')]),
                   Winding(receivers=['front-cover'],
                           arguments=['portrait-oriented'],
                           windings=[ Markdown(content='Dragons\n\n'),
                                      Winding(receivers=['center'],
                                              arguments=[ 'large',
                                                          'landscape-oriented'],
                                              windings=[ Markdown(content=Image(caption='Flying '
                                                                                        'Wind '
                                                                                        'Dragon',
                                                                                url='dragon.png')),
                                                         Markdown(content='\n')])])])
```



## Contributing
We welcome contributions to the Winding project! If you have suggestions, bug reports, or would like to contribute code, please open an issue or a pull request on our GitHub repository [winding](https://github.com/Wind-WindKids/winding).

## License

This project is licensed under the MIT License. See the LICENSE file for more details.