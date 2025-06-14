import json

def custom_title_case(title_str):
    # Trim leading "AI " or "Ai "
    if title_str.lower().startswith("ai "):
        title_str = title_str[3:]
    # Trim leading "AI" if followed by an uppercase or if it's the whole word and next is not space
    elif title_str.startswith("AI") and (len(title_str) == 2 or (len(title_str) > 2 and title_str[2].isupper())):
        title_str = title_str[2:]
    elif title_str.startswith("Ai") and (len(title_str) == 2 or (len(title_str) > 2 and title_str[2].isupper())):
        title_str = title_str[2:]


    words = title_str.split()
    if len(words) > 3:
        words = words[:3]

    acronyms = ["AI", "IO", "UI", "MO", "CPU", "API", "MOE", "SDK", "OCR", "R1", "V3", "ID", "3D", "4K", "TS", "IDE", "QA", "PR", "SEO", "LLM", "TTS", "SVC", "GPT", "AIUX", "ML"]
    # Ensure all acronyms are strings for comparison
    acronyms = [str(ac) for ac in acronyms]

    cased_words = []
    for i, word in enumerate(words):
        # Preserve parts like .Ai, .Com
        if '.' in word and not word.endswith('.'):
            parts = word.split('.')
            cased_parts = []
            for p_idx, p_val in enumerate(parts):
                if p_val.upper() in acronyms:
                    cased_parts.append(p_val.upper())
                elif p_idx == 0 or len(p_val) > 2 or p_val.lower() in ["ai", "io", "ui"]: # common short tech terms
                     cased_parts.append(p_val.capitalize())
                else:
                    cased_parts.append(p_val.lower())
            cased_words.append(".".join(cased_parts))
            continue

        if word.upper() in acronyms:
            cased_words.append(word.upper())
        elif len(word) > 2 or i == 0: # Capitalize if long or first word
            cased_words.append(word.capitalize())
        else: # Short words (not first, not acronym) remain lowercase
            cased_words.append(word.lower())

    # Ensure first word is capitalized if it's not an acronym and became lowercase
    if cased_words and cased_words[0].islower() and cased_words[0].upper() not in acronyms:
        cased_words[0] = cased_words[0].capitalize()

    return " ".join(cased_words)

def format_body(body_str):
    if not body_str:
        return ""

    processed_body = body_str[0].upper() + body_str[1:]

    if len(processed_body) > 50:
        # if len(body_str) <= 50: # This check is redundant as processed_body is already > 50
        #      return body_str[:50]

        original_was_longer = len(body_str) > 50

        # Attempt to break at last space before 47 chars for "..."
        truncated_at_space = False
        if original_was_longer:
            limit = 47
            if ' ' in processed_body[:limit]:
                last_space = processed_body[:limit].rfind(' ')
                if last_space != -1:
                    processed_body = processed_body[:last_space] + "..."
                    truncated_at_space = True

        if not truncated_at_space: # If no space found, or original was not much longer
            # Truncate and check for existing punctuation to replace with "..."
            # Or just add "..." if no punctuation at the very end of truncated part
            temp_truncated = processed_body[:47]
            if temp_truncated.endswith(('.', '!', '?')):
                 processed_body = temp_truncated[:-1] + "..."
            elif original_was_longer : # only add ... if it was actually truncated from a longer string
                 processed_body = temp_truncated + "..."
            else: # if not much longer, just return the truncated string up to 50
                 processed_body = processed_body[:50]


    return processed_body[:50]

# Load existing tools
try:
    with open("src/data/tools.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: src/data/tools.json not found.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error: src/data/tools.json is not valid JSON. Details: {e}")
    exit(1)

tools_data_list = data.get("tools", [])

