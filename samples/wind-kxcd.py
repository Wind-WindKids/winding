#!/usr/bin/env python3
"""
This script converts xkcd Hugging Face dataset into Winding Markdown `.md` 
files in the `output/` directory. You can supply `--examples 3.md 5.md`
to use as examples for the model. 
The script uses the OpenAI API, so you need to set the `OPENAI_API_KEY`
"""


import os
import json
import argparse
import asyncio
import aiohttp
from datasets import load_dataset
from openai import AsyncOpenAI
from tqdm.asyncio import tqdm_asyncio
import base64


client = AsyncOpenAI(timeout=600.0, max_retries=1)

def format_record_message(record: dict):
    data = record.get("image")['bytes']
    
    # build a copy without the image field for JSON serialization
    record_copy = {k: v for k, v in record.items() if k != "image"}
    text_content = {"type": "text", "text": json.dumps(record_copy)}

    print(f"Processing record {record['number']} with image type {type(data)}")
    base64_image = base64.b64encode(data).decode("utf-8")

    # save the image for debugging
    image_path = os.path.join("output", f"{record['number']}.jpg")
    with open(image_path, "wb") as img_file:
        img_file.write(data)
            
    image_content = {
                    "type": "image_url",
                    "image_url": {"url" : f"data:image/jpeg;base64,{base64_image}"}
                }

    return [text_content, image_content]





def build_base_messages(spec: str, examples: list):
    """Construct the system prompt + demonstration examples."""
    system_prompt = f"""Please, transforms xkcd explain records into Winding Markdown documents.
Use the following Winding Markdown specification:
===
{spec}
===
Generate a complete Winding Markdown “winding” that captures the scene, transcript, and explanation."""
    messages = [{"role": "system", "content": system_prompt}]
    for ex in examples:
        record = ex["record"]
        
        messages.append({"role": "user", "content": format_record_message(record)})
        messages.append({"role": "assistant", "content": ex["winding"]})
    return messages


async def generate_winding(record: dict, base_messages: list, model: str, max_tokens: int):
    user_msg = {"role": "user", "content": format_record_message(record)}
    resp = await client.chat.completions.create(
        model=model,
        messages=base_messages + [user_msg],
        max_completion_tokens=max_tokens,
        stream=False
    )
    return resp.choices[0].message.content

async def worker(record: dict, sem: asyncio.Semaphore, base_msgs: list, args):
    async with sem:
        try:
            winding = await generate_winding(record, base_msgs, args.model, args.max_completion_tokens)
            out_path = os.path.join(args.output_dir, f"{record['number']}.md")
            with open(out_path, "w") as f:
                f.write(winding)
            return record["number"]
        except Exception as e:
            print(f"[Error] Record {record['number']}: {e}")
            return None

async def process_all(records: list, base_msgs: list, args):
    sem = asyncio.Semaphore(args.num_workers)
    tasks = [worker(rec, sem, base_msgs, args) for rec in records]
    return await tqdm_asyncio.gather(*tasks)

def main():
    parser = argparse.ArgumentParser(description="Generate Winding Markdown from explainxkcd dataset")
    parser.add_argument("--dataset",       type=str, default="olivierdehaene/xkcd", help="HF dataset identifier")
    parser.add_argument("--model",         type=str, required=True, help="Model endpoint name")
    parser.add_argument("--spec",      type=str, default="winding.md", help="The Winding Markdown spec")
    parser.add_argument("--output_dir",    type=str, default="output", help="Directory to write .md files")
    parser.add_argument("--examples",      type=str, nargs="+", help="List of example `{number}.md` files to use", default=[])
    parser.add_argument("--num_workers",   type=int, default=10, help="Number of parallel requests (>=2)")
    parser.add_argument("--max_completion_tokens", type=int, default=512, help="Max tokens for completion")
    parser.add_argument("--max_samples",   type=int, help="Limit on number of records to process", default=2)
    parser.add_argument("--start_index", type=int, default=0, help="Start index for processing records")
    args = parser.parse_args()

    # 

    os.makedirs(args.output_dir, exist_ok=True)

    # Load dataset into memory
    ds = load_dataset(args.dataset, split="train").to_dict()
    records = [dict(zip(ds.keys(), vals)) for vals in zip(*ds.values())]

    # Prepare examples (dynamic if --examples provided)
    examples = []
    for path in args.examples:
        num = os.path.splitext(os.path.basename(path))[0]
        rec = next((r for r in records if str(r.get("number")) == str(num)), None)
        if rec is None:
            raise ValueError(f"No record with number `{num}` found in dataset")
        with open(path, "rt") as f:
            winding_text = f.read()
        examples.append({"record": rec, "winding": winding_text})

    if args.start_index:
        records = records[args.start_index:]
    if args.max_samples:
        records = records[: args.max_samples]


    # load spec and build messages
    with open(args.spec, "r") as f:
        spec = f.read().strip()
    base_messages = build_base_messages(spec, examples)

    # Generate all windings
    results = asyncio.run(process_all(records, base_messages, args))
    done = len([r for r in results if r])
    print(f"Completed {done}/{len(records)} windings.")

if __name__ == "__main__":
    main()
