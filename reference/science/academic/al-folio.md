===
academic_portfolio: al-folio, jekyll, responsive
===
A beautiful academic portfolio showcasing research, publications, and projects.

@metadata:
- title: Your Name
- tagline: PhD Student / Researcher / Professor
- description: Brief bio or research interests
- keywords: machine learning, computer vision, your field

@theme: minimal, academic
Color scheme: clean whites with accent color
Typography: professional, readable
Features: dark mode, responsive, fast

--
about: page, landing
--
Professional headshot or avatar

Brief introduction paragraph about your research interests and current position. Keep it concise but engaging.

@news: recent, highlighted
- **Jan 2025** Paper accepted at Conference Name!
- **Dec 2024** Released new dataset on GitHub
- **Nov 2024** Started internship at Lab Name

@social: professional
- github: username
- google-scholar: scholar_id  
- orcid: 0000-0000-0000-0000
- twitter: optional
- email: encrypted

--
publications: page, bib
--
@filtering: by-year, by-type
@style: ieee, apa, chicago

@paper: featured
```bib
@inproceedings{yourname2025,
  title={Amazing Research Title},
  author={Your Name and Collaborator},
  booktitle={Top Conference},
  year={2025},
  selected={true}
}
```

@paper: workshop
Include all publications from your .bib file

@assets: organized
- `/papers/2025_conference_paper.pdf`
- `/slides/2025_conference_slides.pdf`
- `/posters/2025_conference_poster.pdf`

--
projects: page, grid
--
@project: featured, ongoing
**Project Title**
Brief description with hero image
[Code](github.com/user/repo) | [Demo](demo.url) | [Paper](paper.pdf)
- Key feature 1
- Key feature 2
- Impact statement

@categories: filterable
- Machine Learning
- Computer Vision  
- Open Source
- Course Projects

@layout: cards, responsive
3 columns on desktop, 1 on mobile
Hover effects showing more details

--
teaching: page, timeline  
--
@course: instructor
**CS101: Introduction to Programming**
*Fall 2024, Spring 2025*
- Students: 150
- Rating: 4.8/5.0
- [Materials](course-website.url)

@course: teaching-assistant
**CS501: Advanced Machine Learning**
*Spring 2024*
- Designed new lab assignments
- Held weekly office hours
- [Student feedback](feedback.pdf)

--
cv: page, pdf-ready
--
@sections: standard-academic
- Education
- Research Experience
- Publications
- Teaching
- Awards & Honors
- Talks & Presentations
- Service
- Skills

@formatting: latex-style
Clean, professional, ATS-friendly
Auto-generated from site content
Downloadable PDF version

--
blog: optional, technical
--
@post: tutorial
**How to Implement [Algorithm]**
Step-by-step guide with code snippets
Interactive demos using Observable/D3.js

@post: research-explainer  
**Our Recent Paper Explained**
Accessible summary for broader audience
Key insights and implications

@features:
- Math support (KaTeX)
- Code highlighting  
- Jupyter notebook integration
- Comments via utterances

--
deployment: github-pages, custom-domain
--
@setup: automated
```bash
winding al-folio-setup --github username/username.github.io
winding al-folio-update --section publications
```

@optimizations:
- Lazy loading images
- Minified CSS/JS
- SEO optimized
- Analytics ready

@maintenance: low
- Update via markdown/winding
- Auto-rebuild on push
- No database needed

--
high_school_version: simplified
--
For ambitious high schoolers:

@sections: age-appropriate
- About Me
- Science Fair Projects
- Coursework
- Volunteer Work
- College Goals

@features: same-quality
Professional appearance for college apps
Easy to maintain through high school
Grows with the student

@examples:
```bash
winding portfolio --template high-school --name "Jane Doe"
winding portfolio --add-project "Robot Competition Winner"
winding portfolio --generate-pdf --college-app
```