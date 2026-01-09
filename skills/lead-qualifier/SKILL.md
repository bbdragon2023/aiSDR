---
name: lead-qualifier
description: Score and qualify leads based on fit criteria, engagement signals, and buying readiness. Use when evaluating whether a lead is worth pursuing or prioritizing leads.
license: MIT
metadata:
  author: sdr-agent
  version: "1.0"
  tags: qualification, scoring, prioritization, sales
---

# Lead Qualifier Skill

This skill guides the evaluation and prioritization of sales leads.

## Qualification Framework

### SPICED Framework (Winning by Design)

SPICED is a diagnostic framework developed by [Winning by Design](https://winningbydesign.com) that helps you better diagnose prospects. Like a doctor, your prescribed solution should help them achieve their desired outcomes—solving the source of their pains, not just the symptoms.

**Situation**
- What is their current environment and context?
- What facts and background information define their circumstances?
- What systems, processes, or solutions are they using today?
- What is their role and team structure?

**Pain**
- What specific challenges motivated them to seek a solution?
- What problems are they experiencing with their current approach?
- What's not working or causing friction?
- Is this a symptom or the root cause?

**Impact**
- How does this pain affect their business outcomes?
- What metrics or KPIs are being impacted?
- What is the cost of inaction (time, money, opportunity)?
- What value would solving this deliver?

**Critical Event**
- What is the deadline by which they need to achieve results?
- What's driving this timeline (contract expiration, board meeting, compliance deadline)?
- What happens if they miss this deadline?
- Is there a compelling event creating urgency?

**Decision**
- Who is involved in the decision-making process?
- What is their evaluation criteria?
- What is the internal buying process?
- Who else needs to be persuaded?
- What factors will determine their final choice?

### ICP (Ideal Customer Profile) Fit

Score leads against your ICP criteria:

| Criteria | Excellent (3) | Good (2) | Marginal (1) | Poor (0) |
|----------|--------------|----------|--------------|----------|
| Company Size | [Ideal range] | [Adjacent] | [Stretch] | [Outside target] |
| Industry | [Target vertical] | [Adjacent] | [New territory] | [Poor fit] |
| Tech Stack | [Perfect match] | [Compatible] | [Integration needed] | [Incompatible] |
| Growth Stage | [Sweet spot] | [Close] | [Stretch] | [Mismatch] |
| Geography | [Target region] | [Serviceable] | [Challenging] | [Cannot serve] |

### Buying Signals

**Strong Signals (High Priority)**
- Requested pricing/demo
- Responded to outreach positively
- Actively evaluating solutions
- Budget approved
- Clear timeline stated
- Executive sponsor identified

**Medium Signals (Qualified)**
- Engaged with content multiple times
- Attending webinars/events
- Job postings indicating need
- Company growth/funding
- Technology changes

**Weak Signals (Nurture)**
- Downloaded single asset
- Single website visit
- Cold list match
- No engagement history

## Lead Scoring Model

### Demographic Score (0-50 points)

| Factor | Points |
|--------|--------|
| Title matches buyer persona | 15 |
| Company in target industry | 10 |
| Company size in range | 10 |
| Geography in target region | 5 |
| Tech stack compatible | 10 |

### Behavioral Score (0-50 points)

| Action | Points |
|--------|--------|
| Requested demo | 20 |
| Responded to email | 15 |
| Visited pricing page | 10 |
| Downloaded content | 5 |
| Attended webinar | 10 |
| Multiple website visits | 5 |
| LinkedIn engagement | 5 |

### Total Score Interpretation

| Score Range | Priority | Action |
|-------------|----------|--------|
| 80-100 | Hot | Immediate outreach, escalate to AE |
| 60-79 | Warm | Prioritized outreach sequence |
| 40-59 | Qualified | Standard nurture sequence |
| 20-39 | Marketing | Marketing nurture only |
| 0-19 | Unqualified | Disqualify or long-term nurture |

## Qualification Questions

When engaging leads, gather information on:

### Business Context
- "What's prompting you to look at this now?"
- "How are you handling [problem] today?"
- "What would success look like?"

### Decision Process
- "Who else is involved in evaluating solutions?"
- "What's your timeline for making a decision?"
- "Do you have budget allocated for this?"

### Requirements
- "What are your must-haves vs. nice-to-haves?"
- "What other solutions are you considering?"
- "What would make you choose one solution over another?"

## Disqualification Criteria

Leads should be disqualified if:

- **No fit**: Company clearly outside ICP
- **No budget**: No possibility of funding
- **No authority**: Contact cannot influence decision
- **No need**: No clear problem or priority
- **No timeline**: No foreseeable buying window
- **Competition**: Already using competitor, happy with it
- **Bad data**: Cannot verify company or contact

## Output Format

When qualifying a lead, provide:

```markdown
# Lead Qualification: [Company/Prospect]

## Qualification Summary
- **Overall Score**: [X]/100
- **Priority**: [Hot/Warm/Qualified/Nurture/Disqualified]
- **Recommendation**: [Specific action]

## ICP Fit Analysis
| Criteria | Score | Notes |
|----------|-------|-------|
| Company Size | X/3 | [Details] |
| Industry | X/3 | [Details] |
| Tech Stack | X/3 | [Details] |
| Geography | X/3 | [Details] |

## SPICED Assessment
- **Situation**: [Current environment and context]
- **Pain**: [Core challenges and root causes]
- **Impact**: [Business outcomes affected and cost of inaction]
- **Critical Event**: [Timeline drivers and compelling events]
- **Decision**: [Decision process, criteria, and stakeholders]

## Buying Signals
[List observed signals]

## Concerns/Risks
[Any red flags or concerns]

## Recommended Next Steps
1. [Action 1]
2. [Action 2]
3. [Action 3]
```

## Priority Matrix

Use this matrix to prioritize your lead queue:

```
                    HIGH FIT
                       |
     NURTURE          |        HOT
     (Future opp)     |        (Pursue now)
                      |
LOW ENGAGEMENT -------+------- HIGH ENGAGEMENT
                      |
     DISQUALIFY       |        QUALIFIED
     (Poor fit)       |        (Active sequence)
                      |
                    LOW FIT
```

## Best Practices

1. **Score objectively** - Use data, not gut feel
2. **Update regularly** - Scores change as engagement happens
3. **Document reasoning** - Note why you scored each factor
4. **Review periodically** - Audit scoring accuracy
5. **Disqualify quickly** - Don't waste time on poor fits
6. **Prioritize ruthlessly** - Focus on highest-potential leads
