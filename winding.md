## Winding Markdown (Draft v0.7)

This spec describes Winding Markdown, a lightweight extension of Markdown, designed to describe scenes, layouts or books in an structured way. For example, a scene, described in an Markdown, could be:

```markdown
Two laptops, a dragon on the left screen, some code on the right screen, and a phone nearby. The dragon is alive, and has green eyes. The laptop is modern, lightly used. The screen of the phone is dark.
```

In Winding Markdown, this would be described as:

```markdown
Two laptops, and a phone nearby. The screen of the phone is dark.

@laptop: modern
Lightly used

@left.screen: 
The dragon, alive, and has green eyes.

@right.screen:
Some code.
```

This effectively decomposes the scene into a set of messages, that are sent to the agents. The agents are the objects in the scene, and the messages are the *prompts* to those objects.

## Winding Markdown Syntax

### `--`

A double-dash is a permeable boundary, it starts a new **space** for the text.

### `@identifier:`
Used to **send a message** in the winding to an agent identified by the `@identifier`.

A colon `:` in it is also a permeable boundary, it starts a new **space** for the text and is equivalent `--`.
An at sign `@` is a decorator, it is not part of the name of the agent, it is used to address the agent.
Multiple identifiers can be used in a single line, preceded by `@`, and separated by spaces or commas.

### `identifiers`
Are used for targeted addressing. They are **true names**. 

### `identifier.other_identifier`
Dot notation for precision, used for **targeting** addressing of sub-agents.

### `!identifier`
Used to **invert** the **message** of the identifier.

In a winding everything is a message, and every message is an agent. The interpretations of the messages are up to the agent...

#### `: layout, style, !something`
Used for example, for **layout, style, or presentation metadata**. Think CSS-like tags. Or talking to that agent to inherit the trait.

#### `: `
#### `Free Text Prompting`
Used to talking to that agent to prompt it. It can be a text to render, an action to perform, a style to apply, or anything else. The agent is free to interpret the message as it sees fit.


### Grammar

[Winding Markdown Grammar](https://winding.md/grammar)

### Examples

#### Typesetting, Spread, Page, Book

An example to illustrate Winding Markdown syntax.  

```markdown
@intro: spread, text  
A spread is a double page, it is usually landscape oriented and this text is a message to the `spread` agent, that by default will print the text.

@page:
A page is a single page, it is usually portrait oriented and this text is a message to the `page` agent, that by default will print the text.
```

#### Metadata
```
---
about_metadata: book, portrait
title: Metadata in Winding Markdown
---
This block is usually present in the beginning of the Winding Markdown file. In this particular case, it is a message to the `about_metadata` agent, that it is a book, and it is portrait oriented. The title is a message to the `title` agent (or more precisely, the `title` agent in the `about_metadata` space, which resolves to `about_metadata.title`), that it is a book about metadata in Winding Markdown.
```

@spread: landscape
Effectively sets the orientation of the current spread to landscape.

#### Object Annotation
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


#### `: message`
Used for example, for **layout, style, or presentation metadata**. Think CSS-like tags. Or talking to that agent to inherit the trait.

```
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

Note: it is allowed to use `wind_on_the_grass.png`, which would then implicitely define
`wind_on_the_grass`, by sending a message to its .png agent, but this in not the recommended syntax. The default for the images is currently `png`, to override it, you can send a massage to the `image`, substracting the current default and mixing in the new one:

```markdown
@image: !png, jpeg
```

or include it in the original winding.


### Up-to-date Spec
You can find the up-to-date spec at [winding.md](https://winding.md).


### Image Example

[Wind on the Grass](https://winding.md/samples/gpt-image-1-wind_on_the_grass.jpeg

```markdown
--
wind_on_the_grass: image, landscape-orientation, png
style: nwind
--
Two laptops. Wind is lying on the grass, completely absorbed by the code on screen.right. Dappled sunlight through a high oak canopy flickers across his back and the keyboards. His tousled blond hair glows gold with soft iridescence, tiny freckles visible at his temples. A sleek smartphone rests nearby, its glass surface reflecting the green of the trees.

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

@clothing:
Teal short-sleeved shirt and charcoal-gray shorts.

@phone:
modern smartphone with a matte-black case, screen dark but glossy, edges catching sunlight.

@trees:
tall oak canopy overhead, leaves filtering light into soft, shifting patterns.

@grass:
lush carpet of individual blades, dew lightly beading near the laptops.

@Wind.focus:
complete, absorbed by the code on screen.right, everything else is background blur.
```

# Philosophy
- No brackets, easy to write by hand, even on a mobile device.
- No indentation rules, no nesting.
- Everything is a message and an agent in a space.
- Compatible with existing Markdown parsers.

Winding Markdown was designed specifically to describe **sequences of scenes**, **agents**, **messages** and **interactions**. We call it interchangebly **Winding Markdown** and `winding.md`. It makes it easier to **illuminate**, to search for a scene that would fit the story, to deal with retroactivity when writing a story, and to create **stable points** and consistent sequences of scenes. 

And we call the process of writing in it **winding** and a resulting document a **winding**. It combines storytelling and typesetting. It allows both to write a story, page by page, and leave precise layout messages for the scenes, text, image, and transparent regions. It strikes a balance between plain-text readability and structured design. It's kind of like if USD, CSS, Smalltalk, Markdown and Python got together on a windy day, and reminiscing GML had taught a trick or two to a new AI kid on the block. 

We call a process of searching for a stable point in a winding **illuminating**. It combines typesetting, illustration, and storytelling.

And that, is kind of like if Feynman, as if he was there all along, explained **state spaces**, **interactions**, **retroactivity** and **stable points** to the kid really clearly, that when illuminating, messages are like light going over all paths and bouncing off the spatial boundaries, and attenuating. And then they went to fly their dragons, and when they were back, the kid was like, "I get it now! It's like when I fly a dragon, I need to think of all the paths other dragons can take, and how they interact with the wind and the terrain, the clouds and the sun. And dance with them. It's like a dance of information!" And Feynman smiled, knowing that the kid had totally grasped it.


## Spatial Model: Agents and Spaces

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

```
@right: page
```

→ tells `right` to adopt the trait `page`, to become a `page`.

#### Multiple roles:
```
@right: page, text, centered
```

→ sends 3 messages: “you are a `page`, you are `text`, and you are `centered`”

#### Property setting:
```
@dragon.eyes: green
Alive and functional - HCI.
```

→ sends 2 messages: “you are a `green`” and “you are `Alive and functional - HCI.`” 


### Image Block Revisited, as an Agent
```
@image: wind-on-the-grass.png, cutout, square
I'm just testing, sorry.
This is not defining a new image. It’s sending a message to image, saying:

"Become wind-on-the-grass.png, and take on the traits cutout, square."
Everything that follows in the current space is assumed to talk to that now-transformed image — unless another agent is addressed.

You're speaking to something, not defining it. But you are using true names.
```

---
### Parser/Tooling Compatibility
No indentation rules. No nesting.