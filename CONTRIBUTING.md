# Contributing to Rise of Machine

### Getting Started

```bash
# Clone the repository
git clone https://github.com/NewDesignFile/template-directory.git
cd template-directory

# Create a new branch for your AI tool
git checkout -b add/your-ai-tool
```


### Adding a Tool
Tools data is stored in `src/data/tools.json`. This file contains all AI tools organized by category in alphabetical order.

Add your tool entry to the appropriate category in the JSON file. Make sure to place your entry in alphabetical order within its category. Each tool entry should follow this format:

```json
{
  "title": "Your AI Tool Name",
  "body": "A brief description.",
  "tag": "Pricing tag comes here.",
  "url": "https://your-ai-tool.com?ref=riseofmachine.com",
  "date-added": "YYYY-MM-DD"
}
```

Note: Always add `?ref=riseofmachine.com` to the end of your AI tool's URL.

### Creating a Pull Request
After adding your tool to the JSON file, submit your changes:

```bash
# Add and commit your changes
git add .
git commit -m "Add [Tool Name] to [Category]"

# Push to your branch
git push -u origin add/your-ai-tool
```

Then go to the [repository page](https://github.com/NewDesignFile/template-directory) and create a pull request.

### Guidelines
- Choose the most appropriate category for your tool.
- Make sure to place your entry in alphabetical order within its category.
- Don't create new categories yourself. If you don't find an appropriate category, add your tool under the "Xtras" category and suggest a new category by creating an issue.
- Keep the description concise and informative.
- For the pricing tag, choose one of: `Free` | `Freemium` | `From $X/mo` | `$X One-time` | `Not available`
- Make sure the URL includes the reference parameter: `?ref=riseofmachine.com`
- Include today's date in the "date-added" field.
- Verify your JSON syntax is valid before submitting.