#!/usr/bin/env python3

import argparse
import os
import asyncio
from openai import AsyncOpenAI
from tqdm.asyncio import tqdm_asyncio

async def initial(args, client):
    # Create the prompt
    prompt = f"""You are
 tasked with creating an engaging {args.type} story suitable for {args.age} year olds. Follow these instructions to structure and write the story:

Step 1: Sketch
- Craft a title, it can be dull, but it should be satisfying
- Write each paragraph clearly and vividly, ensure:
- Appropriate pacing and detail for a story
- Engaging narrative voice and tone
- The story reaches a satisfying conclusion.

Step 2: Feedback
- Act as a critic, write a few slightly disrespectful tweets, punching holes in the story

Step 3: Editing
- Review and suggest improvements or a rewrite, take the tweets seriously

Step 4: Write
- Output: "=== final ===" in lower case
- Write the final version of the story 

Place it in the {args.theme}, for example {args.location}."""

    print(f"Generating a {args.type} story for {args.age} year olds with theme '{args.theme}' set in '{args.location}'...")
    
    try:
        # Call OpenAI API asynchronously
        response = await client.chat.completions.create(
            model=args.model,  # You can change the model as needed
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=5000,
            temperature=args.temperature,
        )
        
        # Print the generated story
        print("\n" + "=" * 50 + " INITIAL " + "=" * 50 + "\n")
        print(response.choices[0].message.content)
        print("\n" + "=" * 120 + "\n")
        
    except Exception as e:
        print(f"Error occurred while calling the OpenAI API: {e}")
        raise e

    if "=== final ===" not in response.choices[0].message.content:
        print("Warning: The final version of the story was not found in the response.")
        raise ValueError("The final version of the story was not found in the response.")

    story = response.choices[0].message.content.split("=== final ===")[-1].strip()
    return story


async def feedback(args, client, story, feedback=None):
    prompt = f"""You are tasked with providing feedback to a {args.type} story suitable for {args.age} year olds placed in {args.theme} at {args.location}. The story is as follows:

{story}


Act as a critic, write a few slightly disrespectful constructive criticism tweets, punching holes in the story. Output the tweets only, no other text.
"""

    try:
        response = await client.chat.completions.create(
            model=args.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=args.temperature,
        )
        
        print("\n" + "=" * 50 + " FEEDBACK " + "=" * 50 + "\n")
        print(response.choices[0].message.content)
        print("\n" + "=" * 120 + "\n")
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error occurred while getting feedback: {e}")
        return "Error generating feedback."


async def degrade(args, client, story):
    prompt = f"""
    You are tasked with creating a low quality preference pair for a {args.type} story suitable for {args.age} year olds.  Take this story:
====
{story} 
====
    
    and rewrite to get a worse version of it. Output that degraded version of a story and no other text.
    """

    try:
        response = await client.chat.completions.create(
            model=args.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=args.temperature,
        )
        
        print("\n" + "=" * 50 + " DEGRADE " + "=" * 50 + "\n")
        print(response.choices[0].message.content)
        print("\n" + "=" * 120 + "\n")
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error occurred while degrading the story: {e}")
        return "Error generating degraded story."


async def score(args, client, feedback):
    prompt = f"""As an expert in children's literature for {args.age} year olds, you're evaluating a {args.type} story set in {args.theme} at {args.location}, based on critical feedback. The feedback is as follows:

{feedback}

Evaluate this feedback using these criteria:
- Plot coherence (0-3 points)
- Character development (0-2 points)
- Creativity (0-2 points)
- Age-appropriate content (0-1 points)
- Setting integration (0-1 points)
- Engagement potential (0-1 points)

Calculate a total score between 0-10.
Respond with ONLY the numeric score (e.g., "3.5"), no other text.
"""

    try:
        response = await client.chat.completions.create(
            model=args.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=10,
            temperature=args.temperature,
        )
        
        score_text = response.choices[0].message.content.strip()
        try:
            score = float(score_text)
            return score
        except ValueError:
            print(f"Could not convert score '{score_text}' to a number. Using default score of 5.")
            return 1.0
        
    except Exception as e:
        print(f"Error occurred while scoring: {e}")
        return 1.0


