# Winding Production System - Flat Architecture

## The Actual Flow

```
┌─────────────────── CONTEXT WINDOW ─────────────────────┐
│                                                         │
│  📄 current.winding.md                                  │
│  "The dragon guards the ancient gate..."               │
│                                                         │
│  🖼️ previous_page.jpg (optional)                       │
│  Shows: dragon with golden eyes                        │
│                                                         │
│  📄 style.winding.md (optional)                        │
│  Generated by style_supervisor or hand-written         │
│                                                         │
│  🖼️ character_ref.png (optional)                       │
│  Checkpointed from earlier good result                 │
│                                                         │
└────────────────────┬───────────────────────────────────┘
                     │
                     ▼
┌─────────────── ILLUMINATION ───────────────────────────┐
│                                                         │
│  The AI reads everything in context and generates:     │
│                                                         │
│  🖼️ current_page.jpg                                   │
│                                                         │
└────────────────────┬───────────────────────────────────┘
                     │
                     ▼
┌─────────────── SUPERVISION (Optional) ─────────────────┐
│                                                         │
│  👁️ invoke spelling_supervisor                          │
│  👁️ invoke consistency_supervisor                      │
│  👁️ invoke style_supervisor                            │
│                                                         │
│  Output: errors.md AND/OR generated.winding.md         │
│                                                         │
└────────────────────┬───────────────────────────────────┘
                     │
                     ▼
┌─────────────── USER DECISION ──────────────────────────┐
│                                                         │
│  ✓ Checkpoint good results                             │
│  ✓ Checkpoint useful windings                          │
│  ✗ Discard and retry                                   │
│  → Continue to next page                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Supervisor-Generated Windings

When supervisors analyze artifacts, they can output windings:

### Consistency Supervisor → Character Winding
```
┌─── INPUT TO SUPERVISOR ────┐    ┌─── SUPERVISOR OUTPUT ────┐
│ • dragon_pages_1-5.jpg     │    │ dragon_facts.winding.md: │
│ • original.winding.md      │ →  │ ---                      │
│ • "Extract dragon facts"   │    │ dragon: character_sheet  │
│                            │    │ ---                      │
└────────────────────────────┘    │ @eyes: golden            │
                                  │ @scales: emerald         │
                                  │ @size: massive           │
                                  │ @personality: wise       │
                                  └──────────────────────────┘
```

### Style Supervisor → Style Guide Winding
```
┌─── INPUT TO SUPERVISOR ────┐    ┌─── SUPERVISOR OUTPUT ────┐
│ • all_pages/*.jpg          │    │ project_style.winding.md │
│ • "Extract visual style"   │ →  │ ---                      │
│                            │    │ style: guide             │
└────────────────────────────┘    │ ---                      │
                                  │ @palette: earth_tones    │
                                  │ @technique: watercolor   │
                                  │ @lighting: soft_diffuse  │
                                  └──────────────────────────┘
```

### Story Supervisor → Scene Index Winding
```
┌─── INPUT TO SUPERVISOR ────┐    ┌─── SUPERVISOR OUTPUT ────┐
│ • chapter1/*.winding.md    │    │ chapter1_index.winding.md│
│ • chapter1/*.jpg           │ →  │ ---                      │
│ • "Create scene index"     │    │ index: chapter_1         │
└────────────────────────────┘    │ ---                      │
                                  │ @scene_1: intro          │
                                  │ Dragon first appears     │
                                  │                          │
                                  │ @scene_2: the_meeting    │
                                  │ Hero meets dragon        │
                                  └──────────────────────────┘
```

## The Checkpoint System

```
working_directory/
├── current.winding.md
├── illuminated/
│   ├── page_1_v1.jpg
│   ├── page_1_v2.jpg
│   └── page_1_v3.jpg
└── checkpoints/
    ├── page_1_final.jpg ✓
    ├── dragon_ref.jpg ✓
    ├── style_guide.winding.md ✓
    └── character_sheets.winding.md ✓
```

## Flat Context Building

Each new illumination just picks what to include:

```bash
# Minimal context
illuminate page_2.winding.md

# With previous page
illuminate page_2.winding.md --context page_1_final.jpg

# With style guide
illuminate page_2.winding.md --context style_guide.winding.md

# Kitchen sink (for complex scenes)
illuminate climax.winding.md --context checkpoints/*
```

## Why This Works

1. **No Hidden State**: Everything is explicit in the context window
2. **User Control**: You choose what context to include
3. **Supervisor as Tool**: Generates helpful windings, not mandates
4. **Checkpoint Freedom**: Save what works, discard what doesn't
5. **Natural Workflow**: Matches how AI copilots already work

## Practical Copilot-Mode Example

```markdown
User: "Check these 5 dragon images for consistency" 

Agent:
- *Analyzing images...*
- *Comparing with original winding...*
- I've found some inconsistencies. *Generating report...*
- Here's the report:
  ---
  goldscale.consistency.report.md
  ---
  # Consistency Report for Goldscale Dragon
  ## Summary
  - **Eyes**: Should be amber-gold on ![Flight Test](flight_test.png) and ![Guarding the Gate](guarding_gate.png) images, as per [Goldscale](goldscale.md).
  - **Size**: Inconsistent size on ![Flight Test](flight_test.png), conflicts with the established size the "comparable to a small house" in [Guarding the Gate](guarding_gate.md).

  ## Unique Features Discovered
  - Scar above left eye, slightly visible on ![Wiser dragon](wiser_dragon.png).

  ## Posture Observations
  - The dragon is facing left on *all* images, which could be an artifact of the style guide.

  No other inconsistencies found.

- *Would you like me to checkpoint Goldscale, correct the eyes on ![Flight Test](flight_test.png) and redo ![Guarding the Gate](guarding_gate.png)?*
```

## Practical Supervisor Agent Example
```markdown






## The Beauty of Flatness

- **What You See Is What You Get**: No hidden production memory
- **Mix and Match**: Combine any artifacts/windings as context
- **Supervisor Products**: Generated windings are just helpful artifacts
- **Version Control Friendly**: Everything is files
- **Agent-Mode Natural**: Copilots already work this way

The system is just:
1. Files (windings and artifacts)
2. Context (what you choose to include)
3. Tools (supervisors that can generate more files)
4. Checkpoints (files you choose to keep)

That's it. Flat, simple, powerful.
