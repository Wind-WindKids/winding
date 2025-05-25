# Winding Markdown (Draft v0.13)
[plain text version](https://winding.md/winding.md) | [pypi module](https://pypi.org/project/winding/) | [GitHub](https://github.com/Wind-WindKids/winding)

> A lightweight CommonMark extension for describing layouts, scenes, and images via concise prompts.

## Table of Contents
- [Introduction](#introduction)  
- [Syntax](#syntax)  
- [Formal Grammar](#formal-grammar)
- [Reference Examples](#reference-examples)
- [Philosophy](#philosophy)  

## Introduction

Winding Markdown lets you define websites, images, slides, agents, or 3D scenes using structured, minimal prompts. If you've ever struggled with an out-of-control image prompt, this is for you.

## Quick Start

To see it in action, here’s your first winding:

```markdown
--
my_first_winding: slide, square, jpg
--
Welcome to Winding Markdown  
_A markdown for illuminating documents_

@center: image, wide
A swirl of wind, a flowing text, forming a shape of a dragon.

@footer:
Learn more at  https://winding.md
```
![My First Winding](assets/my_first_winding.jpg)

Initially, with simple images and slides, you don't need specialized tooling. Provide a prompt like this: `Please, illuminate this markdown.` into [ChatGPT](https://chatgpt.com) or another capable generative AI. With larger projects, you can use projects, copilots and the `illuminate` command from the [Winding Python module](https://pypi.org/project/winding/).


## Key Benefits
- **Efficient**: Complex projects can be [completed in days instead of months](https://wind.kids)
- **Compatible**: Works with any Markdown processor and generative AI tools
- **Readable**: Plain-text format, easy to write even on a mobile

Winding Markdown is context-aware, allowing you to be *concise* in your descriptions. For example, you can create a logo that matches your first winding with just two lines:

```markdown
@winding.logo: square, abstract, png
A swirl of wind, a flowing text, a galaxy, forming a shape of a dragon.
```

![Winding Logo](assets/logos/winding.logo.abstract.png)

## Describing a Scene

Scenes can be described, with a level of detail that can rich a USD-like description, but without nesting and readable on a mobile device.

```markdown
--
laptops: image, file, landscape-orientation, png
--
Two laptops, and a phone in the grass. The screen of the phone is dark.

@laptops: modern
Lightly used

@left.screen: 
The dragon, alive, and has green eyes.

@right.screen:
VSCode
```

![Laptops](samples/gpt-image-1-laptops.jpeg)

Winding Markdown effectively decomposes the scene description, into a set of prompts or *messages* to the *agents* that are responsible for the layout, style and visualization of the objects in the scene.

Here's a more realistic example, with a more specific description:

![Wind on the Grass](samples/gpt-image-1-wind_on_the_grass.jpeg)

```markdown
--
wind_on_the_grass: image, landscape-orientation, png
style: nwind
--
Two laptops. Wind is lying on the grass, looking at the screen.left. Dappled sunlight through a high oak canopy flickers across his back and the keyboards. His tousled blond hair glows gold with soft iridescence, tiny freckles visible at his temples. A sleek smartphone rests nearby, its glass surface reflecting the green of the trees.

@laptop.left: matte-silver
A Kite logo to the left of the mouse pad.

@laptop.right: smaller, !logo, charcoal-gray

@screen.left:
running a robotics simulation in Omniverse / Isaac Sim.  

@simulation.subject: 
a quadruped metallic dragon in a test harness. Influence: robotic dog, Japanese motorcycle. Wings unfolded, aerodynamic plating, slightly smaller than a hang glider.

@dragon.eyes:
glow bright green — functional HCI, alert despite mechanical constraint.

@screen.right:
VSCode in dark mode, split view with terminals at the bottom, logs streaming and editor pane showing dense motion-control code.

@Wind:
boy, around 8 years old, tousled blond hair, bright blue eyes.

@Wind.pose:
He is lying on his stomach, propped up on his elbows, fingertips poised over the keyboard, slight tension in his wrists. Looking at the laptop, away from the camera, his face is not visible. 

@Wind,dragon: eye-contact

@Wind.clothes:
Teal short-sleeved shirt and charcoal-gray shorts.

@phone:
modern smartphone with a matte-black case, screen dark but glossy, edges catching sunlight.

@trees:
tall oak canopy overhead, leaves filtering light into soft, shifting patterns.

@grass:
lush carpet of individual blades, dew lightly beading near the laptops.
```

## Creating a Web Page

The same syntax can be used to create a web page, a page of book, or a slide. The only difference is the message to the receiving agent:

```markdown
--
my_first_winding_web_page: jekyll, liquid, file, md
--
Welcome to Winding Markdown  
_A markdown for illuminating documents_

@center: image, square, png, cutout
![A swirl of wind, a flowing text, a galaxy, forming a shape of a dragon.](assets/logos/winding_logo.png)

@footer:
Learn more at  https://winding.md
```

![My First Winding Web Page](my_first_winding_web_page/)

## Creating a Winding from a Winding
By illuminating a winding that outputs a winding, you can create a new winding. This is useful for creating a new winding based on the current context:

```markdown
--
spelling_errors: winding, file, md
--
A winding that contains spelling errors, from the current context, including misspellings inside images.
```

or even creating an agent that can modify itself, if needed:

```markdown
---
spelling_supervisor: winding, file, md
---
A spelling supervisor is a winding that ensures that the spelling is correct in the current context.

--
spelling_errors: winding, file, md
--
A winding that contains spelling errors, from the current context, including misspellings inside images.

--
flagged_windings: winding, file, md
--
A winding that contains flagged winding names with spelling errors.
```


## Core Concepts

Winding Markdown is built on three core concepts:

### 1. **Agents**
Everything in a winding is an agent that can receive messages. An agent could be:
- A layout element (`@center`, `@footer`)
- An object in a scene (`@laptop`, `@dragon`)
- A style, trait or the context (`@style`, `@wide`, `@this`)

### 2. **Messages**
Every line in a winding is a message, prompting some agent:
```markdown
@dragon: green, alive
The dragon soars through clouds.
```
Here, `dragon` receives three messages:
- `green` (trait)
- `alive` (trait)  
- `The dragon soars through clouds.` (description)

### 3. **Spaces**
Spaces are bounded contexts. They determine:
- Which agents are nearby
- How messages propagate
- How much influence context has
- How messages are interpreted

## Syntax Reference

### Quick Reference Table

| Syntax | Purpose | Example |
|---|---|---|
| `@receivers:` | Send message to agent | `@header: bold,centered` |
| `identifier.sub` | Sub-agent | `@laptop.screen: bright` |
| `!identifier` | Negate/remove trait | `@screen: !dark,bright` |
| `:` | Lightweight boundary | `@section:` |
| `--` | Medium boundary | `-- scene: outdoor --` |
| `---` | Strong boundary | `--- document: report ---` |
| `,` | Multiple traits | `@text: bold,italic,large` |

### Agent Addressing

```markdown
@agent:              # Direct message to agent
@agent.sub:          # Message to sub-agent
@agent1, agent2:     # Same message to multiple agents
@*:                  # Message to all agents in the current space
```

### Argument Messages

```markdown
@agent: argument1, argument2, !argument3
```
- For example, `@text: bold, illuminated`
- Or to subtract traits, `@text: !italic`

## Boundaries and Context

Boundaries control how context flows between spaces. Think of them as walls with different permeability:

```markdown
: (colon)      → Lightweight boundary (highly permeable)
-- (dash)      → Medium boundary (permeable)  
--- (triple)   → Strong boundary (less permeable)
```

Visual mnemonic: Rotate `:` ninety degrees → `..` → `--` → `---`

### Permeability in Practice

When illuminating a winding, context from surrounding spaces influences the output. The boundary strength determines this influence:

#### Strong Boundary (File, Meta Winding)
```markdown
---
report: document, formal, pdf
---
Quarterly Financial Report
```
- Used at file beginning
- Establishes document-level context
- Less influenced by external context

#### Medium Boundary (Section, Space Winding)
```markdown
--
chart: visualization, data
--
Revenue by quarter...
```
- Creates distinct sections
- Moderate context flow

#### Light Boundary (Local, Inline Winding)
```markdown
@note: aside, italic
Market conditions were favorable.
```
- Minimal separation
- Maximum context influence
- Quick annotations


## Syntax

### `@receivers:`
Used to **send a message** in the winding to agents identified by the `@identifier,[identifier]:` list.

A colon `:` in it is a boundary, it starts a new **space** for the text.  A sign `@` is a decorator, it is not part of the name of the agent, it is used to address the agents.
Multiple identifiers can be used in a single line, preceded by `@`, and separated by commas.

### `identifier.other_identifier`
Dot notation for precision, used for **targeting** addressing of sub-agents.

### `!identifier`
Used to **invert** the identifier.

In a winding everything is a prompt or a message, and everyhing is an agent. The interpretations of the messages are up to the agents...

### `: layout, style, !something`
Used for example, for **layout, style, or presentation metadata**. Think Smalltalk arguments or CSS-like tags. Or talking to that agent to inherit the trait.

### `---` or `--` or `:`
A triple-dash, double-dash or column are boundaries, they start a new **space** for the text.

### `Free Markdown Prompting`
Used to talk to that agent to prompt it. The agent is free to interpret the message as it sees fit. The content can be a Markdown to render, an action to perform, a style to apply, or anything else. A table, mermade diagram or a code block can be used. 



## Examples

### Typesetting, Spread, Page, Book

An example to illustrate Winding Markdown syntax.  

```markdown
@intro: spread, text  
A spread is a double page, it is usually landscape oriented and this text is a message to the `spread` agent, that by default will print the text.

@page:
A page is a single page, it is usually portrait oriented and this text is a message to the `page` agent, that by default will print the text.
```

### Metadata
```markdown
---
about_metadata: book, portrait-orientation
title: Metadata in Winding Markdown
---
This block is usually present in the beginning of the Winding Markdown file. In this particular case, it is a message to the `about_metadata` agent, that it is a book, and it is portrait oriented. The title is a message to the `title` agent (or more precisely, the `title` agent in the `about_metadata` space, which resolves to `about_metadata.title`), that it is a book about metadata in Winding Markdown.  
```

### Object Annotation
```markdown
@laptop:
Modern laptop, lightly used

the description of the laptop is a message to the `laptop` agent, that is in turn a message to *this*, which in this case is the winding.

@screen: 
A dragon, soaring.

@laptop.left.lid:
Kite logo

@dragon.eyes: alive, green
```

Annotation is:
- Context-sensitive — `@screen` in a `@laptop` space assumes containment.
- Objects can be nested mentally, but not structurally.
- Repeated tags are allowed. Order implies visual/topical grouping.


### `: message`
Used for example, for **layout, style, or presentation metadata**. Think CSS-like tags. Or talking to that agent to inherit the trait.

```markdown
@right: page, cutout, square, medium
```

### Images

```markdown
@wind_on_the_grass: image, file, square, png
A summary of the scene. Defaults to camera-level / observer view.
Use `@object` sections to describe focused parts of the image.
```

Alternative syntax, where the winding is defined as a separate block (spatial winding):

```markdown
--
wind_on_the_grass: image, file, square, png
--
A one-paragraph summary of the scene. Defaults to camera-level / observer view.
```

Note: it is allowed to use `wind_on_the_grass.png`, which would then implicitly instantiate `wind_on_the_grass`, by sending a message to its .png agent, but this is not the recommended syntax. The default for the images is currently `png`, to override it, you can send a message to the `image`, subtracting the current default and mixing in the new one:

```markdown
@image: !png, jpeg
```

or include it in the original winding.


## Formal Grammar
### EBNF Grammar (Lark)

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

### AST
```python
from dataclasses import dataclass, field
from typing import List, Union

@dataclass
class Image:
    caption: str = field(metadata={"description": "Image caption."})
    url:     str = field(metadata={"description": "Image URL."})

@dataclass
class Markdown:
    content: Union[str, 'Markdown', Image] = field(
        metadata={"description": "Plain text, nested Markdown, or Image node."}
    )

@dataclass
class Winding:
    receivers: List[str] = field(
        default_factory=lambda: ["this"],
        metadata={"description": "The @at receivers list, identifies recipient agents."}
    )
    arguments: List[str] = field(
        default_factory=list,
        metadata={"description": "Arguments: messages like size, orientation, !negation."}
    )
    windings:    List[Union[Markdown, 'Winding']] = field(
        default_factory=list,
        metadata={"description": "Windings: messages with free text or windings."}
    )
```

### Example
```markdown
---
dragon.portrait: image, character_art, jpg, wide
quality: high
---
Wise eyes.
```

turns into:  

```python
Winding(receivers=['this'], arguments=[], windings=[
    Winding(receivers=['dragon.portrait'],
            arguments=['image', 'character_art', 'jpg', 'wide'],
            windings=[
                Winding(receivers=['quality'], arguments=['high']),                                        
                Markdown(content='Wise eyes.\n')
                ])])
```


## Philosophy
- No brackets, easy to write by hand, even on a mobile device.
- No indentation rules, no nesting.
- Everything is a message and an agent in a space.
- Compatible with existing Markdown parsers.

Winding Markdown was designed specifically to describe **sequences of scenes**, **agents**, **messages** and **interactions**. We call it interchangebly **Winding Markdown** and `winding.md`. It makes it easier to **illuminate**, to search for a scene that would fit the story, to deal with retroactivity when writing a story, and to create **stable points** and consistent sequences of scenes. 

We call the process of writing in it **winding** and a resulting document a **winding**. It combines storytelling and typesetting. It allows both to write a story, page by page, and leave precise layout messages for the scenes, text, image, and transparent regions. It strikes a balance between plain-text readability and structured design. 

We call a process of searching for a stable point in a winding **illuminating**. It combines typesetting, illustration, and storytelling.


### Spatial Model: Agents and Spaces

Note a **shift** from namespace thinking to **message passing**, and it changes how we mentally model `.winding.md`.

This is a **declarative message system** where:
- Every `@agent:` is a message
- The receiver is contextually defined by the **current space**
- Values are **traits, roles, transformations, or definitions**
- Identity is **relational, not hierarchical**


### Space & Addressing

Every winding (book, page, spread, image...) **defines a space**.

Within a space:
- `@right:` means “send message to `right` agent in this space”
- `@screen.left:` means “send message to agent `screen.left` in this space”
- `@wind.hair:` means “send message to `hair` inside `wind` in this space”

No need to treat these like nested paths (`spread.screen.left`) — it’s more like **contextual dispatch**.

---

### Message Semantics

All `@agent` lines are **sending messages** to an **agent** or *prompting* it.

#### Single role/trait:

```markdown
@right: page
```

→ tells `right` to adopt the trait `page`, to become a `page`.

#### Multiple roles:
```markdown
@right: page, text, centered
```

→ sends 3 messages: “you are a `page`, you are `text`, and you are `centered`”

#### Property setting:
```markdown
@dragon.eyes: green
Alive and functional - HCI.
```

→ sends 2 messages: “you are a `green`” and “you are `Alive and functional - HCI.`” 


### Image Block Revisited, as an Agent
```markdown
@image: wind-on-the-grass.png, cutout, square
I'm just testing, sorry.
This is not defining a new image. It’s sending a message to image, saying:

"Become wind-on-the-grass.png, and take on the traits cutout, square."
Everything that follows in the current space is assumed to talk to that now-transformed image — unless another agent is addressed.

You're speaking to something, not defining it. But you are using true names.
```

## Reference Examples
### Smalltalk

[A comic strip to illuminate the process of winding and illuminating.](reference/smalltalk/)

### This

```markdown
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
Flat doesn’t mean shallow.  
Let things breathe.  
Negative space is part of the story.
```

![The Zen of Winding](assets/chagpt-gpt4o-apr-16-2025.zen.jpg)