async def improve(args, client, story, feedback):
    prompt = f"""You are a master storyteller specializing in children's literature for {args.age}-year-olds. Your task is to significantly improve or reimagine a story based on critical feedback. Follow these steps:

Step 1: Sketch
- Review the following story sketch
{story} 

Step 2: Feedback
- Read the following feedback
{feedback}

Step 3: Editing
- Review and suggest to reimagine or improve. Take the tweets seriously, if the story is bad, write a different one without any elements from the original story sketch.

Step 4: Write
- Output: "=== reimagine ===" or "=== improve ===" in lower case
- Write the final version of the story 

This should be a {args.type} story. Place it in the {args.theme}, for example {args.location}."""

    print("\n" + "=" * 50 + " IMPROVEMENT PROMPT " + "=" * 50 + "\n")
    print(prompt)
    print("\n" + "=" * 120 + "\n")

    response = await client.chat.completions.create(
        model=args.model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=8000,
        temperature=args.temperature,
    )

    content = response.choices[0].message.content
    
    print("\n" + "=" * 50 + " IMPROVED STORY " + "=" * 50 + "\n")
    print(content)
    print("\n" + "=" * 120 + "\n")

    if "=== reimagine ===" in content:
        improved_story = content.split("=== reimagine ===")[-1].strip()
    elif "=== improve ===" in content:
        improved_story = content.split("=== improve ===")[-1].strip()
    else:
        print("Warning: The final version of the story was not found in the response.")
        raise ValueError("The final version of the story was not found in the response.")

    if len(improved_story) < 1000:
        print("Warning: The improved story is too short.")
        raise ValueError("The improved story is too short.")

    return improved_story


async def process_story(args, client, semaphore, stories_lock, stories, i, iteration):
    """Process a single story improvement with a semaphore for concurrency control."""
    async with semaphore:
        # Get the best story to improve
        async with stories_lock:
            best_score_so_far = max(stories, key=lambda x: x["score"])["score"]
            best_stories_so_far = [s for s in stories if s["score"] == best_score_so_far]
            best_story_so_far = best_stories_so_far[i % len(best_stories_so_far)]
        
        print(f"Worker {i}: Improving story with score {best_story_so_far['score']} (iteration {iteration+1})")
        
        try:
            # Improve the story
            improved_story = await improve(args, client, best_story_so_far["story"], best_story_so_far["feedback"])
            
            # Get feedback and score for the improved story
            story_feedback = await feedback(args, client, improved_story)
            score_value = await score(args, client, story_feedback)
            
            print(f"Worker {i}: Finished improvement with score {score_value} (iteration {iteration+1})")
            
            # Add the improved story to the shared list
            async with stories_lock:
                stories.append({"score": score_value, "story": improved_story, "feedback": story_feedback})
                return score_value
                
        except Exception as e:
            print(f"Worker {i}: Error during story processing: {e}")
            return None


async def improve_loop_async(args, client, story, score_value, story_feedback):
    # Initialize story collection
    stories = []
    stories.append({"score": score_value, "story": story, "feedback": story_feedback})
    
    # Create a lock for the shared stories list
    stories_lock = asyncio.Lock()
    
    # Create a semaphore to limit concurrency
    semaphore = asyncio.Semaphore(args.num_workers)
    
    # Run multiple iterations with parallel workers
    for iteration in range(0, args.iterations, args.num_workers):
        remaining = min(args.num_workers, args.iterations - iteration)
        print(f"\nRunning batch of {remaining} improvements (iterations {iteration+1}-{iteration+remaining})")
        
        # Create tasks for each worker in this batch
        tasks = []
        for i in range(remaining):
            task = asyncio.create_task(
                process_story(args, client, semaphore, stories_lock, stories, i, iteration+i)
            )
            tasks.append(task)
        
        # Wait for all tasks to complete
        await asyncio.gather(*tasks)
    
    # Find the best story
    best_story = max(stories, key=lambda x: x["score"])
    best_score = best_story["score"]

    print(f"\nBest score achieved: {best_score}")
    print("\n" + "=" * 50 + " FINAL STORY " + "=" * 50 + "\n")
    print(best_story["story"])
    print("\n" + "=" * 120 + "\n")
    
    return best_story


