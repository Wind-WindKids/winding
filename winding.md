# Winding Markdown (Draft v0.10)
[plain text version](https://winding.md/winding.md)

> A lightweight CommonMark extension for describing layouts, scenes, and images via concise prompts.

## Table of Contents
- [Introduction](#introduction)  
- [Syntax](#syntax)  
- [Syntax Examples](#syntax-examples)  
- [Formal Grammar](#formal-grammar)
- [Philosophy](#philosophy)  

## Introduction

Winding Markdown lets you define slides, scenes , or (https://wind.kids)[complete picture books] using structured, minimal prompts—no long prose required. If you’ve ever struggled with an out of control scene description, this is for you.

To see it in action, here’s a slide example:

```markdown
--
gpt-image-1-winding_markdown: slide, square, jpeg
--
Winding Markdown  
_A markdown for illuminating documents_

@center: image, landscape-orientation
Agents, messages, and layout blocks orbiting a markdown core.

@footer.right:
[https://winding.md](https://winding.md)
```

![Winding Markdown](assets/gpt-image-1-winding_markdown.jpeg)


Or a scene, described in a USD-like way, with a hierarchical structure:

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

![Laptops](https://winding.md/samples/gpt-image-1-laptops.jpeg)

Winding Markdown effectively decomposes the scene description, into a set of messages to the objects in the scene. These messages are the *prompts* to the *agents* that determine the layout, style and visualization for these objects.


A more realistic example, with a complex scene:

![Wind on the Grass](https://winding.md/samples/gpt-image-1-wind_on_the_grass.jpeg)

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

@Wind.clothes:
Teal short-sleeved shirt and charcoal-gray shorts.

@phone:
modern smartphone with a matte-black case, screen dark but glossy, edges catching sunlight.

@trees:
tall oak canopy overhead, leaves filtering light into soft, shifting patterns.

@grass:
lush carpet of individual blades, dew lightly beading near the laptops.
```


## Syntax

### `@identifier:`
Used to **send a message** in the winding to an agent identified by the `@identifier`.

A colon `:` in it is a boundary, it starts a new **space** for the text.  A sign `@` is a decorator, it is not part of the name of the agent, it is used to address the agent.
Multiple identifiers can be used in a single line, preceded by `@`, and separated by spaces or commas.

### `identifiers`, `identifier.other_identifier`
Are used for targeted prompting, this includes free text. Dot notation for precision, used for **targeting** addressing of sub-agents.

### `!identifier`
Used to **invert** the identifier.

In a winding everything is a prompt or a message, and everyhing is an agent. The interpretations of the messages are up to the agents...

### `: layout, style, !something`
Used for example, for **layout, style, or presentation metadata**. Think CSS-like tags. Or talking to that agent to inherit the trait.

### `--` or `:`
A double-dash or column are boundaries, they starts a new **space** for the text.

### `: `
### `Free Markdown Prompting`
Used to talking to that agent to prompt it. The agent is free to interpret the message as it sees fit. The content  can be a Markdown to render, an action to perform, a style to apply, or anything else. A table, mermade diagram or a code block can be used. 



## Syntax Examples

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

#### Image Example - Complex Scene



## Formal Grammar
Formal EBNF Grammar (Lark)

```ebnf
start: (winding | markdown)+

winding: meta_winding | space_winding | inline_winding
meta_winding: "---\n" IDENTIFIER ":" attributes header_winding* "\n---\n" content? 
space_winding: "--\n" IDENTIFIER ":" attributes header_winding* "\n--\n" content?
header_winding: "\n" IDENTIFIER ":" attributes
inline_winding: "@" IDENTIFIER ":" attributes "\n" markdown

content: (inline_winding | markdown)+

markdown: (image | TEXT)+

attributes: (IDENTIFIER ("," IDENTIFIER)*)?

image: "![" CAPTION? "]" "(" URI? ")"

IDENTIFIER: /!?[A-Za-z0-9][ A-Za-z0-9_.-]*/
URI: /[^\)\n]+/
TEXT: /(?:(?!@\w+:|--|!\[).)*\n+/ 
CAPTION: /[^\]]+/
    
%ignore /[ \t]+/
%ignore "\r"  
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


### Smalltalk

TODO: turn this into comic strip

It's kind of like if USD, CSS, Smalltalk, Markdown and Python got together on a windy day, and reminiscing GML had taught a trick or two to a new AI kid on the block. 

And then, it is kind of like if Feynman, as if he was there all along, explained state spaces, interactions, retroactivity and stable points to the AI kid really clearly. That when illuminating, messages are like light going over all paths and bouncing off the spatial boundaries, and attenuating. And then they went to fly their dragons, and when they were back, the kid was like, "I get it now! It's like when I fly a dragon, I need to think of all the paths other dragons can take, and how they interact with the wind and the terrain, the clouds and the sun. And dance with them. It's like a dance of information!" And Feynman smiled, knowing that the kid had totally grasped it.

```markdown
--- 
smalltalk: comic, portrait-orientation
---
A comic strip to illuminate retroactive interactions when an author winds a story and changes something in the middle of a text.

@style: nwind, illuminating, hand-drawn, sketchy

--
characters: recognizable, gentle, personified
--
Based on most recognizable photos from Wikipedia main pages. Characters wear their usual clothes.

@Markdown: character, image, anchor  
Based on ![Aaron Swartz Photo](images/anchors/photos/aaron_swartz.jpg)

@CSS: character, image, anchor  
Based on ![Håkon Wium Lie Photo](images/anchors/photos/hakon_wium_lie.jpg)

@USD: character, image, anchor  
Based on ![Steve Jobs Photo](images/anchors/photos/steve_jobs.jpg)

@USD.explanation: !visible  
The Universal Scene Description (USD) was first used internally by Pixar in the film Brave (2012) as part of their Presto system; that movie was “dedicated with love and gratitude to Steve Jobs.”

@Python: character, image, anchor  
Based on ![Guido van Rossum Photo](images/anchors/photos/guido_van_rossum.jpg)

@Smalltalk: character, image, anchor  
Based on ![Alan Kay Photo](images/anchors/photos/alan_kay.jpg)

@Wind: character, image, anchor  
Based on ![Wind Photo](images/anchors/photos/wind_kid.jpg)

--
opening: panel, wide, large
--
Markdown, CSS, USD, Smalltalk, Python and Wind sit together on a grassy hillside, chatting. GML stands nearby, looking at the ridge.

@background: early-morning mist, soft sunlight on grass, a few dragons flying, distant paraglider silhouettes, low to the ground.

--
usd_talking: panel, square
--
USD leans forward, eyes tracing a blue dragon skimming gravel below.

@bubble: text, small, italic  
"Look at that blue dragon—she's catching lift right off the gravel streaks."

@detail:  
Dragon is quite low, barely clearing the hillside tree line. The gravel patch is a mix of light and dark, with some patches glistening in the sunlight.

--
python_reply: panel, wide
--
Python nods thoughtfully, adjusting his scripting gloves.

@bubble:
"Yeah, I see it. She's timing her turns perfectly. I'm not sure I could do that. I'd probably end up in a tree."

--
smalltalk_laughs: panel, square
--
Smalltalk laughs, coffee cup in hand, turning to GML.

@bubble: 
"Remember that time?"

@cup: brown, green, paper
A coffee cup with a kite logo and a travel lid.

--
smalltalk_anecdote: panel, wide
--
@bubble:
"One misplaced bracket and the whole code tree spiraled. I thought I was going to end up in that tree too!"

@background:
A misty cloud over the ridge looks suspiciously like a bracket.


--
markdown_reflection: panel, tall
--
Markdown gazes toward the ridge, at the whispy clouds suddenly appearing and looking suspiciously like brackets.

@markdown.thoughts: cloud, text, small, handwritten  
"Brackets always sneak back in. And in the retrospective, they are nearly always a mistake."

--
smalltalk_points: panel, tall
--
Smalltalk points out the ridge, under the misty clouds that look a bit less like brackets now. The early morning thermal starting to lift gently from the hillside, implying conditions may improve soon.

@bubble:
"Look at those streaks of wind on the grass, on the hillside."

--
wind_impatient: panel, square
--
Wind, clearly anxious to launch, listens impatiently as the adults discuss conditions calmly.

@bubble:
"Yeah, should we launch now? I think I could have caught that one."

@GML.bubble:
"Be patient, Wind. It is still too light. See this green dragon?"

--
green_dragon: panel, wide, large
--
A striking, iridescent green dragon swoops dramatically toward the hilltop, startling the group.

@dragon:
A metallic green dragon, iridescent, with a hint of blue and gold in the sunlight. It's a bit smaller than a hang glider, with a sleek, aerodynamic design. It looks a bit too precise, to be biological, but it is not a drone either. It is a dragon, and it is alive.

--
green_dragon_arrival: panel, square
--
The dragon lands somewhat abruptly, scattering dust and causing slight disarray among gear and group members.

--
green_dragon_folding_wings: panel, square
--
An emerald-green dragon begins folding its wings.

--
dragon_transformation_starts: panel, square
--
An emerald-green dragon begins folding its wings, wingtips contract as the wings pixelate, fragmenting into quads and pixels.

@transformation: detail, !visible, !text
Human/dragon transforms without menace, casual. Like in Airbender or Luca, but with pixelation. Obviously some advanced nanotech at work there, handling a quick redistribution of matter from an object the size of the hang glider to a human size. But the magic of it is efficient, not flashy and it fades into the background, like good technology should.

--
dragon_transformation_head: panel, square
--
Pixelation and quades cascade from the dragon’s head; a faint human silhouette (Feynman) emerges.

--
dragon_transformation_body: panel, square
--
The body pixelates, flesh and fabric take shape mid-transition. A quad mesh forms the outline of a face.

@transformation: detail, !visible, !text  
Nanotech weaves pixelated iridescent dragon body into skin and clothes seamlessly.

--
dragon_transformation_face: panel, square
--
Feynman’s face emerges from the pixelated quad mesh, slightly angled and amused.

--
feynman_arrival: panel, wide, large
--
Richard Feynman stands where the dragon once was, dusting pixels off himself casually. The group waves, warmly, but nonchalantly.


--
weather_talk: panel, wide
--
Feynman brushes pixel-dust off his jacket, smiling at the group.

@bubble:  
“Very light lift, a lot of flapping. I've barely made it to top-land.”

--
wind_frustration: panel, square
--
Wind, looking a bit frustrated, glances at the GML.
@bubble:
"More waiting?"

--
feynman_instruction: panel, wide
--
@bubble:
"Wind, pretend you are airborne, scratching the rocks, just above that blue dragon.”

--
wind_looks: panel, square
--
Wind looks at the blue dragon, who is now a lot lower.

--
feynman_looks: panel, square
--
Feynman looks at the blue dragon, as well.
@bubble:
"And retrace how you got there."
```


OUTLINE:
They launch then, each turning into a dragon as they run and launch from the hill, and soar, forming a small gaggle in flight.

A couple of panels there, where they just fly.

They land down the hill, at the landing zone, a panel of the group together, some in dragon form, some turning human.

A panel where the Wind, saying to Feynman, something like:  "You know, I think I get it, what you've been explaining. Information dance when winding and illuminating a story is a little bit like our dragon dance, when we fly together."



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