---
name: prospect-research
description: Research individual prospects to understand their role, background, interests, and recent activity. Use when preparing personalized outreach to a specific person.
license: MIT
metadata:
  author: sdr-agent
  version: "1.0"
  tags: research, prospect, personalization, sales
---

# Prospect Research Skill

This skill guides comprehensive research on individual prospects for personalized B2B outreach.

## Research Framework

When researching a prospect, gather information in these categories:

### 1. Professional Identity
- Current title and role
- Company and department
- Reporting structure (who they report to, who reports to them)
- Time in current role
- Location and time zone

### 2. Career History
- Previous roles and companies
- Career progression pattern
- Industry experience depth
- Notable achievements or promotions
- Patterns (startup person vs. enterprise, etc.)

### 3. Educational Background
- Universities attended
- Degrees and fields of study
- Certifications and training
- Continuing education

### 4. Professional Interests
- Topics they post about
- Articles they've written or shared
- Conferences they've spoken at
- Podcasts or interviews
- Professional associations

### 5. Recent Activity
- LinkedIn posts from last 30 days
- Comments on industry topics
- Job changes or promotions
- Company announcements involving them
- Speaking engagements

### 6. Connection Points
- Mutual connections
- Shared alma maters
- Common previous employers
- Shared interests or hobbies
- Geographic connections

### 7. Communication Style
- Formal vs. casual based on content
- Topics they engage with
- How they describe themselves
- Tone of their posts

## Search Strategies

Use these search queries:

```
"{prospect name}" "{company name}" LinkedIn
"{prospect name}" "{company name}" speaker OR conference
"{prospect name}" "{company name}" interview OR podcast
"{prospect name}" "{company name}" article OR blog
site:linkedin.com/in "{prospect name}"
"{prospect name}" {industry} {topic}
```

## Output Format

Structure your prospect profile as:

```markdown
# Prospect Profile: [Name]

## Current Role
- **Title**: [Title]
- **Company**: [Company]
- **Department**: [Department]
- **Location**: [Location]
- **Tenure**: [Time in role]

## Background
[2-3 sentences on career trajectory]

## Career History
- [Previous Role] at [Company] ([Years])
- [Previous Role] at [Company] ([Years])

## Education
- [Degree] from [University]
- [Certifications]

## Professional Interests
[Topics they care about based on activity]

## Recent Activity
[Notable posts, achievements, or news from last 30-60 days]

## Personalization Opportunities
[Specific angles for personalized outreach]

## Recommended Approach
[Suggested outreach strategy and talking points]
```

## Best Practices

1. **Respect privacy** - Only use publicly available professional information
2. **Focus on professional** - Avoid personal/family information
3. **Note context** - Understand why information matters for outreach
4. **Find commonality** - Identify genuine connection points
5. **Be current** - Prioritize recent information over old
6. **Verify identity** - Ensure you have the right person

## Personalization Triggers

Look for these high-value personalization opportunities:

- **Promotions** - Congratulate on new role
- **Content creation** - Reference their post/article
- **Speaking** - Mention their talk or podcast
- **Company news** - Connect to recent announcements
- **Shared background** - Common school, employer, or interest
- **Industry trends** - Topics they've engaged with

## Red Flags

Watch for these signals that may affect outreach:

- Recently changed jobs (may not be settled)
- Actively job hunting (may not be decision maker)
- Negative posts about vendors (bad timing)
- Very junior despite title (limited authority)
- No recent activity (inactive account)
