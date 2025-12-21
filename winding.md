---
winding: spec, markdown, v0.21
---
[plain text](https://winding.md/winding.md) | [pypi](https://pypi.org/project/winding/) | [Wind for Developers](https://wind.dev) | [Wind for Kids](https://wind.kids) | [GitHub](https://github.com/Wind-WindKids/winding)

A CommonMark extension for creating artifacts via concise prompts.

--
quick_start
--
```markdown
--
my_first_winding: slide, square, jpg
--
Welcome to Winding Markdown  
_A markdown for illuminating documents_

@center: image, wide
A swirl of wind, a flowing text, forming a shape of a dragon.

@footer:
Learn more at https://winding.md
```

@artifacting:
This is how you'd turn your winding into an artifact:

```bash
artifact my_first_winding
```

Which may look like this:
![My First Winding](assets/my_first_winding.jpg)

--
core_concepts
--

@agents:
Everything is an agent that receives messages:
- Layout elements (`@center`, `@footer`)
- Objects in a scene (`@laptop`, `@dragon`)
- Styles or traits (`@style`, `@wide`)

@messages:
Every line is a message to an agent:
```markdown
@dragon: green, alive
The dragon soars through clouds.
```
Here `dragon` receives: `green`, `alive`, and the description text.

@spaces:
Spaces are bounded contexts. Boundary strength controls context flow:
- `:` — Light (inline)
- `--` — Medium (section)
- `---` — Strong (file/document)

--
syntax
--

| Syntax | Purpose | Example |
|---|---|---|
| `@receivers:` | Send message to agent | `@header: bold, centered` |
| `identifier.sub` | Sub-agent | `@laptop.screen: bright` |
| `!identifier` | Negate/remove trait | `@screen: !dark, bright` |
| `:` | Light boundary | `@section:` |
| `--` | Medium boundary | `-- scene: outdoor --` |
| `---` | Strong boundary | `--- document: report ---` |
| `,` | Multiple traits | `@text: bold, italic, large` |

@addressing:
```markdown
@agent:              # Direct message
@agent.sub:          # Sub-agent
@agent1, agent2:     # Multiple agents
@*:                  # All agents in space
```

@arguments:
```markdown
@agent: arg1, arg2, !arg3
```

--
examples
--

```markdown
@winding.logo: square, abstract, png
A swirl of wind, a flowing text, a galaxy, forming a shape of a dragon.
```

```markdown
--
my_page: jekyll, liquid, file, md
--
Welcome to Winding Markdown

@center: image, square, png
![Dragon logo](assets/logo.png)

@footer:
Learn more at https://winding.md
```

```markdown
---
my_book: book, portrait-orientation, file, pdf
---

--
cover
--
Book Title

--
intro: page
--
Introduction text.
```

```markdown
--
laptops: image, landscape-orientation, png
--
Two laptops in the grass.

@left.screen: 
A dragon with green eyes.

@right.screen:
VSCode
```

```markdown
---
hello_world: file, py
---
Make it shine.

@style: pythonic, minimal
```

--
grammar: ebnf, lark
--
```ebnf
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

--
ast: python
--
```python
@dataclass
class Image:
    caption: str
    url: str

@dataclass
class Markdown:
    content: Union[str, 'Markdown', Image]

@dataclass
class Winding:
    receivers: List[str] = field(default_factory=lambda: ["this"])
    arguments: List[str] = field(default_factory=list)
    windings: List[Union[Markdown, 'Winding']] = field(default_factory=list)
```

@example:
```markdown
---
dragon.portrait: image, jpg, wide
quality: high
---
Wise eyes.
```

Parses to:
```python
Winding(receivers=['this'], arguments=[], windings=[
    Winding(receivers=['dragon.portrait'],
            arguments=['image', 'jpg', 'wide'],
            windings=[
                Winding(receivers=['quality'], arguments=['high']),                                        
                Markdown(content='Wise eyes.\n')
            ])])
```

--
philosophy
--
- No brackets, easy to write on mobile
- No indentation rules, no nesting
- Compatible with existing Markdown
- Spatial thinking over hierarchical
- Intent-oriented: describe *what*, not *how*

--
this : this
--

The Zen of Winding
===

Winding is the source of truth.  
Story, structure, image, and layout  
all emerge from it—and return to it.

Agents speak for themselves.  
You are always in a space.

True names have power.  
Everything is a message.  
Even a page is listening.

Clarity matters more than ceremony.  
Flat doesn't mean shallow.  
Let things breathe.  
Negative space is part of the story.
