# Evidence-First Portfolio Design

## Goal

Replace the live portfolio's banking- and RFP-oriented positioning with a concise, evidence-first one-pager that matches the linked resume: civic-platform product leadership, GIS, AI-assisted discovery, platform continuity, and measurable delivery outcomes.

## Chosen Direction

Implement the approved **Direction 1: Evidence-first targeted one-pager** from the July 16 portfolio audit. Preserve the dependency-free GitHub Pages architecture and current editorial visual language, but change the scan order to:

1. Hero
2. Metric strip
3. Three compact cases
4. Relevant capabilities
5. Contact

The case-study direction is deferred until publishable source material exists. The two-track banking/GovTech direction is rejected for now because it would preserve the credibility split and duplicate upkeep.

## Evidence Boundary

`public/resume.pdf` is the source of truth. The page may state only claims supported there.

Featured proof:

- `350+` government agencies covered by the ArcGIS Enterprise compatibility program.
- A `0-to-1` Rapid Damage Assessment launch shaped through AI-assisted discovery with about 30 agencies and about 150 interviews.
- `121` customers and `$2.17M ARR` retained through the legacy CRM end-of-life program.

The resume also supports a 50% implementation time-and-cost reduction and 97% API migration conversion, but this page will omit them rather than create extra cases or detach metrics from their evidence.

Remove unsupported or misleading claims, including digital banking, BECU, member workflows, RFP cycles, four-team roadmap ownership, customer wins, recurring C-suite readouts, pen-test-style reviews, Claude/Codex workflows, 23-vendor analysis, and AI-assisted product operations. Poynt supports payments experience, not digital-banking or member-product positioning.

Align the repository's public profile `README.md` to the same civic-platform/GIS story. Leave the resume PDF unchanged.

## Page Structure

### Hero

- Position Tyler as a senior product manager for civic platforms, GIS, and AI-assisted product discovery.
- Use one concise value proposition grounded in platform modernization and government customers.
- Provide exactly two actions: `Selected work` and `Resume PDF`.
- Keep email, LinkedIn, and GitHub in Contact and the footer area.

### Metric Strip

- Place three linked metrics immediately below the hero.
- Link each metric to its corresponding case so proof is not detached from context.
- Use `350+ agencies`, `0-to-1 launch`, and `$2.17M ARR retained`.

### Selected Work

Use exactly three compact, non-clickable case articles. Each contains the visible labels `Context`, `My role`, `Decision`, and `Outcome`.

1. **ArcGIS compatibility at scale**
   - Context: ArcGIS Enterprise upgrades affected Civic Platform integrations and 350+ active customers.
   - My role: directed the upgrade posture.
   - Decision: coordinate compatibility analysis, endpoint validation, customer communications, and rollout planning.
   - Outcome: a compatibility program spanning 350+ government agencies; do not imply adoption or revenue not stated in the resume.
2. **Rapid Damage Assessment**
   - Context: government agencies needed a new damage-assessment solution.
   - My role: drove go-to-market and AI-assisted discovery with about 30 agencies and about 150 interviews.
   - Decision: shape a spatial-first emergency-response product.
   - Outcome: a successful 0-to-1 launch and early customer onboarding.
3. **Legacy CRM end-of-life**
   - Context: retiring the legacy CRM put customer continuity and recurring revenue at risk.
   - My role: headed the program and secured executive and board approval.
   - Decision: execute the transition through about 15 features across 12 epics, 100+ defect fixes, and management of about 50 customer incidents.
   - Outcome: 121 customers and $2.17M ARR retained.

### Relevant Capabilities

Use one compact section covering only resume-backed capabilities: GIS/ArcGIS, AI-assisted discovery, product strategy and roadmapping, go-to-market, discovery interviews and user research, Agile delivery, stakeholder and executive communication, API integration, workflow automation, customer onboarding, and revenue retention. Lead with business capabilities, not tool names.

### Contact

Invite relevant senior product conversations in civic technology, government software, GIS-enabled platforms, and adjacent platform roles. Preserve email, resume, LinkedIn, and GitHub links.

## Visual and Interaction Direction

- Keep the teal, copper, ink, warm-neutral palette, responsive grid, automatic dark mode, and editorial typography.
- Delete the product-system explorer and its CSS instead of repairing or demoting it.
- Merge Proof, Evidence, and Skills into Metrics, Selected Work, and Relevant Capabilities.
- Remove hover elevation from non-interactive cards. Retain clear hover and focus states on links and buttons.
- Add no JavaScript, framework, analytics, CMS, animation library, or new runtime/build dependency.

## Accessibility and Reflow

- Add a keyboard-visible skip link targeting the main content.
- Use labelled semantic sections, a list for metrics, and articles for cases.
- Preserve visible focus and reduced-motion handling.
- Make the navigation static and wrappable on narrow screens.
- Add anchor scroll margins and allow long button text to wrap.
- Verify keyboard flow, 320 CSS pixels, and 200% zoom. The static validator cannot prove visual reflow.

## Metadata and Assets

- Add a canonical URL, favicon, `og:type`, `og:url`, absolute social-image URLs, and social-image width, height, and alt metadata.
- Regenerate `public/og-image.png` so its visible text matches the evidence-first civic-platform positioning and featured metrics.
- Add one small `public/favicon.svg`; do not add an icon package.

## Validation

Extend the existing Python standard-library validator before editing the page. It must initially fail against the interactive baseline, then pass only when the deployable repository has:

- no explorer or grouped disclosures;
- section order `outcomes`, `cases`, `capabilities`, `contact`;
- three metrics linked to three case IDs;
- exactly three case articles, each with all four evidence labels;
- exactly two hero actions;
- a skip link targeting an existing ID;
- aligned resume, email, LinkedIn, GitHub, canonical, favicon, and social metadata;
- no unsupported banking, BECU, member, or RFP copy;
- the resume, favicon, and social image assets present;
- reduced-motion support retained.

Also run whitespace checks, serve the page locally, inspect desktop and mobile layouts, test keyboard interaction and 200% zoom, and inspect the regenerated social preview. Publishing or merging remains a separate explicit finish choice; do not push automatically.

## Scope Boundary

Do not create full case-study routes, rewrite the resume, add analytics, add a CMS, migrate frameworks, introduce JavaScript, or create a banking track. Those changes require evidence or maintenance that this pass does not need.
