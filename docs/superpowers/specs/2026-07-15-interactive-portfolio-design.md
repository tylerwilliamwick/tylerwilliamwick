# Interactive Portfolio Design

## Goal

Replace the static hero graphic with a useful interactive product-system explorer and refine the one-page portfolio’s visual hierarchy without adding dependencies or changing its GitHub Pages hosting model.

## Chosen Direction

Use a code-native “Product Operating System” explorer with four stages: Frame, Align, Ship, and Learn. Each stage is a native `<details>` disclosure grouped with the same `name`, so mouse, touch, and keyboard users can reveal the methods and proof behind that stage without JavaScript. The first stage is open by default, and all content remains available when scripting is disabled.

Alternatives rejected:

- Image hotspots preserve the current visual but make the information harder to navigate with keyboards and small screens.
- A scroll-driven animated timeline creates more motion and code than the recruiter-scanning use case warrants.

## Page Structure

- Keep the sticky navigation, headline, proof points, evidence, skills, contact links, résumé, and current public URL.
- Replace the `<figure><img></figure>` hero asset with an interactive explorer immediately below the hero actions.
- Present the four stages as a responsive guided sequence. Each stage contains a concise purpose, representative methods, and one concrete output; the full-width order keeps the expanding content visually stable and reinforces the Frame-to-Learn progression.
- Remove the now-unused `public/portfolio-systems.png`; retain `public/og-image.png` for link previews.

## Visual Direction

- Preserve the teal, copper, ink, and warm-neutral palette while increasing contrast and depth.
- Use a restrained editorial style: stronger section rhythm, larger whitespace, softer 14–18px corners, subtle shadows, and a single accent rule rather than decorative imagery.
- Give cards and metrics consistent hover/focus elevation, without hiding essential information behind hover.
- Add restrained disclosure motion only when the user has not requested reduced motion.
- Preserve automatic dark mode and responsive layouts.

## Interaction and Accessibility

- Use semantic `<details>` and `<summary>` controls; no custom widget roles or JavaScript state.
- Supply visible focus rings, minimum touch-friendly targets, meaningful headings, and descriptive stage numbers.
- Keep the explorer fully usable at narrow widths and in dark mode.
- Respect `prefers-reduced-motion` and avoid parallax, autoplay, or pointer-only interactions.

## Validation

- Extend the existing static validator to assert that the image is gone, exactly four grouped explorer stages exist, one starts open, and the résumé/contact links remain intact.
- Run the validator against the deployable repository.
- Serve the site locally and verify desktop/mobile behavior in the in-app browser.
- Publish through the existing GitHub Pages workflow, wait for a successful deployment, and confirm the page, interactive markup, image preview, and résumé return HTTP 200 in production.

## Scope Boundary

This pass does not migrate frameworks, add analytics, add a CMS, create new case-study routes, or introduce animation libraries. Those changes do not improve the requested interaction enough to justify their maintenance cost.
