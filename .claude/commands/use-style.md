---
description: Apply a style from the style library to generate an image
allowed-tools: Read, Bash, Glob, Grep
---

# Use Style from Library

Apply style #$ARGUMENTS to generate an image.

## Instructions

1. Read the style library at `/Users/lance/Documents/claude-code-course/lesson-modules/3-nano-banana/3.1-intro-to-image-gen/3.1.4-style-database/style-library.html`

2. Parse the `styles` array in JavaScript and find the style with the matching ID number

3. Extract the `prompt` field from that style

4. If the user provided a subject after the style number (e.g., `/use-style 125 sunset over mountains`), combine the style prompt with their subject

5. Generate the image using the style's prompt via image_gen.py:
   ```
   cd /Users/lance/Documents/claude-code-course/lesson-modules/3-nano-banana && python3 image_gen.py "[combined prompt]"
   ```

6. Return the path to the generated image and offer to open it

## Example Usage

- `/use-style 125` - Shows the style details and asks what to generate
- `/use-style 125 data visualization of user growth` - Generates using style #125 with that subject
- `/use-style 130 sankey diagram of music genres` - Generates a Sankey in style #130