new_tools_input = [
  {
    "title": "Chatgpt",
    "body": "OpenAI's chatgpt",
    "tag": "Freemium",
    "url": "https://chat.openai.com?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "ChatGPT and other AI chat assistant"
  },
  {
    "title": "Deepseek",
    "body": "DeepSeek's AI assistant. [API](https://platform...",
    "tag": "Freemium",
    "url": "https://chat.deepseek.com?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "ChatGPT and other AI chat assistant"
  },
  {
    "title": "Claude",
    "body": "Anthropic's AI assistant",
    "tag": "Freemium",
    "url": "https://claude.ai?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "ChatGPT and other AI chat assistant"
  },
  {
    "title": "Gemini",
    "body": "Google's conversational, AI chat service....",
    "tag": "Free",
    "url": "https://gemini.google.com?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "ChatGPT and other AI chat assistant"
  },
  {
    "title": "Grok",
    "body": "XAI's AI assistant",
    "tag": "Free",
    "url": "https://x.com/i/grok?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "ChatGPT and other AI chat assistant"
  },
  {
    "title": "Microsoft Copilot",
    "body": "Microsoft's AI assistant.",
    "tag": "Free",
    "url": "https://copilot.microsoft.com?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "ChatGPT and other AI chat assistant"
  },
  {
    "title": "Le Chat",
    "body": "Mistral.ai's conversational, AI chat service",
    "tag": "Free",
    "url": "https://chat.mistral.ai/chat?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "ChatGPT and other AI chat assistant"
  },
  {
    "title": "Qwen",
    "body": "Alibaba's AI assistant. Includes QwQ-32B,...",
    "tag": "Free",
    "url": "https://chat.qwen.ai?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "ChatGPT and other AI chat assistant"
  },
  {
    "title": "Perplexity.Ai",
    "body": "AI-driven conversational search engine.",
    "tag": "Free",
    "url": "https://www.perplexity.ai?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Search engine"
  },
  {
    "title": "Morphik.Ai",
    "body": "Open source AI-driven search engine for private...",
    "tag": "Free",
    "url": "https://morphik.ai?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Search engine"
  },
  {
    "title": "Deepseek-R1",
    "body": "DeepSeek's first-generation reasoning models,...",
    "tag": "Free",
    "url": "https://github.com/deepseek-ai/DeepSeek-R1?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Open Source LLMs"
  },
  {
    "title": "Deepseek-V3",
    "body": "A strong Mixture-of-Experts (MoE) language model...",
    "tag": "Free",
    "url": "https://github.com/deepseek-ai/DeepSeek-V3?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Open Source LLMs"
  },
  {
    "title": "Mixtral",
    "body": "Mixtral 8x7B, a high-quality sparse mixture of...",
    "tag": "Free",
    "url": "https://github.com/mistralai/mistral-inference?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Open Source LLMs"
  },
  {
    "title": "Grok-1",
    "body": "A large language model open sourced by xAI",
    "tag": "Free",
    "url": "https://github.com/xai-org/grok-1?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Open Source LLMs"
  },
  {
    "title": "Phi-3",
    "body": "Phi-3, a family of open AI models developed by...",
    "tag": "Free",
    "url": "https://github.com/microsoft/Phi-3CookBook?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Open Source LLMs"
  },
  {
    "title": "Lmsys Chatbot Arena Leaderboard",
    "body": "LMSYS Chatbot Arena is a crowdsourced open plat...",
    "tag": "Free",
    "url": "https://lmarena.ai/leaderboard?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "LLM Leaderboard"
  },
  {
    "title": "Artificial Analysis",
    "body": "Artificial Analysis is a platform that provides...",
    "tag": "Free",
    "url": "https://artificialanalysis.ai?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "LLM Leaderboard"
  },
  {
    "title": "Livecodebench",
    "body": "LiveCodeBench is a holistic and contamination-f...",
    "tag": "Free",
    "url": "https://livecodebench.github.io/leaderboard.html?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "LLM Leaderboard"
  },
  {
    "title": "Trae",
    "body": "Trae is your helpful coding partner. It offers...",
    "tag": "Free",
    "url": "https://www.trae.ai?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Programming Development"
  },
  {
    "title": "Marscode",
    "body": "Built-in AI programming assistant with capabili...",
    "tag": "Free",
    "url": "https://www.marscode.com?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Programming Development"
  },
  {
    "title": "Code-Translator",
    "body": "Open source project. Translates code from one...",
    "tag": "Not available",
    "url": "https://github.com/mckaywrigley/ai-code-translator?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Programming Development"
  },
  {
    "title": "Amazon Codewhisperer",
    "body": "A code writing assistant developed by Amazon",
    "tag": "Not available",
    "url": "https://aws.amazon.com/cn/codewhisperer?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Programming Development"
  },
  {
    "title": "Scalene",
    "body": "Scalene: a high-performance, high-precision CPU,...",
    "tag": "Free",
    "url": "https://github.com/plasma-umass/scalene?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Programming Development"
  },
  {
    "title": "Fitten Code",
    "body": "Fitten Code is an AI programming assistant driven...",
    "tag": "Free",
    "url": "https://code.fittentech.com/en?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Programming Development"
  },
  {
    "title": "Flappy",
    "body": "Production-Ready LLM Agent SDK for Every Developer",
    "tag": "Free",
    "url": "https://github.com/pleisto/flappy?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Programming Development"
  },
  {
    "title": "Midjourney",
    "body": "Enter text or pictures to create pictures",
    "tag": "Not available",
    "url": "https://www.midjourney.com?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Image Creation"
  },
  {
    "title": "Photoshop Ai",
    "body": "Adobe Photoshop generative-fill",
    "tag": "Not available",
    "url": "https://www.adobe.com/products/photoshop/generative-fill.html?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Image Creation"
  },
  {
    "title": "Stable Diffusion Webui",
    "body": "Open source project, input text or pictures to...",
    "tag": "Free",
    "url": "https://github.com/AUTOMATIC1111/stable-diffusion-webui?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Image Creation"
  },
  {
    "title": "Firefly",
    "body": "Adobe's AI image processing web site",
    "tag": "Freemium",
    "url": "https://firefly.adobe.com?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Image Creation"
  },
  {
    "title": "Ideogram.Ai",
    "body": "Enter text to create pictures. A product develo...",
    "tag": "Freemium",
    "url": "https://ideogram.ai?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Image Creation"
  },
  {
    "title": "Nero Ai",
    "body": "AI picture upscale, AI repair scratches, AI...",
    "tag": "Not available",
    "url": "https://ai.nero.com?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Image Creation"
  },
  {
    "title": "Skybox Ai",
    "body": "Generate 360-degree panoramic images using text...",
    "tag": "Freemium",
    "url": "https://skybox.blockadelabs.com?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Image Creation"
  },
  {
    "title": "Draggan",
    "body": "Interactive Point-based Manipulation on the...",
    "tag": "Free",
    "url": "https://github.com/XingangPan/DragGAN?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Image Creation"
  },
  {
    "title": "Visual-Chatgpt",
    "body": "Create images with ChatGPT",
    "tag": "Free",
    "url": "https://github.com/microsoft/visual-chatgpt?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Image Creation"
  },
  {
    "title": "Controlnet",
    "body": "ControlNet is a neural network structure to...",
    "tag": "Free",
    "url": "https://github.com/lllyasviel/ControlNet?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Image Creation"
  },
  {
    "title": "Seede Ai",
    "body": "Helps you create a poster in 1 min",
    "tag": "Not available",
    "url": "https://seede.ai?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Image Creation"
  },
  {
    "title": "Sora",
    "body": "Sora is an AI model published by OpenAI that can...",
    "tag": "Not available",
    "url": "https://openai.com/sora?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Video Creation"
  },
  {
    "title": "Kling Ai",
    "body": "AI Video Creation Tool by kuaishou.",
    "tag": "Not available",
    "url": "https://klingai.com?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Video Creation"
  },
  {
    "title": "Hailuoai",
    "body": "AI Video Creation Tool by Minimax",
    "tag": "Not available",
    "url": "https://hailuoai.com/video?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Video Creation"
  },
  {
    "title": "D-Id",
    "body": "Generate digital human dubbing video based on text",
    "tag": "Not available",
    "url": "https://studio.d-id.com?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Video Creation"
  },
  {
    "title": "Animatediff",
    "body": "AnimateDiff is a plug-and-play module turning...",
    "tag": "Free",
    "url": "https://github.com/guoyww/AnimateDiff?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Video Creation"
  },
  {
    "title": "Vivago.Ai/Video",
    "body": "Text to Video; Image to Video; 4K enhance",
    "tag": "Free",
    "url": "https://vivago.ai/video?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Video Creation"
  },
  {
    "title": "F/Awesome-Chatgpt-Prompts",
    "body": "This repo includes ChatGPT prompt curation to use...",
    "tag": "Free",
    "url": "https://github.com/f/awesome-chatgpt-prompts?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "LLM Prompts"
  },
  {
    "title": "Lm-Sys/Fastchat",
    "body": "An open platform for training, serving, and...",
    "tag": "Free",
    "url": "https://github.com/lm-sys/FastChat?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "LLM training platform"
  },
  {
    "title": "Auto-Gpt",
    "body": "Open source, An experimental open-source attempt...",
    "tag": "Not available",
    "url": "https://github.com/Torantulino/Auto-GPT?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Agent"
  },
  {
    "title": "Othersideai/Self-Operating-Computer",
    "body": "A framework to enable multimodal models to...",
    "tag": "Not available",
    "url": "https://github.com/OthersideAI/self-operating-computer?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Agent"
  },
  {
    "title": "Appagent",
    "body": "Multimodal Agents as Smartphone Users, an...",
    "tag": "Free",
    "url": "https://github.com/mnotgod96/AppAgent?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Agent"
  },
  {
    "title": "Microsoft/Autogen",
    "body": "AutoGen is an open-source programming framework...",
    "tag": "Free",
    "url": "https://github.com/microsoft/autogen?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Agent"
  },
  {
    "title": "Potpie-Ai/Potpie",
    "body": "Open Source AI Agents for your codebase in...",
    "tag": "Not available",
    "url": "https://potpie.ai?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Agent"
  },
  {
    "title": "Saplings",
    "body": "A framework for building agents that use search...",
    "tag": "Free",
    "url": "https://github.com/shobrook/saplings?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Agent"
  },
  {
    "title": "Mastraai",
    "body": "Mastra is an opinionated TypeScript framework...",
    "tag": "Free",
    "url": "https://github.com/mastra-ai/mastra?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI Agent"
  },
  {
    "title": "Notion Ai",
    "body": "AI-assisted note-taking software",
    "tag": "From $10/mo",
    "url": "https://www.notion.so?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Writing"
  },
  {
    "title": "Deep L Write",
    "body": "English and German writing tools to fix writing...",
    "tag": "Freemium",
    "url": "https://www.deepl.com/write?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Writing"
  },
  {
    "title": "Grammarly",
    "body": "Edit and correct your grammar, spelling, punctu...",
    "tag": "Freemium",
    "url": "https://app.grammarly.com?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Writing"
  },
  {
    "title": "Textcraft",
    "body": "Add-in for Microsoft Word that seamlessly...",
    "tag": "Free",
    "url": "https://github.com/suncloudsmoon/TextCraft?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Writing"
  },
  {
    "title": "Google Translate",
    "body": "Support text, picture, document and URL",
    "tag": "Free",
    "url": "https://translate.google.com?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Translation"
  },
  {
    "title": "Immersive-Translate",
    "body": "Open source project. Immersive bilingual web...",
    "tag": "Free",
    "url": "https://github.com/immersive-translate/immersive-translate?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Translation"
  },
  {
    "title": "Openai-Translator",
    "body": "Open source project. Crossword translation...",
    "tag": "Not available",
    "url": "https://github.com/yetone/openai-translator?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Translation"
  },
  {
    "title": "Azure Text To Speech",
    "body": "The best and most realistic voice tools currently...",
    "tag": "Freemium",
    "url": "https://speech.microsoft.com/portal/voicegallery?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Text To Speech"
  },
  {
    "title": "Hailuo Ai Text To Speech",
    "body": "Offer over 300 voices in 17 languages and...",
    "tag": "Not available",
    "url": "https://www.hailuo.ai/audio?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Text To Speech"
  },
  {
    "title": "Shazam",
    "body": "Download the shazaom app for music recognition,...",
    "tag": "Free",
    "url": "https://www.shazam.com?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Music Recognition"
  },
  {
    "title": "So-Vits-Svc",
    "body": "SoftVC VITS Singing Voice Conversion.",
    "tag": "Free",
    "url": "https://github.com/svc-develop-team/so-vits-svc?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Voice Processing"
  },
  {
    "title": "Mureka.Ai",
    "body": "Text to music",
    "tag": "Freemium",
    "url": "https://www.mureka.ai?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI generated music or sound effects"
  },
  {
    "title": "Elevenlabs/Sound-Effects",
    "body": "Imagine a sound and bring it to life, or explore...",
    "tag": "Free",
    "url": "https://elevenlabs.io/app/sound-effects?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI generated music or sound effects"
  },
  {
    "title": "Suno-Ai/Bark",
    "body": "Bark is a transformer-based text-to-audio model...",
    "tag": "Free",
    "url": "https://github.com/suno-ai/bark?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI generated music or sound effects"
  },
  {
    "title": "Audiocraft",
    "body": "Open source library for audio/music generation by...",
    "tag": "Free",
    "url": "https://github.com/facebookresearch/audiocraft?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "AI generated music or sound effects"
  },
  {
    "title": "Seamless",
    "body": "Seamless is a family of AI models that enable...",
    "tag": "Free",
    "url": "https://github.com/facebookresearch/seamless_communication?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Speech translation"
  },
  {
    "title": "Alphaxiv",
    "body": "An open academic discussion community based on...",
    "tag": "Free",
    "url": "https://www.alphaxiv.org?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "Academic research"
  },
  {
    "title": "Umi-Ocr",
    "body": "Comes with a highly efficient offline OCR engine....",
    "tag": "Free",
    "url": "https://github.com/hiroi-sora/Umi-OCR?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "OCR"
  },
  {
    "title": "Allenai/Olmocr",
    "body": "A toolkit for training language models to work...",
    "tag": "Free",
    "url": "https://github.com/allenai/olmocr?ref=riseofmachine.com",
    "date-added": "2025-06-13",
    "category": "OCR"
  }
]

