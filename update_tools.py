import json

new_tools = [
    {
        "title": "Snoika",
        "body": "AI SEO tool for Google and AI search engines.",
        "url": "https://snoika.com/?ref=riseofmachine.com",
        "pricing_tag": "Contact for pricing",
        "category": "SEO"
    },
    {
        "title": "LiftPilot",
        "body": "AI-powered 1:1 landing page builder for outbound.",
        "url": "https://liftpilot.ai/?ref=riseofmachine.com",
        "pricing_tag": "Freemium",
        "category": "Marketing"
    },
    {
        "title": "StackGen",
        "body": "AI platform for autonomous cloud management.",
        "url": "https://stackgen.com/?ref=riseofmachine.com",
        "pricing_tag": "Freemium",
        "category": "Developer"
    },
    {
        "title": "Meet-Ting",
        "body": "Free AI assistant for email meeting scheduling.",
        "url": "https://meet-ting.com/?ref=riseofmachine.com",
        "pricing_tag": "Free",
        "category": "Productivity"
    },
    {
        "title": "Lock-in",
        "body": "AI focus assistant for optimizing attention.",
        "url": "https://lock-in.ai/?ref=riseofmachine.com",
        "pricing_tag": "Contact for pricing",
        "category": "Productivity"
    },
    {
        "title": "OpenWispr",
        "body": "Open-source, private AI voice dictation tool.",
        "url": "https://openwispr.com/?ref=riseofmachine.com",
        "pricing_tag": "Freemium",
        "category": "Audio"
    },
    {
        "title": "Rustic AI",
        "body": "AI-powered design editor for visuals.",
        "url": "https://rusticai.art/?ref=riseofmachine.com",
        "pricing_tag": "Freemium",
        "category": "Design"
    },
    {
        "title": "Nimt.ai",
        "body": "Track and boost brand visibility on AI platforms.",
        "url": "https://www.nimt.ai/?ref=riseofmachine.com",
        "pricing_tag": "Freemium",
        "category": "SEO"
    },
    {
        "title": "Droidrun",
        "body": "Open-source AI mobile app automation platform.",
        "url": "https://www.droidrun.ai/?ref=riseofmachine.com",
        "pricing_tag": "Freemium",
        "category": "Developer"
    },
    {
        "title": "Adtwin",
        "body": "AI platform for audio ad creation and tracking.",
        "url": "https://adtwin.ai/?ref=riseofmachine.com",
        "pricing_tag": "Freemium",
        "category": "Audio"
    },
    {
        "title": "Wan 2.2",
        "body": "AI video generator for professional videos.",
        "url": "https://wan22.studio/?ref=riseofmachine.com",
        "pricing_tag": "Paid",
        "category": "Video"
    },
    {
        "title": "Resea AI",
        "body": "AI research agent for academic research.",
        "url": "https://resea.ai/?ref=riseofmachine.com",
        "pricing_tag": "Freemium",
        "category": "Research"
    },
    {
        "title": "MuAPI",
        "body": "AI Image/Video API platform for rapid generation.",
        "url": "https://muapi.ai/?ref=riseofmachine.com",
        "pricing_tag": "Freemium",
        "category": "Photos"
    },
    {
        "title": "Veo Video",
        "body": "AI video generation platform from text/images.",
        "url": "https://veo-video.org/?ref=riseofmachine.com",
        "pricing_tag": "Freemium",
        "category": "Video"
    },
    {
        "title": "Clothes Changer",
        "body": "Transform your look with AI Clothes Changer.",
        "url": "https://www.clothes-changer.com/?ref=riseofmachine.com",
        "pricing_tag": "Free",
        "category": "Photos"
    },
    {
        "title": "Hairstyle",
        "body": "Discover your perfect hairstyle with AI.",
        "url": "https://www.aihairstyle.design/?ref=riseofmachine.com",
        "pricing_tag": "Free",
        "category": "Photos"
    },
    {
        "title": "Sniff Job",
        "body": "AI-powered job search assistant.",
        "url": "https://sniffjob.com/?ref=riseofmachine.com",
        "pricing_tag": "Freemium",
        "category": "Enterprise"
    },
    {
        "title": "Fiddl.art",
        "body": "AI art generator for custom models and earning.",
        "url": "https://fiddl.art/?ref=riseofmachine.com",
        "pricing_tag": "Freemium",
        "category": "Art"
    },
    {
        "title": "Insights by Coupler.io",
        "body": "Data integration, reporting, and AI insights.",
        "url": "https://www.coupler.io/ai-insights?ref=riseofmachine.com",
        "pricing_tag": "Freemium",
        "category": "Enterprise"
    },
    {
        "title": "Wan 2.2 AI",
        "body": "Professional AI platform for video generation.",
        "url": "https://wan22.ai/?ref=riseofmachine.com",
        "pricing_tag": "Freemium",
        "category": "Video"
    },
    {
        "title": "Chat Agents",
        "body": "No-code platform to create AI Chatbots.",
        "url": "https://www.chatagents.io/?ref=riseofmachine.com",
        "pricing_tag": "Freemium",
        "category": "Enterprise"
    }
]

with open('src/data/tools.json', 'r+') as f:
    data = json.load(f)
    for new_tool in new_tools:
        for category in data['tools']:
            if category['category'].lower() == new_tool['category'].lower():
                # Fix the key for pricing_tag to tag
                new_tool['tag'] = new_tool.pop('pricing_tag')
                # Add date-added
                new_tool['date-added'] = '2025-07-31'
                # remove category from new_tool
                del new_tool['category']
                category['content'].append(new_tool)
                category['content'].sort(key=lambda x: x['title'])
                break
    f.seek(0)
    json.dump(data, f, indent=2)
    f.truncate()
