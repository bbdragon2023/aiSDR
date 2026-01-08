---
name: company-research
description: Research companies to understand their business, technology stack, funding, news, and key decision makers. Use when the user asks to research a company or prepare for outreach to a specific organization.
license: MIT
metadata:
  author: sdr-agent
  version: "1.0"
  tags: research, company, b2b, sales
---

# Company Research Skill

This skill guides comprehensive company research for B2B sales outreach.

## Research Framework

When researching a company, gather information in these categories:

### 1. Company Overview
- Official company name and any DBA names
- Founding date and company age
- Headquarters location and office locations
- Company size (employees, revenue if public)
- Industry and market segment
- Mission statement and value proposition

### 2. Products and Services
- Core product/service offerings
- Target customer segments
- Pricing model (if available)
- Key differentiators from competitors
- Recent product launches or updates

### 3. Technology Stack
- Known technologies used (check job postings, BuiltWith, StackShare)
- Cloud infrastructure (AWS, GCP, Azure)
- Development frameworks and languages
- Marketing/sales tools (CRM, marketing automation)
- Integrations and partnerships

### 4. Funding and Financials
- Funding stage and total raised (for private companies)
- Recent funding rounds
- Key investors
- Revenue estimates (if available)
- Growth trajectory

### 5. Recent News and Developments
- Press releases from last 6 months
- News coverage and media mentions
- Product announcements
- Executive changes
- Awards and recognition

### 6. Key Decision Makers
- C-suite executives (CEO, CTO, CFO, CMO, CRO)
- VP-level leaders relevant to your solution
- Hiring managers in target departments
- Their backgrounds and tenure

### 7. Pain Points and Opportunities
- Challenges mentioned in job postings
- Industry trends affecting them
- Competitive pressures
- Growth initiatives

## Search Strategies

Use these search queries to find information:

```
"{company name}" overview OR about
"{company name}" funding OR raised OR investors
"{company name}" news OR press release
"{company name}" technology OR stack OR engineering
site:linkedin.com "{company name}" CEO OR CTO OR VP
"{company name}" reviews OR customers
```

## Output Format

Structure your research report as follows:

```markdown
# Company Research: [Company Name]

## Overview
[2-3 sentence summary]

## Key Facts
- Founded: [Year]
- Headquarters: [Location]
- Employees: [Count]
- Industry: [Industry]

## Products & Services
[Bullet points of main offerings]

## Technology
[Known tech stack]

## Funding
[Funding history and investors]

## Recent News
[Key developments from last 6 months]

## Key Contacts
[Decision makers with titles]

## Outreach Opportunities
[Specific angles for personalized outreach]
```

## Best Practices

1. **Verify information** - Cross-reference data from multiple sources
2. **Focus on relevance** - Prioritize information useful for outreach
3. **Note recency** - Flag when information might be outdated
4. **Identify gaps** - Acknowledge what you couldn't find
5. **Suggest next steps** - Recommend additional research if needed
