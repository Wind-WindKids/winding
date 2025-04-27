# This is a sample Winding Markdown snippet that defines an image and a Python script to parse it.
# The script uses Pydantic to define the data model and OpenAI's API to parse the snippet.

snippet = '''---
wind_on_the_grass: image, square, png
---
Wind lies in the grass in front of two laptops, focused on screen.right.  
Sunlight glows through his hair. His back is to us.  

@laptops: two, side by side

@screen.left:
A robotics sim, Omniverse or Isaac Sim.

@sim-subject:
A metallic quadruped dragon stands in a virtual rig.  
Inspired by Japanese motorcycles and robotic dogs. Battery and hydrogen  
cell powered. Metal wings folded. Intake fan centered.  

@dragon.eyes: green — functional, HCI.

@screen.right:
VSCode. Terminal open. Logs streaming.  
@code.density: high  

@Wind:
boy, around 8 years old, tousled blond hair, bright blue eyes.

@Wind.focus: full, wind types rapidly, in flow.
@Wind.hair: soft, gold-tinted, unstyled
@phone: nearby, dark screen
'''

def main():
    """Parses a sample Winding Markdown snippet and prints the resulting Pydantic model."""    

    from openai import OpenAI
    # from winding.ast import Winding
    from winding.grammar import grammar

    from typing import List, Union, Optional
    from pydantic import BaseModel, Field


    class Image(BaseModel):
        caption: str = Field(..., description="Image caption.")
        url: str = Field(..., description="Image URL.")

    class Markdown(BaseModel):
        content: Union[str, 'Markdown', Image] = Field(
            ..., description="Plain text, nested Markdown, or Image node."
        )

    class Winding(BaseModel):
        at: str = Field(description="The @at recipient, a valid identifier.")
        attributes: List[str] = Field(
            default_factory=list,
            description="Modifiers (e.g., size, orientation, !negation)."
        )
        content: List[Union[Markdown, 'Winding']] = Field(
            default_factory=list,
            description="Child nodes: text (Markdown), or nested directives (Winding)."
        )

    # For forward references
    Markdown.update_forward_refs()
    Winding.update_forward_refs()


    client = OpenAI()


    response = client.responses.parse(
        model="gpt-4o-2024-08-06",
        instructions=f"Parse the following Winding Markdown snippet into our Pydantic schema, if this helps here is EBNF: {grammar}",
        input=snippet,
        text_format=Winding,
    )

    print(response)


if __name__ == "__main__":
    main()