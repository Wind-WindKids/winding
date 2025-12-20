import subprocess
import sys
import json

def stream_cursor_agent(prompt):
    command = [
        "cursor", "agent",
        "--print",
        "--output-format", "stream-json",
        "--stream-partial-output",
        prompt
    ]

    # Colors for CLI
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
                    # Display "thinking" deltas in gray
                    text = data.get("text", "")
                    if text:
                        print(f"{GRAY}{text}{RESET}", end='', flush=True)
                
                elif msg_type == "assistant":
                    # Display the actual response
                    content_list = data.get("message", {}).get("content", [])
                    for item in content_list:
                        if item.get("type") == "text":
                            print(item.get("text"), end='', flush=True)
                
                elif msg_type == "tool_call":
                    # Display tool interactions in blue
                    subtype = data.get("subtype")
                    tool_info = data.get("tool_call", {})
                    call_name = next(iter(tool_info.keys()), "tool") if tool_info else "tool"
                    
                    if subtype == "started":
                        print(f"\n{BLUE}[Executing {call_name}...]{RESET}", flush=True)
                    elif subtype == "completed":
                        # Tool finish is often silent in "human readable" unless it fails
                        pass

            except json.JSONDecodeError:
                # Fallback for unexpected non-JSON output (errors, etc.)
                if line:
                    print(f"\n{line}")

    except KeyboardInterrupt:
        process.terminate()
        print("\n\nAgent interrupted.")
    finally:
        process.wait()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test.py \"Your prompt here\"")
        sys.exit(1)
    
    user_prompt = " ".join(sys.argv[1:])
    print(f"--- Cursor Agent: {user_prompt} ---\n")
    stream_cursor_agent(user_prompt)
    print("\n\n--- Finished ---")