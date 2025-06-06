import json
import random

def generate_tool_candidates(num_tools=150):
    """Generates a list of plausible AI tool candidate dictionaries."""
    candidates = []
    categories = ["Art", "Audio", "Developer", "Productivity", "Video", "Copywriting", "LLM", "Research", "Xtras", "Education", "SEO", "Social Media", "Gaming", "Health", "Fashion", "Legal", "Enterprise", "No Code", "Photos", "Music", "Design"]
    tags = ["Free", "Freemium", "Paid", "Open-source", "Contact for pricing", "Subscription", "One-time purchase"]

    common_actions_verbs = ["Create", "Generate", "Analyze", "Automate", "Optimize", "Transform", "Build", "Discover", "Enhance", "Manage", "Edit", "Summarize", "Translate", "Detect", "Personalize", "Monitor", "Simulate", "Integrate"]
    common_nouns_objects = ["images", "audio", "code", "workflows", "videos", "text", "models", "data", "content", "reports", "designs", "insights", "apps", "chatbots", "presentations", "music", "3D assets", "social posts", "research papers", "legal documents"]
    common_adj_benefits = ["stunning", "high-quality", "efficient", "intelligent", "personalized", "seamless", "powerful", "easy-to-use", "innovative", "next-generation", "AI-powered", "automated", "data-driven"]
    tool_name_suffixes = ["AI", "Bot", "GPT", "Sense", "Flow", "Kit", "Spark", "Pilot", "Mate", "Gen", "Craft", "Labs", "Studio", "Ninja", "Wise", "Synth"]
    tool_name_prefixes = ["Quantum", "Neuro", "Cogni", "Data", "Pixel", "Sound", "Code", "Task", "Media", "Write", "Deep", "Robo", "Smart", "Auto"]

    for i in range(num_tools):
        # Generate Title
        prefix = random.choice(tool_name_prefixes)
        suffix = random.choice(tool_name_suffixes)
        middle_word_count = random.randint(0,1)
        middle_words = [random.choice(common_nouns_objects).capitalize().replace(" ", "") for _ in range(middle_word_count)]
        if middle_words:
            title = f"{prefix}{''.join(middle_words)}{suffix}"
        else:
            title = f"{prefix}{suffix}"
        if random.random() < 0.3: # Add a number sometimes
            title += str(random.randint(1, 1000))

        # Generate URL
        url_name = title.lower().replace(" ", "").replace("AI", "ai").replace("GPT", "gpt")
        url = f"https://www.{url_name}.com"
        if random.random() < 0.2:
            url = f"https://www.{url_name}.ai"
        elif random.random() < 0.1:
            url = f"https://www.{url_name}.io"


        # Generate Body
        verb = random.choice(common_actions_verbs)
        adj = random.choice(common_adj_benefits)
        noun = random.choice(common_nouns_objects)
        body = f"{verb} {adj} {noun} with our innovative platform."
        if random.random() < 0.5:
            body = f"Your go-to solution for {verb.lower()}ing {noun}. {random.choice(common_adj_benefits).capitalize()} results, effortlessly."
        if random.random() < 0.2:
            body += f" Powered by cutting-edge AI technology to streamline your {random.choice(common_nouns_objects)} creation."


        category_guess = random.choice(categories)
        tag_guess = random.choice(tags)

        # Refine category based on keywords in title/body
        if any(kw in title.lower() or kw in noun.lower() for kw in ["art", "image", "photo", "design", "visual", "graphic", "draw", "paint"]):
            category_guess = random.choice(["Art", "Design", "Photos"])
        elif any(kw in title.lower() or kw in noun.lower() for kw in ["audio", "music", "sound", "voice", "podcast"]):
            category_guess = random.choice(["Audio", "Music"])
        elif any(kw in title.lower() or kw in noun.lower() for kw in ["video", "film", "animation", "clip"]):
            category_guess = "Video"
        elif any(kw in title.lower() or kw in noun.lower() for kw in ["code", "develop", "debug", "deploy", "software", "API"]):
            category_guess = "Developer"
        elif any(kw in title.lower() or kw in noun.lower() for kw in ["text", "write", "copy", "content", "summarize", "translate", "blog", "article"]):
            category_guess = "Copywriting"
        elif any(kw in title.lower() or kw in noun.lower() for kw in ["llm", "gpt", "chatbot", "language model"]):
            category_guess = "LLM"
        elif any(kw in title.lower() or kw in noun.lower() for kw in ["task", "meeting", "schedule", "workflow", "automate", "organize"]):
            category_guess = "Productivity"
        elif any(kw in title.lower() or kw in noun.lower() for kw in ["data", "research", "analyze", "insight", "report"]):
            category_guess = "Research"
        elif any(kw in title.lower() or kw in noun.lower() for kw in ["seo", "keyword", "ranking"]):
            category_guess = "SEO"
        elif any(kw in title.lower() or kw in noun.lower() for kw in ["social", "tweet", "post", "influencer"]):
            category_guess = "Social Media"


        candidates.append({
            "title": title,
            "body": body,
            "url": url,
            "category_guess": category_guess,
            "tag_guess": tag_guess
        })

    return candidates

if __name__ == "__main__":
    num_candidates = 160  # Generate a bit more to ensure we have at least 150 unique enough ones
    tool_candidates = generate_tool_candidates(num_candidates)

    output_filepath = "candidate_tools.json"
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(tool_candidates, f, indent=2)
        print(f"Successfully generated and saved {len(tool_candidates)} tool candidates to {output_filepath}")
    except IOError:
        print(f"Error: Could not write to output file {output_filepath}")

    # Sanity check: print first few candidates
    # for i, tool in enumerate(tool_candidates[:3]):
    #     print(f"\nCandidate {i+1}:")
    #     print(f"  Title: {tool['title']}")
    #     print(f"  URL: {tool['url']}")
    #     print(f"  Body: {tool['body']}")
    #     print(f"  Category: {tool['category_guess']}")
    #     print(f"  Tag: {tool['tag_guess']}")
