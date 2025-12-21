#!/usr/bin/env python3

import subprocess
import sys
import json
import os

def stream_cursor_agent(prompt, force=False):
    command = [
        "cursor", "agent",
        "--print",
        "--output-format", "stream-json",
        "--stream-partial-output",
    ] + (["--force"] if force else []) + [ 
        "--",
        prompt
    ]
    
    GRAY = "\033[90m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    try:
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue
            
            try:
                data = json.loads(line)
                msg_type = data.get("type")
                
                if msg_type == "thinking":
                    text = data.get("text", "")
                    if text:
                        print(f"{GRAY}{text}{RESET}", end='', flush=True)
                
                elif msg_type == "assistant":
                    content_list = data.get("message", {}).get("content", [])
                    for item in content_list:
                        if item.get("type") == "text":
                            print(item.get("text"), end='', flush=True)
                
                elif msg_type == "tool_call":
                    subtype = data.get("subtype")
                    tool_info = data.get("tool_call", {})
                    call_name = next(iter(tool_info.keys()), "tool") if tool_info else "tool"
                    
                    if subtype == "started":
                        print(f"\n{BLUE}[Executing {call_name}...]{RESET}", flush=True)

            except json.JSONDecodeError:
                if line:
                    print(f"\n{line}")

    except KeyboardInterrupt:
        process.terminate()
        print("\n\nAgent interrupted.")
    finally:
        process.wait()

def load_file(filename):
    """Loads a file from the script's directory or the current directory."""
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(script_dir, filename)
        if not os.path.exists(path):
            path = filename
        with open(path, "r") as f:
            return f.read()
    except Exception:
        return ""

COMMAND_RECIPES = {
    "illuminate": """
    1. Read {target}.md.
    2. Parse it as Winding Markdown (refer to winding.md for grammar details).
    3. Generate the artifact (code/file) based on the intent and receivers.
    4. Run the artifact and display results.
    """,
    "artifact": "Read {target}.md, parse its Winding intent, and generate/update the artifact. Do not run.",
    "run": "Locate and execute the artifact associated with {target}.",
    "wind": "Update {target}.md by adding the intent: '{extra_intent}', then refresh the artifact.",
    "unwind": "Update {target}.md by removing/negating the intent: '{extra_intent}', then refresh the artifact.",
}

if __name__ == "__main__":
    cmd_path = sys.argv[0]
    cmd_name = os.path.basename(cmd_path)
    if cmd_name.endswith(".py"):
        cmd_name = "wind"

    if len(sys.argv) < 2:
        print(f"Usage: {cmd_name} <target> [intent...]")
        sys.exit(1)
    
    target = sys.argv[1]
    extra_intent = " ".join(sys.argv[2:])
    
    # Core distillation
    spec = load_file("prompt.md")
    # Operation definitions & simulations
    ops = load_file("wind.md")
    
    recipe = COMMAND_RECIPES.get(cmd_name, f"Perform {cmd_name} on {target}.")

    full_prompt = f"""
# SYSTEM: WINDING ENGINE
{spec}

# OPERATION REFERENCE (wind.md)
{ops}

# TASK: {cmd_name.upper()}
Target: {target}
Recipe: {recipe.format(target=target, extra_intent=extra_intent)}

# INSTRUCTIONS
- Refer to `winding.md` for formal grammar if you encounter complex syntax.
- Use your tools to read, write, and execute.
- Be concise and artifact-focused.
"""

    force = (cmd_name in ["illuminate", "run"])
    stream_cursor_agent(full_prompt.strip(), force)
