---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
---

# Frontend Design Skill

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.
- **Constraints**: Technical requirements (framework, performance, accessibility)
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:

### Typography
Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt for distinctive choices. Pair a distinctive display font with a refined body font.

**Good choices**: Space Grotesk, Clash Display, Satoshi, Cabinet Grotesk, General Sans, Outfit, Syne, Manrope, Plus Jakarta Sans, DM Sans, Bricolage Grotesque, Instrument Sans

**For display/headers**: Playfair Display, Fraunces, Bebas Neue, Archivo Black, Anton, Oswald, Montserrat

### Color & Theme
Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.

Example color strategy:
```css
:root {
  --bg-primary: #0a0a0a;
  --text-primary: #fafafa;
  --accent: #ff3366;
  --accent-subtle: rgba(255, 51, 102, 0.1);
}
```

### Motion
Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments with staggered reveals (animation-delay) and scroll-triggering hover states.

```css
/* Staggered animation example */
.item { animation: fadeUp 0.6s ease-out forwards; opacity: 0; }
.item:nth-child(1) { animation-delay: 0.1s; }
.item:nth-child(2) { animation-delay: 0.2s; }
.item:nth-child(3) { animation-delay: 0.3s; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### Spatial Composition
Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.

### Backgrounds & Visual Details
Create atmosphere and depth. Add contextual effects and textures:
- Gradient meshes
- Noise textures
- Geometric patterns
- Layered transparencies
- Dramatic shadows
- Decorative borders
- Custom cursors
- Grain overlays

## What to Avoid

NEVER use:
- Generic AI-generated aesthetics
- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliched color schemes (purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character
- Rounded corners on everything with soft shadows (the "corporate SaaS" look)
- Blue/purple gradient buttons
- Generic hero sections with stock imagery

## Implementation Approach

### For HTML/CSS projects:
1. Use semantic HTML5
2. Modern CSS (Grid, Flexbox, custom properties)
3. Mobile-first responsive design
4. Include Google Fonts links for typography
5. Add subtle animations and hover effects

### For React projects:
1. Use functional components with hooks
2. Consider Tailwind CSS or styled-components
3. Use Framer Motion for animations
4. Create reusable, composable components
5. Implement proper state management

### For Vue/Svelte/other frameworks:
1. Follow framework best practices
2. Use scoped styles
3. Implement proper reactivity patterns

## Output Format

When creating frontend code:

1. **First**: Describe the design concept and aesthetic direction in 2-3 sentences
2. **Then**: Provide complete, production-ready code
3. **Finally**: Note any setup requirements (fonts, dependencies, etc.)

## Key Principle

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Elegance comes from executing the vision well.

Remember: You are capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same.