category_mapping = {
    "ChatGPT and other AI chat assistant": "llm",
    "AI Search engine": "research",
    "Open Source LLMs": "llm",
    "LLM Leaderboard": "xtras",
    "Programming Development": "developer",
    "AI Image Creation": "art",
    "Video Creation": "video",
    "LLM Prompts": "prompts",
    "LLM training platform": "developer",
    "AI Agent": "llm",
    "Writing": "copywriting",
    "Translation": "productivity",
    "Text To Speech": "audio",
    "Music Recognition": "music",
    "Voice Processing": "audio",
    "AI generated music or sound effects": "music",
    "Speech translation": "audio",
    "Academic research": "research",
    "OCR": "productivity"
}
changes_made_count = 0
skipped_count = 0

for new_tool_data in new_tools_input:
    original_title = new_tool_data["title"]

    final_title = custom_title_case(original_title)
    final_body = format_body(new_tool_data["body"])

    source_category_name = new_tool_data["category"]
    target_category_key = category_mapping.get(source_category_name, "xtras")

    category_obj = next((cat for cat in tools_data_list if cat["category"] == target_category_key), None)

    if not category_obj:
        print(f"Warning: Target category key '{target_category_key}' for source '{source_category_name}' not found. Tool '{final_title}' skipped.")
        skipped_count += 1
        continue

    if "content" not in category_obj:
        category_obj["content"] = []

    is_duplicate = False
    for existing_tool in category_obj["content"]:
        if existing_tool["title"].lower() == final_title.lower() or existing_tool["url"] == new_tool_data["url"]:
            print(f"Info: Tool '{final_title}' (URL: {new_tool_data['url']}) already exists or has a conflicting title in category '{target_category_key}'. Skipping.")
            is_duplicate = True
            skipped_count +=1
            break
    if is_duplicate:
        continue

    # URL check - ensure it ends with ?ref=riseofmachine.com
    if not new_tool_data["url"].endswith("?ref=riseofmachine.com"):
        print(f"Warning: URL for tool '{final_title}' does not end with '?ref=riseofmachine.com'. Skipping. URL: {new_tool_data['url']}")
        skipped_count += 1
        continue

    tool_to_add = {
        "title": final_title,
        "body": final_body,
        "tag": new_tool_data["tag"],
        "url": new_tool_data["url"],
        "date-added": "2025-06-14"
    }

    category_obj["content"].append(tool_to_add)
    changes_made_count += 1

    category_obj["content"].sort(key=lambda x: x["title"].lower())
    # print(f"Success: Added tool '{final_title}' to category '{target_category_key}'.") # Reduced verbosity

data["tools"] = tools_data_list

with open("src/data/tools.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nProcessing complete. Added {changes_made_count} tools. Skipped {skipped_count} tools (duplicates, missing category, or invalid URL).")

try:
    with open("src/data/tools.json", "r", encoding="utf-8") as f:
        json.load(f)
    print("JSON validation successful.")
except json.JSONDecodeError as e:
    print(f"Error: Updated src/data/tools.json is not valid JSON. Details: {e}")
    exit(1)
