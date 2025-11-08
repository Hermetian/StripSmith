# Stripsmith Quickstart Guide

Get your first AI-generated comic in 5 minutes!

## Prerequisites

- Python 3.12+
- OpenAI API key (DALL-E 3)
- Anthropic API key (Claude)

## 1. Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

## 2. Configure API Keys

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your keys:
# OPENAI_API_KEY=your-openai-key-here
# ANTHROPIC_API_KEY=your-anthropic-key-here
```

## 3. Test Your Setup

```bash
python scripts/generate_comic.py test
```

You should see:
```
Testing Claude API...
  ✓ Claude API connected
Testing OpenAI API...
  ✓ OpenAI API connected
```

## 4. Generate Your First Comic!

We've included a sample story. Let's turn it into a comic:

```bash
python scripts/generate_comic.py data/stories/sample_story.txt \
  --style "noir comic, high contrast" \
  --format pdf
```

### What Happens:

1. **Story Analysis** (30 sec) - Claude extracts chapters, characters, scenes
2. **Character Sheets** (~$0.50, 2 min) - Generates reference art for each character
3. **Panel Breakdown** (1 min) - Claude breaks story into comic panels
4. **Image Generation** (~$1.50, 5 min) - DALL-E 3 creates each panel
5. **Composition** (30 sec) - Assembles panels into pages
6. **Export** (10 sec) - Creates final PDF

**Total time:** ~10 minutes
**Total cost:** ~$2.00

Your comic will be saved to: `data/output/sample_story.pdf`

---

## 5. Use Your Own Story

Create a text file with your story:

```
data/stories/my_story.txt
```

**Tips for best results:**
- Use clear chapter breaks
- Include detailed character descriptions
- Separate dialogue with quotation marks
- Describe settings visually

Then generate:

```bash
python scripts/generate_comic.py data/stories/my_story.txt \
  --style "your preferred art style" \
  --output data/output/my_comic \
  --format pdf
```

---

## Common Commands

### Analyze story only (no image generation):
```bash
python scripts/generate_comic.py my_story.txt --analyze-only
```

Review the analysis in `data/temp/project_spec.json`

### Generate character sheets only:
```bash
python scripts/generate_comic.py my_story.txt --characters-only
```

Review character sheets in `data/temp/character_sheets/`

### Generate specific chapters:
```bash
python scripts/generate_comic.py my_story.txt --chapters 1-2
```

### Export as images instead of PDF:
```bash
python scripts/generate_comic.py my_story.txt --format png
```

---

## Art Style Examples

Try these styles with `--style`:

**Comic Book Styles:**
- `"superhero comic, vibrant colors, dynamic poses"`
- `"noir comic, high contrast black and white"`
- `"manga, detailed linework, screentones"`
- `"European BD, ligne claire style"`
- `"indie comic, sketchy style, muted colors"`

**Genre-Specific:**
- `"cyberpunk comic, neon colors, futuristic"`
- `"western comic, sepia tones, dusty desert"`
- `"horror comic, dark shadows, gothic style"`
- `"fantasy comic, detailed backgrounds, epic scale"`

---

## Cost Breakdown

**Per comic (30 panels):**
- Character sheets (9 images): $0.36
- Panels (30 images): $1.20
- Claude API calls: $0.05
- **Total: ~$1.60**

**Cost-saving tips:**
- Use `--analyze-only` first to review before generating
- Generate `--characters-only` to check quality
- Process `--chapters 1` first as a test
- Standard quality is usually fine (HD costs 2x)

---

## Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure `.env` file exists in project root
- Check that you copied from `.env.example`
- Verify your API key is valid

### "API test failed"
- Check your API keys are correct
- Ensure you have credits in your OpenAI account
- Try the keys directly in OpenAI/Anthropic playgrounds

### Character consistency issues
- Review character sheets first with `--characters-only`
- Add more physical details to character descriptions
- Keep ≤3 characters per panel

### Generated panels look wrong
- Check `data/temp/chapter_X_panels.json` for panel descriptions
- Try different `--style` keywords
- Use more visual descriptions in your story

---

## Next Steps

1. **Write better stories** - Focus on visual descriptions
2. **Experiment with styles** - Try different art styles
3. **Edit intermediate files** - Manually adjust `project_spec.json` or panel breakdowns
4. **Batch process** - Generate multiple chapters separately

---

## Configuration

Edit `config/config.yaml` to customize:
- Image sizes and quality
- Panel layouts
- Speech bubble settings
- Cost limits

---

**Ready to create amazing comics!** 🎨📚

For full documentation, see [README.md](README.md)