async def main_async():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate a story using OpenAI API')
    parser.add_argument('--age', type=int, default=12, help='Age of the target audience (default: 12)')
    parser.add_argument('--type', type=str, default='bedtime', help='Type of story (default: bedtime)')
    parser.add_argument('--theme', type=str, default='modern city', help='Theme of the story (default: modern city)')
    parser.add_argument('--location', type=str, default='Paris, park luxembourg gardens.', 
                        help='Location where the story takes place (default: Luxembourg Gardens)')
    parser.add_argument('--degrade', action='store_true', help='Degrade the story')
    parser.add_argument('--iterations', type=int, default=20, help='Number of iterations for story generation (default: 100)')
    parser.add_argument('--num_workers', type=int, default=10, help='Number of concurrent workers (default: 10)')
    parser.add_argument('--model', type=str, default='mistralai/Mistral-Small-3.1-24B-Instruct-2503', help='The model to use (default: mistralai/Mistral-Small-3.1-24B-Instruct-2503)')
    parser.add_argument('--endpoint', type=str, default='http://127.0.0.1:8001/v1',
                        help='The OpenAI API endpoint (default: 127.0.0.1:8001/v1)')
    parser.add_argument('--temperature', type=float, default=0.15, help='Temperature for randomness (default: 0.15)')
    
    args = parser.parse_args()
    
    # Check if OpenAI API key is available
    if 'OPENAI_API_KEY' not in os.environ:
        print("Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        print("You can create a .env file with the line: OPENAI_API_KEY=your_api_key_here")
        return
    
    # Configure async OpenAI client
    client = AsyncOpenAI(api_key=os.environ['OPENAI_API_KEY'], timeout=600.0, max_retries=3, 
                         base_url=args.endpoint)
    
    story = """In the bustling heart of Paris, where the Seine River flowed gently beneath the city's glittering lights, lay the tranquil Luxembourg Gardens. Beloved by both locals and visitors, these gardens offered lush greenery, sparkling fountains, and vibrant blooms. Among its frequent visitors was Sophie, a curious and imaginative teen who enjoyed spending sunny afternoons relaxing and scrolling through TikTok in her favorite quiet spot.

One bright afternoon, Sophie noticed something unusual under a stone bench—an old, weathered book. Intrigued, she picked it up and flipped through pages filled with intriguing sketches and cryptic riddles. The book hinted at a hidden treasure in the gardens, supposedly left behind by a famous Parisian artist.

Initially skeptical yet curious enough for new content, Sophie decided to follow the riddles. She captured each step of her journey in short videos, solving clues cleverly planted throughout the gardens. Along the way, she found delightful items like a delicate silver locket, an antique quill, and a tiny porcelain figurine, all of which she enthusiastically documented on her TikTok.

Finally, the last riddle led Sophie to an ancient oak in a secluded corner. Inspecting closely, she noticed a hollow spot hidden behind loose bark. She gently removed the bark to reveal a small, beautifully carved chest. With growing excitement, she opened it and found a stunning painting, vibrant with color and charm, labeled clearly as part of a special social media event.

At that moment, cheers erupted around her. Sophie turned in surprise to see smiling creators and a camera crew approaching. "Congratulations, Sophie! You've successfully completed the first-ever TikTok treasure hunt on our new show, 'Hidden Gardens'! Everything you've found was planted by our team, and you captured every step beautifully."

Sophie laughed, delighted and relieved. Soon after, she was invited to feature her adventure clips on the show's TikTok channel and participate in an upcoming teen event.

And now, it's time to sleep—don't forget to say thank you for the story!

"""

    # Generate initial story
    #story = await initial(args, client)
    story_feedback = await feedback(args, client, story)
    score_value = await score(args, client, story_feedback)

    print(f"Initial Score: {score_value}")

    if args.degrade:
        # Degrade the story
        degraded_story = await degrade(args, client, story)
        print("\n" + "=" * 50 + " DEGRADE " + "=" * 50 + "\n")
        print(degraded_story)
        print("\n" + "=" * 120 + "\n")

        # Score the degraded story
        degraded_story_feedback = await feedback(args, client, degraded_story)
        degraded_score_value = await score(args, client, degraded_story_feedback)
        print(f"Degraded Score: {degraded_score_value}")

        return

    # Improve the story using feedback with async workers
    await improve_loop_async(args, client, story, score_value, story_feedback)


def main():
    asyncio.run(main_async())

    
if __name__ == "__main__":
    main()