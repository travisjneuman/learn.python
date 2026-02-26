# Community Growth & Distribution Strategy

## Audit Report for learn.python

**Date:** 2026-02-25
**Scope:** Launch strategy, distribution channels, partnerships, monetization, and a 90-day playbook to grow from private repo to thriving open-source educational community.

---

## Table of Contents

1. [Current State Assessment](#1-current-state-assessment)
2. [Competitive Landscape: How Others Grew](#2-competitive-landscape-how-others-grew)
3. [GitHub SEO & Repository Optimization](#3-github-seo--repository-optimization)
4. [Reddit & Hacker News Strategy](#4-reddit--hacker-news-strategy)
5. [Social Media Strategy](#5-social-media-strategy)
6. [YouTube & Video Content Strategy](#6-youtube--video-content-strategy)
7. [Contributor Pipeline](#7-contributor-pipeline)
8. [Community Partnerships](#8-community-partnerships)
9. [Conference & Speaking Strategy](#9-conference--speaking-strategy)
10. [Localization Strategy](#10-localization-strategy)
11. [Monetization Models](#11-monetization-models)
12. [Metrics & Tracking](#12-metrics--tracking)
13. [90-Day Launch Playbook](#13-90-day-launch-playbook)

---

## 1. Current State Assessment

### Strengths

- **Massive scope:** 246 projects, 50+ curriculum docs, 16 concept guides, 15 quizzes, 16 flashcard decks, 30 coding challenges. This is a genuinely large, well-structured body of work.
- **Complete beginner path:** The "what is a terminal?" to "deploy to production" pipeline is rare. Most resources assume you already know something.
- **Project-first pedagogy:** Not a reference manual or lecture series. Every level produces tangible artifacts.
- **Expansion modules:** 12 real-world technology modules (web scraping, FastAPI, Django, Docker, cloud deploy) give practical skills beyond pure Python.
- **Strong README:** Clear value proposition, badges, navigation, quick start. Competitive with top educational repos.
- **CONTRIBUTING.md and CODE_OF_CONDUCT.md:** Already present, lowering the barrier for community contributions.
- **GitHub Discussions:** Enabled (per README audit files).
- **Issue templates:** Bug reports, feature requests, curriculum feedback templates in place.
- **MIT License:** Maximally permissive, removes adoption friction.

### Weaknesses

- **Zero distribution:** The repo exists but has no audience, no stars, no external awareness.
- **No social media presence:** No Twitter/X, LinkedIn, YouTube, or blog presence tied to the project.
- **No community channels:** No Discord server, no forum beyond GitHub Discussions.
- **Single maintainer:** All content created by one person. No contributor history, no proof of community.
- **No social proof:** No testimonials, no "I completed this" stories, no case studies.
- **No video companion:** In a market where Fireship, Corey Schafer, and Tech With Tim dominate Python education on YouTube, there is no video presence.

### Opportunity Size

The Python education market is enormous:
- r/learnpython has 951K+ members
- r/Python has 1.4M+ members
- "learn python" is one of the most searched programming queries globally
- Comparable repos (30-Days-Of-Python, 100-Days-Of-Code) have 30K-40K+ stars
- freeCodeCamp's GitHub repo has 400K+ stars
- The demand for free, structured, project-based Python education far exceeds supply

---

## 2. Competitive Landscape: How Others Grew

### freeCodeCamp (400K+ GitHub stars, 40K+ graduates hired)

**What worked:**
- Free, interactive, browser-based curriculum with certificates
- Strong community Discord and forum
- YouTube channel (9M+ subscribers) driving awareness back to the platform
- Open-source ethos attracted massive contributor base
- Quincy Larson's personal brand and consistent content marketing
- Strong SEO: "learn to code for free" rankings

**Lesson for learn.python:** The YouTube-to-GitHub pipeline is the single most powerful growth channel for educational repos. freeCodeCamp's YouTube channel predates much of its growth.

### The Odin Project (est. 2013, 30K+ GitHub stars)

**What worked:**
- "Read the docs" philosophy mirrors real developer work
- Community Discord is the primary support channel (100K+ members)
- Word-of-mouth from graduates who got jobs
- Integration with freeCodeCamp expanded reach
- Clear curriculum path with no ambiguity about "what's next"

**Lesson for learn.python:** The Discord community is often more important than the curriculum itself. People stay for the community, not the docs. learn.python's "follow the Next link" navigation is directly comparable.

### Exercism (57 languages, mentorship model)

**What worked:**
- Unique mentorship model where experienced developers review learner solutions
- Language-agnostic platform attracted polyglot developers
- Clean, modern web UI for submissions and feedback
- Strong partnership with language communities

**Lesson for learn.python:** A mentorship layer on top of the curriculum could differentiate learn.python from other repos.

### Boot.dev (~10K weekly active users)

**What worked:**
- Gamification (leagues, badges, streaks)
- Backend-focused niche (less competition than general "learn to code")
- YouTube channel (ThePrimeagen partnership, Lane Wagner's content)
- AI mentor integration (GPT-4o / Claude 3.5 Sonnet)
- Fantasy RPG theme creates emotional engagement

**Lesson for learn.python:** Gamification and AI integration are table stakes for modern learning platforms. Boot.dev's niche focus (backend) is comparable to learn.python's Python-only focus.

### 30-Days-Of-Python (Asabeneh, 35K+ stars)

**What worked:**
- Challenge-based format ("30 days") creates urgency and social sharing
- Simple, approachable scope (30 days vs. "complete curriculum")
- YouTube companion videos
- Strong representation in African developer communities

**Lesson for learn.python:** The "challenge" framing is powerful for social sharing. A "30-day Python challenge" subset of learn.python could serve as a viral entry point.

### PHPStan (0 to 1,000 stars in 3 months)

**Documented strategy:**
1. Build core value first, release early
2. Leverage existing Twitter following
3. Share development process publicly (build in public)
4. Submit to Reddit and community newsletters
5. Give talks at local user groups
6. Respond promptly to all feedback and issues
7. Celebrate milestones publicly

**Lesson for learn.python:** The PHPStan playbook is directly replicable. The key insight: the founder had an existing audience on Twitter before launching. Building that audience should start immediately.

---

## 3. GitHub SEO & Repository Optimization

### Current State

The README is strong but the repository's GitHub metadata can be optimized.

### Recommendations

**Repository description (About section):**
```
A complete, project-based Python curriculum — 246 projects from "what is a terminal?" to production deployment. Free, open-source, self-paced.
```

**Topics (tags):** Add these topics to the repository settings:
```
python, learn-python, python-tutorial, python-projects, python-course,
python-beginner, python-education, learn-to-code, programming-tutorial,
coding-challenges, fastapi, django, data-analysis, web-scraping,
project-based-learning, curriculum, self-paced, free-course
```

**Social preview image:** Create a custom Open Graph image (1280x640px) with:
- learn.python branding
- "246 Projects | 13 Levels | Zero to Production"
- Python logo
- Dark background with strong typography

**README optimization:**
- The README is already strong. Minor additions:
  - Add a "Star History" chart (using star-history.com)
  - Add a "Contributors" section with `contrib.rocks` or similar
  - Add a prominent CTA: "If this curriculum helped you, consider giving it a star"

**Pinning:** Pin the repo on the maintainer's GitHub profile.

---

## 4. Reddit & Hacker News Strategy

### Reddit

**Target subreddits:**

| Subreddit | Members | Strategy |
|-----------|---------|----------|
| r/learnpython | 951K+ | Primary target. Share individual projects as "practice exercises." Do NOT self-promote the whole repo. |
| r/Python | 1.4M+ | Share as a "Show r/Python" post once. Focus on the engineering behind the curriculum (validation scripts, auto-grader). |
| r/programming | 6M+ | Cross-post the launch announcement. Frame as "open-source education infrastructure." |
| r/learnprogramming | 3.5M+ | Share the absolute beginner path. Emphasize "no prior experience needed." |
| r/opensource | 200K+ | Frame as contribution opportunity. |
| r/datascience | 1M+ | Share the data analysis module specifically. |
| r/cscareerquestions | 800K+ | Share Career Readiness and Portfolio Guide docs. |

**Reddit best practices:**
- Build karma on r/learnpython by answering questions for 2-4 weeks BEFORE posting about the repo
- Never post the same link to multiple subreddits on the same day
- Frame posts as "I built this for myself and thought others might find it useful"
- Engage genuinely in comments. Answer every question.
- Do not ask for stars or upvotes. Let quality speak.
- Post individual, genuinely helpful content (concept guides, project ideas) that links back to the repo organically

**Timing:** Post between 8-10 AM Eastern on Tuesday or Wednesday for maximum visibility.

### Hacker News

**Show HN post:**

Title format:
```
Show HN: Learn Python — 246 projects from zero experience to production deployment
```

**Best practices:**
- Post around 9 AM Eastern, early in the week (Monday-Wednesday)
- The "Show HN:" prefix places the post on the less competitive "show" tab
- Do NOT ask friends to upvote. HN detects voting rings aggressively.
- Ask supporters to leave thoughtful comments instead of just upvoting
- Be present in the thread for the first 3-4 hours to answer every question
- Frame the post around what's technically interesting (the curriculum architecture, the validation system, the project-based approach), not as a sales pitch
- HN values authenticity. Share the origin story: why it was built, what problem it solves.

**Timing:** One shot. Do not repost if it doesn't gain traction on the first attempt. Wait at least 30 days before trying again with a different angle.

---

## 5. Social Media Strategy

### Twitter/X

**Account setup:**
- Handle: @learnpython_dev or @learnpythoncurr (check availability)
- Bio: "246 projects. Zero to production. Free, open-source Python curriculum."
- Pinned tweet: Launch announcement with GitHub link

**Content pillars (4-1-1 rule adapted):**

| Type | Frequency | Example |
|------|-----------|---------|
| Python tips/tricks | 3x/week | "Python tip: You can unpack dictionaries with **kwargs. Here's a 30-second example..." |
| Project spotlights | 2x/week | "Project spotlight: Build a CSV-to-JSON converter. Level 2, Project 12. Full tests included." |
| Behind-the-scenes | 1x/week | "Just added 5 new flashcard decks covering async/await. Here's how the Leitner box system works..." |
| Repo link/CTA | 1x/week | "The curriculum now has 246 projects. Star it on GitHub if you find it useful." |
| Community engagement | Daily | Reply to #Python, #100DaysOfCode, #learnpython tweets |

**Growth tactics:**
- Follow and engage with Python educators: Trey Hunner (@treyhunner), Al Sweigart (@AlSweigart), Talk Python (@taborators), Real Python (@realpython)
- Use hashtags: #Python, #100DaysOfCode, #LearnPython, #CodingNewbie, #OpenSource
- Create Twitter threads ("Here's how I designed a 246-project Python curriculum. Thread:")
- Share learner wins and progress (once the community exists)

### LinkedIn

**Content strategy:**
- Long-form posts about the "why" behind the curriculum design
- Frame as professional development content
- Tag Python-related companies and communities
- Post 2-3x/week
- Optimal video length: 90 seconds to 3 minutes (34% YoY increase in LinkedIn video engagement)

**Target audience:** Career changers, bootcamp graduates looking for supplemental practice, managers building Python-literate teams, educators looking for curriculum resources.

### Mastodon/Fediverse

- Post on fosstodon.org (FOSS-focused instance) or similar tech instance
- Lower reach but higher engagement per post
- Good for reaching open-source enthusiasts

---

## 6. YouTube & Video Content Strategy

### Assessment

Video is the highest-impact growth channel for programming education. freeCodeCamp, Fireship, Corey Schafer, and Tech With Tim all demonstrate that YouTube drives GitHub stars at massive scale. However, video production is expensive in time and effort.

### Recommended Approach: Start Small, Scale Strategically

**Phase 1 (Weeks 1-4): Proof of concept**
- Record 3-5 short (5-10 minute) walkthrough videos of Level 00 exercises
- Screen recording with voiceover (no face cam needed initially)
- Use free tools: OBS for recording, DaVinci Resolve for editing
- Upload to YouTube with SEO-optimized titles:
  - "Python for Complete Beginners - Your First Script (Project 1 of 246)"
  - "Learn Python by Building: Calculator Project Walkthrough"

**Phase 2 (Weeks 5-12): Consistent cadence**
- 1 video per week
- Mix of project walkthroughs and concept explanations
- Create playlists matching curriculum levels
- Add YouTube links to corresponding project README files

**Content format that works in 2025-2026:**
- Educational (40%): Project walkthroughs, concept explanations
- Entertainment (35%): "Building X in Python" challenges, "Can a beginner build this?"
- Inspirational (25%): Learner progress stories, "What you can build after Level 5"

**Key metrics to target:**
- 50% audience retention at the 2-minute mark (triggers algorithmic recommendation)
- Consistent upload schedule (trains both audience and algorithm)
- End every video with something the viewer has built

**Alternative: Partnered content**
If video production is not feasible:
- Partner with existing Python YouTubers to create companion content
- Offer curriculum as a structured path that creators can build videos around
- Create a "Creator Kit" with talking points, project descriptions, and screenshots

---

## 7. Contributor Pipeline

### The Conversion Problem

Most open-source projects describe their lack of contributors as a "pipeline problem," but it is almost always a "conversion problem." The pipeline (users) exists. Converting them into contributors requires lowering barriers at every stage.

### Contributor Funnel

```
Learners (users)
  └─→ Community members (join Discord/Discussions)
      └─→ Bug reporters (file first issue)
          └─→ Documentation contributors (fix typo, improve explanation)
              └─→ Content contributors (add project, write concept guide)
                  └─→ Maintainers (review PRs, triage issues)
```

### Concrete Actions

**1. Seed "good first issues" (pre-launch)**
Create 20-30 issues labeled `good first issue` across categories:
- Typo fixes in concept guides
- Add missing navigation links
- Write TRY_THIS.md for specific exercises
- Add test cases to existing projects
- Translate a concept guide section
- Improve error messages in validation scripts

**2. Create a CONTRIBUTORS.md**
Recognize every contributor, no matter how small the contribution. Use an all-contributors bot or similar tool.

**3. Mentored contributions**
For first-time contributors:
- Assign a maintainer to review within 24 hours
- Leave encouraging, detailed code review comments
- Merge quickly (don't let PRs sit)
- Thank publicly in the merge message

**4. Learner-to-contributor bridge**
Add a section to each project's notes.md:
```
## Found a bug? Have an improvement?
This curriculum is open source. If you found an error, thought of a better
explanation, or want to add a test case, open a PR. Every contribution helps
the next learner.
```

**5. Contributor recognition**
- Monthly "contributor spotlight" in Discussions or Discord
- Add contributor count badge to README
- Consider a HALL_OF_FAME.md for significant contributions

**6. Structured programs**
- Hacktoberfest participation (October): Label issues for Hacktoberfest, attracting contributors globally
- Google Summer of Code / Outreachy: If the project reaches sufficient scale, apply as a mentoring organization

---

## 8. Community Partnerships

### Python Software Foundation (PSF)

**PSF Community Partner Program:**
- Non-monetary partnership providing credibility and promotional support
- PSF will attach its name to events and promote through social media
- Apply at python.org/psf/community-partners/
- Requires: organized events or educational initiatives (learn.python qualifies)

**PSF Grants:**
- The PSF accepts grant proposals for educational resources related to Python
- Could fund: localization efforts, video production, community events
- Apply through PSF website

**PSF Discord:**
- Monthly Board Office Hours on PSF Discord
- Grants Program Office Hours (third Tuesday of each month, 1-2 PM UTC)
- Attend to build relationships and understand grant processes

### PyLadies

- International mentorship group focused on women in Python
- Operates under PSF fiscal sponsorship
- Partnership angle: Offer learn.python as a recommended curriculum for PyLadies chapters
- Create a "PyLadies Study Group Guide" showing how to use the curriculum in group settings

### Python Discord

- One of the largest Python communities online
- Share curriculum resources in appropriate channels
- Offer to help moderate a study group channel

### Local Python User Groups (PUGs)

- Search meetup.com for Python user groups in major cities
- Offer to present the curriculum at meetups (virtual or in-person)
- Create a "Meetup Workshop Kit" that PUG leaders can use to run sessions based on learn.python projects

### Bootcamp Partnerships

- Reach out to bootcamps as a "pre-work" or "supplemental practice" resource
- Bootcamps like General Assembly, Flatiron, Springboard often recommend external resources
- Frame as: "free, structured Python practice for your students"

### University/Education Partnerships

- The Teaching Guide already exists (TEACHING_GUIDE.md), targeting classroom use
- Reach out to CS professors and teaching assistants
- Post in r/CSEducation and r/compsci

---

## 9. Conference & Speaking Strategy

### PyCon US 2026 (CFP likely opens Q4 2025)

**Talk proposal angle:**
- Title: "246 Projects Later: Designing an Open-Source Python Curriculum from Zero to Production"
- Focus on curriculum design decisions, not the repo itself
- Discuss: project sequencing, how to teach debugging before giving answers, the flashcard/quiz system design

**Education Summit:**
- PyCon US has a dedicated Education Summit
- Ideal venue for presenting learn.python to educators
- Submit proposal specifically for this track

**Tutorial submission:**
- PyCon tutorials pay a $1,500 honorarium
- Propose: "Build 5 Python Projects in 3 Hours: A Hands-On Workshop" using learn.python projects
- Tutorial format naturally showcases the curriculum

### Regional PyCons

- PyCon DE, EuroPython, PyCon UK, PyCon APAC, PyCon Africa
- Lower acceptance bar than PyCon US
- Each conference introduces the curriculum to a new geographic audience

### Online Events

- Python Community News livestream
- Talk Python to Me podcast (guest appearance pitch)
- Real Python podcast
- PythonBytes podcast
- Python-related Twitch streams

### Lightning Talks

- Most PyCons have lightning talk slots (5 minutes, often open sign-up)
- Prepare a 5-minute demo: "From zero to first passing test in 5 minutes"
- Lightning talks are lower commitment and still get recorded

---

## 10. Localization Strategy

### Feasibility Assessment

Translating 50+ curriculum docs, 16 concept guides, 246 project READMEs, and quizzes is a massive effort. A phased approach is essential.

### Priority Languages (by market size and Python learner demand)

| Priority | Language | Rationale |
|----------|----------|-----------|
| 1 | Spanish | 580M+ speakers, large Latin American developer community, strong Python adoption in Spain/Mexico/Colombia/Argentina |
| 2 | Portuguese (Brazilian) | 260M+ speakers, Brazil has one of the fastest-growing developer communities globally |
| 3 | Simplified Chinese | 1.1B+ speakers, massive Python learner population, but competition from local platforms |
| 4 | Hindi | 600M+ speakers, India is the #2 developer population globally |
| 5 | French | 280M+ speakers, growing African developer community |
| 6 | Japanese | Strong Python community, high engagement with open-source education |
| 7 | Korean | Active developer community, strong open-source culture |

### Phased Approach

**Phase 1: Translation-ready infrastructure**
- Extract all user-facing strings into a translatable format
- Create a `/translations/` directory structure mirroring the docs
- Write a TRANSLATING.md guide for volunteer translators
- Use ISO 639-1 language codes (es/, pt-br/, zh-cn/, etc.)

**Phase 2: Translate the entry path only**
- README.md
- START_HERE.md
- 00_COMPUTER_LITERACY_PRIMER.md
- 01_ROADMAP.md
- Level 00 exercises (15 exercises)
- This gives a complete "first session" experience in the target language

**Phase 3: Community-driven translation**
- Recruit bilingual contributors for each language
- Use Crowdin, Transifex, or Weblate for translation management
- Recognize translators prominently

### Key Insight

Hedy, an educational programming language, supports 47 languages as of 2024. Their model: community volunteers translate via a web platform, with maintainers reviewing submissions. This scales far better than maintainer-driven translation.

---

## 11. Monetization Models

### Why Consider Monetization

GitHub's 2024 Open Source Economy Report found that developers who monetize their projects spend 3.5x more time maintaining them and release updates 2.8x more frequently. Sustainability, not profit, is the goal.

### Models Ranked by Feasibility

**Tier 1: Low effort, start immediately**

| Model | Description | Expected Revenue |
|-------|-------------|-----------------|
| GitHub Sponsors | Monthly sponsorship tiers ($1, $5, $10, $25) | $50-500/month at 500+ stars |
| "Buy Me a Coffee" | One-time donations via link in README | $20-100/month |
| Star/fork CTA | Not revenue, but drives all other metrics | N/A |

**Tier 2: Medium effort, start at 1K+ stars**

| Model | Description | Expected Revenue |
|-------|-------------|-----------------|
| Sponsor-only content | Early access to new modules, sponsor Discord channel | $200-1000/month |
| Corporate sponsors | Companies sponsor the repo for visibility (logo in README) | $500-2000/month per sponsor |
| Consulting/workshops | Paid workshops for companies adopting the curriculum for team training | $1000-5000 per workshop |

**Tier 3: High effort, start at 5K+ stars**

| Model | Description | Expected Revenue |
|-------|-------------|-----------------|
| Video course | Paid video companion on Udemy/Gumroad | $1000-5000/month |
| Certification service | Paid verification of curriculum completion (portfolio review, mock interview) | $50-200 per certification |
| Book adaptation | Publish curriculum as a physical/ebook | $500-3000/month |
| Premium mentorship | Paid 1:1 mentorship sessions | $50-150/hour |

### GitHub Sponsors Setup

GitHub Sponsors charges 0% fees on personal account sponsorships (100% goes to the maintainer). Organization account sponsorships have up to 6% fee.

**Recommended tiers:**
- $1/month: "Supporter" - Name in SPONSORS.md
- $5/month: "Learner" - Early access to new content + sponsor Discord channel
- $10/month: "Builder" - Above + monthly Q&A session
- $25/month: "Patron" - Above + logo in README
- $100/month: "Corporate" - Company logo in README, mention in release notes

---

## 12. Metrics & Tracking

### Primary Metrics (Track Weekly)

| Metric | Tool | Target (90 days) |
|--------|------|-------------------|
| GitHub Stars | GitHub Insights | 500+ |
| GitHub Forks | GitHub Insights | 50+ |
| Unique Clones | GitHub Traffic | 200+/week |
| Unique Visitors | GitHub Traffic | 500+/week |
| Open Issues | GitHub Issues | 20+ (sign of engagement) |
| Discussion Posts | GitHub Discussions | 50+ |
| Contributors | GitHub Insights | 10+ |
| Twitter/X Followers | Twitter Analytics | 500+ |

### Secondary Metrics (Track Monthly)

| Metric | Tool | Target (90 days) |
|--------|------|-------------------|
| Reddit mentions | Manual search / social listening | 10+ posts |
| YouTube views (if applicable) | YouTube Analytics | 1000+ total |
| Newsletter mentions | Manual tracking | 3+ |
| Blog post mentions | Google Alerts | 5+ |
| Discord members (if applicable) | Discord | 100+ |
| PR submissions | GitHub | 15+ |
| Star growth rate | star-history.com | Trending upward |

### Tools

- **GitHub Traffic:** Built into repository Insights tab
- **Star History:** star-history.com (embed chart in README)
- **Google Alerts:** Set up for "learn.python", "travisjneuman python"
- **Social listening:** Track mentions on Twitter, Reddit, HN using manual search or tools like Mention.com
- **Plausible/Umami:** If a documentation site is created, use privacy-friendly analytics

---

## 13. 90-Day Launch Playbook

### Pre-Launch (Days -14 to 0): Foundation

**Week -2:**
- [ ] Optimize GitHub repository metadata (description, topics, social preview image)
- [ ] Create Twitter/X account for the project
- [ ] Create LinkedIn presence (posts from maintainer's account)
- [ ] Set up GitHub Sponsors with tier structure
- [ ] Seed 20-30 "good first issues" across categories
- [ ] Add star-history chart to README
- [ ] Add contributor recognition tooling (all-contributors bot)
- [ ] Set up Google Alerts for project name
- [ ] Join Python Discord, r/learnpython, r/Python (begin participating genuinely)

**Week -1:**
- [ ] Write 3-5 Python tip tweets and schedule them
- [ ] Draft the Hacker News "Show HN" post title and talking points
- [ ] Draft Reddit posts for r/learnpython and r/Python
- [ ] Prepare a "launch day" checklist
- [ ] Record 1-2 short video walkthroughs (optional but high-impact)
- [ ] Create a simple Discord server with #general, #help, #introductions, #show-your-work channels
- [ ] Write a blog post / Twitter thread: "Why I built a 246-project Python curriculum"

---

### Phase 1: Launch Week (Days 1-7)

**Day 1 (Tuesday or Wednesday, 9 AM Eastern):**
- [ ] Post "Show HN: Learn Python - 246 projects from zero experience to production deployment" on Hacker News
- [ ] Be present in the HN thread for 3-4 hours, answering every question
- [ ] Post the "Why I built this" Twitter thread
- [ ] Share on personal LinkedIn

**Day 2:**
- [ ] Post on r/Python: "I built an open-source Python curriculum with 246 projects - from 'what is a terminal?' to deploying production apps"
- [ ] Engage with all comments

**Day 3:**
- [ ] Post on r/learnpython: Share a specific concept guide (e.g., "Functions Explained") as a standalone resource, with a note that it's part of a larger curriculum
- [ ] Post on r/learnprogramming

**Day 4-5:**
- [ ] Share on Python Discord
- [ ] Share on Dev.to with a detailed writeup
- [ ] Post on r/opensource

**Day 6-7:**
- [ ] Respond to all GitHub issues and discussions that arrived during launch week
- [ ] Merge any quick PRs from new contributors
- [ ] Write a "Week 1 recap" tweet/post with metrics

---

### Phase 2: Build Momentum (Weeks 2-4)

**Weekly cadence:**
- 3 Python tip tweets per week
- 2 project spotlight tweets per week
- 1 behind-the-scenes post per week
- 1 LinkedIn post per week
- Answer 3-5 questions on r/learnpython per week (build reputation)
- 1 video walkthrough per week (if doing YouTube)

**Week 2:**
- [ ] Submit to Python-related newsletters (Python Weekly, PyCoder's Weekly, Real Python newsletter)
- [ ] Pitch a guest appearance on Talk Python to Me or PythonBytes podcast
- [ ] Create a "Quick Start" YouTube short / TikTok (60 seconds)
- [ ] Add Discord invite link to README and CONTRIBUTING.md

**Week 3:**
- [ ] Post a "technical deep dive" on Dev.to or personal blog about the curriculum design
- [ ] Share specific expansion module (e.g., Web Scraping module) on r/learnpython as a standalone resource
- [ ] Begin engaging with PyLadies chapters about using the curriculum

**Week 4:**
- [ ] Run first "contributor sprint" - invite Discord members to tackle good first issues together
- [ ] Publish a "Month 1 Progress" update on GitHub Discussions
- [ ] Apply to PSF Community Partner Program
- [ ] Research PyCon US 2026 CFP timeline

---

### Phase 3: Sustain & Scale (Weeks 5-8)

**Week 5-6:**
- [ ] Launch a "30-Day Python Challenge" using Level 00 + Level 0 projects as a viral entry point
- [ ] Create a challenge-specific hashtag (#LearnPython246 or similar)
- [ ] Encourage participants to share daily progress on Twitter
- [ ] Submit PSF grant proposal for localization effort

**Week 7-8:**
- [ ] If YouTube is active: publish a "Python Project Walkthrough" playlist
- [ ] Reach out to 3-5 Python YouTubers about partnership/collaboration
- [ ] Begin Phase 1 localization (translation-ready infrastructure)
- [ ] Host first live coding session on Discord (walkthrough a project together)
- [ ] Publish second "technical deep dive" article

---

### Phase 4: Community Maturity (Weeks 9-12)

**Week 9-10:**
- [ ] Run second contributor sprint
- [ ] If eligible, prepare Hacktoberfest labels and promotion plan
- [ ] Recruit volunteer translators for top 2 priority languages (Spanish, Portuguese)
- [ ] Submit talk proposal to a regional PyCon or online Python event

**Week 11-12:**
- [ ] Publish "90-Day Retrospective" with full metrics
- [ ] Announce first community milestone (100 stars? 10 contributors? First translation?)
- [ ] Plan Q2 roadmap based on community feedback
- [ ] Evaluate monetization readiness (if 500+ stars, consider Tier 2 options)
- [ ] Write and share first "learner success story" (even if it's the maintainer's own learning journey)

---

### Milestone Targets

| Milestone | Target Date | Metric |
|-----------|-------------|--------|
| Launch post live | Day 1 | HN + Reddit posts published |
| First external contributor | Week 1 | 1+ merged PR from non-maintainer |
| 100 GitHub stars | Week 2 | Stars |
| Newsletter mention | Week 3 | Featured in Python Weekly or similar |
| Discord 50 members | Week 4 | Discord member count |
| 250 GitHub stars | Week 6 | Stars |
| First podcast/video mention | Week 8 | External media |
| 10+ contributors | Week 10 | GitHub contributor count |
| 500 GitHub stars | Week 12 | Stars |
| PSF Community Partner | Week 12 | Application accepted |

---

## Key Takeaways

1. **YouTube is the single highest-leverage growth channel** for programming education. Even 5-minute walkthrough videos can drive thousands of visitors to the GitHub repo. Start with screen recordings and voiceover.

2. **Discord is the community backbone.** GitHub Discussions is not enough. The Odin Project, freeCodeCamp, and Boot.dev all prove that a real-time community is what retains learners.

3. **The "30-Day Challenge" format is viral.** Extract a 30-project subset from the curriculum and frame it as a shareable challenge. This creates a low-commitment entry point.

4. **Build in public.** Share the development process on Twitter/X. The PHPStan case study shows that transparency about the building process itself attracts attention.

5. **Reddit requires earned credibility.** Spend 2-4 weeks genuinely helping people on r/learnpython before posting about the repo. The community will support resources from active, helpful members.

6. **The content already exists.** 246 projects, 50+ docs, 16 concept guides. The product is strong. The entire problem is distribution. Every action in this playbook is about getting existing content in front of the right people.

7. **Start sponsorship early.** Even if it generates $10/month initially, GitHub Sponsors signals that the project is a serious, maintained effort and creates a path to sustainability.

---

*This strategy was produced as part of the learn.python v2 audit. It should be revisited and updated at the 90-day mark based on actual metrics and community feedback.*
