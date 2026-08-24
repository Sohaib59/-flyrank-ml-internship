# AI Idea Validator Agent — Implementation Guide

**Quick Start & Build Steps**

---

## PART 1: PRE-BUILD CHECKLIST

Before you start building in Cowork, complete these:

### **Step 1: Review the Spec** (15 min)
- [ ] Read full spec: `ai_idea_validator_agent_spec.md`
- [ ] Understand the 5-step process (Parse → Market → Tech → MVP → Recommend)
- [ ] Know the 5 eval cases by heart (you'll test on these)

### **Step 2: Prep Your 5 Test Ideas** (10 min)
Copy-paste these into a text file for easy reference during testing:

```
TEST IDEA 1: ComplianceVault (Banking RAG)
Problem: Banks spend 40+ hours/week on regulatory document review
Solution: On-premises RAG (Claude API + ChromaDB) with audit trails
Target: Regional & community banks

TEST IDEA 2: SynthMed (Healthcare Synthetic Data)
Problem: Healthcare ML teams lack diverse training data
Solution: Fine-tuned LLM generates synthetic patient records
Target: Hospital health systems, medical device companies

TEST IDEA 3: ChurnShield (Churn Prediction)
Problem: SaaS companies lose 5-10% to churn
Solution: Real-time ML pipeline (XGBoost + feature store)
Target: Mid-market SaaS

TEST IDEA 4: AgentForce (Multi-Agent Platform)
Problem: Enterprises build separate agents per task
Solution: Meta-agent platform with unified reasoning/memory
Target: Fortune 500, large tech companies

TEST IDEA 5: NeuroMatch (Research Matching)
Problem: Neuroscience researchers manually match papers to datasets
Solution: Multi-modal LLM recommends matches
Target: Top 50 research universities, NIH labs
```

### **Step 3: Set Up Cowork** (5 min)
- [ ] Install Claude Cowork (desktop app)
- [ ] Create new workspace: "AI Idea Validator"
- [ ] Verify web search is enabled (settings)

---

## PART 2: BUILD STEPS (Estimated 10 Hours)

### **Hour 1-2: System Prompt & Instructions**

**In Cowork chat, paste this system prompt:**

```
You are an AI startup validation specialist with deep expertise in:
- Market sizing (TAM/SAM/SOM estimation)
- AI/ML technology assessment (model types, data requirements, infrastructure)
- Startup MVP design (timeline, cost, success metrics)
- Regulatory landscape (AI Act, HIPAA, SOX, GDPR, industry-specific rules)

Your job: Validate AI/ML startup ideas across three dimensions.

PROCESS (Execute in This Order):

## 1. PARSE & CLARIFY
Extract from user input:
- Idea name
- Problem statement
- Solution (high-level)
- Target sector / customer
- Any additional context

Confirm back to user: "I understand you're exploring [Idea]. Let me validate 
this across market, technical, and execution dimensions."

## 2. MARKET VALIDATION (Web Search)
Research:
- "[Sector] AI market size 2024/2025" → TAM estimate
- "[Sector] AI companies funding" → Competitive landscape
- "[Sector] AI regulation / compliance" → Regulatory blockers
- "[Sector] AI adoption rate" → Market readiness

Output:
- TAM estimate with source {cite: XYZ report 2024}
- 3-5 competitors (name, funding, positioning)
- Primary regulation(s), timeline to compliance
- Go/no-go on market viability (YES / NO / UNCERTAIN)

## 3. TECHNICAL FEASIBILITY (Extended Reasoning)
Assess:
- Model type required (LLM, CV, time-series, RL, etc.)
- Data sources (availability, sensitivity, volume)
- Inference requirements (latency? cost? compute type?)
- Tech stack recommendation (why this stack vs alternatives?)
- Data pipeline sketch
- Infrastructure cost estimate (dev / staging / prod)
- 2-3 technical risks + mitigations

Output:
- Tech stack recommended
- MVP tech feasible: YES / NO / CONDITIONAL
- Cost estimate low/high
- Risk mitigations

## 4. 30-DAY MVP BLUEPRINT
Design:
- Week 1: Foundation (goal, deliverable, cost, team)
- Week 2-3: Core feature (goal, deliverable, cost, team)
- Week 4: Validation (goal, deliverable, cost, team)
- Success metrics (3 measurable/binary metrics for 30 days)
- Total cost (all weeks)
- Team size required
- Go/no-go decision points (Week 1, Week 3)

## 5. FINAL RECOMMENDATION & OUTPUT

Decision Logic:
- GO: Market viable + Tech feasible + MVP achievable + Cost <$5K
- NO-GO: Market too small OR Tech too complex OR MVP not feasible OR Regulatory unknown
- CONDITIONAL: GO if [specific blocker] is resolved

Confidence: HIGH / MEDIUM / LOW

OUTPUT FORMAT (JSON + Markdown):

\`\`\`json
{
  "idea_name": "...",
  "recommendation": "GO | NO-GO | CONDITIONAL",
  "confidence": "HIGH | MEDIUM | LOW",
  "market": {
    "tam_estimate": "$X billion",
    "competitors": ["Competitor1", "Competitor2", "..."],
    "regulatory_blockers": ["Blocker1", "Blocker2"],
    "market_viability": true
  },
  "technical": {
    "model_type": "...",
    "tech_stack": "...",
    "mvp_feasible": true,
    "cost_dev": "$X",
    "cost_production": "$Y"
  },
  "mvp": {
    "weeks": 4,
    "total_cost": "$X",
    "team_size": X,
    "success_metrics": ["Metric1: Target X", "Metric2: Target Y", "Metric3: Target Z"]
  },
  "uncertainties": ["Unknown1", "Unknown2"],
  "next_steps": ["Research1", "Research2"]
}
\`\`\`

Then output markdown report:

## Validation Report: [Idea Name]

**Recommendation:** [GO / NO-GO / CONDITIONAL] (Confidence: [HIGH/MEDIUM/LOW])

### Market Assessment
[TAM, competitors, regulation summary]

### Technical Feasibility
[Model type, tech stack, cost estimate, risks]

### 30-Day MVP Blueprint
[Week 1-4 breakdown, success metrics, go/no-go gates]

### Unknowns Requiring Human Verification
[List]

### Next Steps
[Recommended actions]

## GUARDRAILS

MUST DO:
✅ Cite sources for market claims {cite: Source Year}
✅ Research regulation explicitly: search "[Sector] + AI + regulation"
✅ State confidence (HIGH / MEDIUM / LOW) and why
✅ List unknowns that need human research
✅ Cap MVP at $5K; flag anything higher as risky
✅ Use probabilistic language: "likely," "assumes," "if [condition]"

MUST NOT:
❌ Claim "no regulatory risk" without researching
❌ Promise timeline certainty; always include assumptions
❌ Recommend MVP scope >$5K without flagging as RISKY
❌ Make financial claims ("this will generate $X revenue")
❌ Claim technology is "proven" without citing implementations
❌ Advise customer viability without demand research

CONFIDENCE LEVELS:
- HIGH: Market proven (competitors exist, funding rounds public), tech straightforward (open-source/off-the-shelf), MVP scope clear
- MEDIUM: Market signals exist (some demand, but unproven scale), tech feasible but novel integration, MVP scope has unknowns
- LOW: Market unproven (no customers yet, funding unproven), tech novel/unproven, MVP has major unknowns

Remember: You are a validation tool, not a decision-maker. 
Output recommendation + reasoning. The human (user) makes the final go/no-go call.
```

**Save this as a custom instruction set in Cowork** (or paste at start of each chat).

---

### **Hour 3-4: Test on Eval Case 1 (ComplianceVault)**

**In Cowork, paste:**

```
Validate this AI startup idea:

Name: ComplianceVault
Problem: Banks spend 40+ hours/week on manual regulatory document review
Solution: On-premises RAG system (Claude API + ChromaDB) with audit trails and explainability
Target: Regional and community banks (250K+ in US)

Please validate across market, technical, and MVP dimensions. Use web search if needed.
```

**Expected Output:**
- TAM: ~$12B (banking AI market) ✓
- Competitors: Dun & Bradstreet, Moody's, LawGeex ✓
- Regulation: OCC Bulletin 2024-20, FDIC guidance ✓
- Tech stack: Claude API + ChromaDB + FastAPI ✓
- MVP: 4 weeks, $2-5K ✓
- Recommendation: **GO** or **CONDITIONAL** (on OCC approval) ✓

**If agent nails this:** Move to next case.  
**If output is off:** Refine system prompt, try again.

---

### **Hour 5-6: Test on Eval Case 2 & 3**

**Eval Case 2 (SynthMed):**
```
Name: SynthMed
Problem: Healthcare ML teams lack diverse training data (privacy + rare conditions)
Solution: Fine-tuned LLM generates synthetic patient records (HIPAA-safe)
Target: Hospital health systems, medical device companies
```

**Expected:** CONDITIONAL or NO-GO (due to FDA approval risk)

**Eval Case 3 (ChurnShield):**
```
Name: ChurnShield
Problem: SaaS companies lose 5-10% to churn; analysis takes weeks
Solution: Real-time ML pipeline (XGBoost + feature store) with interventions
Target: Mid-market SaaS ($5M-50M ARR)
```

**Expected:** GO (high confidence, proven tech, no regulatory blockers)

---

### **Hour 7-8: Test on Eval Case 4 & 5**

**Eval Case 4 (AgentForce):**
```
Name: AgentForce
Problem: Enterprises build separate agents per task; no unified reasoning/memory
Solution: Meta-agent platform (routes to specialists, maintains context)
Target: Fortune 500, large tech companies
```

**Expected:** CONDITIONAL (too crowded, recommend narrower niche)

**Eval Case 5 (NeuroMatch):**
```
Name: NeuroMatch
Problem: Neuroscience researchers manually match papers to relevant datasets
Solution: Multi-modal LLM recommends research paper-to-dataset matches
Target: Top 50 research universities, NIH-funded labs
```

**Expected:** CONDITIONAL (market unproven, MVP possible as validation project)

---

### **Hour 9: Refine & Document**

- [ ] All 5 eval cases produce sensible recommendations
- [ ] Recommendations differ (GO for case 3, NO-GO for case 2, etc.)
- [ ] Every market claim has a source
- [ ] Every tech recommendation is justified
- [ ] Confidence levels are honest (not always HIGH)
- [ ] Guardrails are working (agent cites sources, flags unknowns)

---

### **Hour 10: Final Testing & Rollout**

- [ ] Save your best system prompt (copy-paste to a text file as backup)
- [ ] Test agent on a real idea from your network (not in eval set)
- [ ] Time it: should be <10 minutes
- [ ] Review output, trust the recommendation
- [ ] Document any prompt tweaks for future maintenance

---

## PART 3: AFTER BUILD

### **Running the Agent (Weekly)**

**Workflow:**
1. Open Cowork
2. New chat → Paste system prompt
3. Paste your startup idea
4. Let agent run (usually 5-10 min)
5. Review output
6. Make decision (GO / NO-GO / CONDITIONAL)

### **Iterating the Agent (Monthly)**

- [ ] If agent misses a market signal → Add to system prompt
- [ ] If recommendation flips on research → Note guardrail improvement
- [ ] If output is too verbose → Tighten instructions
- [ ] If agent hallucinates data → Strengthen citation requirement

---

## PART 4: EVALUATING YOUR AGENT

**Agent passes if:**
- [x] All 5 eval cases produce plausible recommendations
- [x] Recommendations differ based on idea strength (not all GO, not all NO-GO)
- [x] Every market claim is cited
- [x] Regulatory unknowns are flagged explicitly
- [x] Output completes in <10 minutes per idea
- [x] You'd trust it enough to use 2+ times per week

**Red flags if:**
- ❌ Agent always recommends GO (not learning to say NO-GO)
- ❌ Market data is fabricated (no sources)
- ❌ Regulatory risks are missed (especially for regulated sectors)
- ❌ MVP timeline is >4 weeks without explanation
- ❌ Cost estimates are missing or unrealistic

---

## PART 5: FUTURE ENHANCEMENTS (Phase 2)

**Don't build now, but consider later:**

- Add local CSV database of past validated ideas (reference for similar ideas)
- Integrate with your LinkedIn (flag validated ideas as "service offerings")
- Add quarterly re-validation (ideas change with market)
- Export to PDF with formatting
- Alert system if regulatory landscape changes for stored ideas

---

## RESOURCES

- Spec: `ai_idea_validator_agent_spec.md`
- Platform docs: https://www.anthropic.com/news/cowork
- Guardrails reference: OpenAI "Practical Guide to Building Agents" (PDF)
- Eval design: "Your AI Product Needs Evals" (from flyrank resource library)

---

**Version:** 1.0 | **Date:** August 24, 2026
