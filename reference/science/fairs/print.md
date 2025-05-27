---
science_fair_print: tool, python, service
---
Transforms science fair windings into physical artifacts via print services.

--
print_photos: command, api
--
Extract all visual elements and send to photo printing service.

@extraction:
- Parse winding for images, charts, tables
- Convert tables/calculations to high-res images
- Add margins for clean cutting
- Generate QR codes for interactive elements

@sizing:
- 4x6: default for poster elements
- 5x7: featured images, main chart
- 8x10: title card, hypothesis
- Custom: based on @size argument

@services:
- walgreens: via API or selenium
- cvs: photo API
- local: PDF for self-printing
- api.wind.kids: managed service

@layout_hints:
Each photo gets a companion hint card:
```
IMG_001_hypothesis.jpg → "Top center of board"
IMG_002_procedure.jpg → "Left panel, under materials"
```

@usage:
```bash
science_print dragon_wingsuit.md --service walgreens --store 94086
science_print experiment.md --size 4x6,8x10 --copies 2
science_print project.md --api wind.kids --rush
```

--
photobook: command, pdf
--
Transform science fair project into keepsake book.

@layout_engine:
- Title page with student photo
- Project overview spread
- Step-by-step procedure pages
- Results with full data visualization
- Conclusion and learnings
- Behind-the-scenes photos
- Judge feedback page (blank template)

@formats:
- 8x8: Instagram-friendly square
- 8.5x11: Standard, economical  
- 11x14: Premium presentation

@print_ready:
- Bleeds and margins for pro printing
- PDF/X compatible
- Embedded fonts
- Color profiles

@themes:
- scientific: clean, journal-style
- fun: colorful, kindergarten-friendly
- prestigious: thesis-style, serious

@usage:
```bash
science_book dragon_wingsuit.md --format 8x8 --theme fun
science_book research.md --format 11x14 --theme prestigious --isbn
```

--
api_service: hosted, scalable
--
api.wind.kids or api.articoder.com endpoint.

@endpoints:
```
POST /science/print
  body: winding content
  params: service, size, rush
  returns: order_id, pickup_info

POST /science/book  
  body: winding content
  params: format, theme
  returns: pdf_url, preview_url

GET /science/status/:order_id
  returns: status, tracking, eta
```

@features:
- Parental approval workflow
- Bulk school discounts
- Science fair deadline awareness
- Quality preview before printing

@integration:
```python
# In the winding tool
illuminate science_fair.md --print --service wind.kids
illuminate project.md --book --format 8x8 --order

# Or via API
from winding import science_fair_print
order = science_fair_print.photos("dragon.md", size="4x6")
print(f"Pick up at Walgreens: {order.location}")
```

--
smart_features:
--
Beyond basic printing:

@poster_optimizer:
- Detect standard tri-fold dimensions
- Suggest photo arrangements
- Generate cutting guides
- "Too much text" warnings

@parent_helper:
- Shopping list: posterboard, glue, markers
- Timeline: "Order by Tuesday for Friday fair"
- Cost estimate before ordering

@judge_mode:
- QR code for digital appendix
- AR markers for phone visualization
- "Scan for video demonstration"

@batch_processing:
```bash
# Teacher processes entire class
science_print class/*.md --school "Lincoln Elementary" --bulk_discount
```

--
example_winding:
--
What the tool processes:

```markdown
---
dragon_wingsuit: science_fair, grade_1
---
Can I fly with dragon wings?

@hypothesis:
If I use a 9.2m² wing, I might glide!

@materials: !photo
- Wing 5m²
- Wing 9.2m²  
- Harness
- Pilot (22kg)

@procedure: grid[2,2]
1. Calculate lift needed
2. Test small wing
3. Test large wing
4. Measure results

@results: chart, prominent
!["Wing Size vs Jump Distance"](results_chart.png)

@math: table
| Mass | 22 kg |
| Speed | 4 m/s |
| Lift needed | 216 N |

@conclusion: callout
9.2m² not enough. Need 20m²!
```

Outputs:
- 6 photos (4x6) for poster
- 1 chart (8x10) 
- 1 photo book (8x8)