---
description: Transform business hypotheses into working validation prototypes within 80 hours. Creates functional prototypes covering critical functionality with working code for rapid hypothesis testing and user feedback collection.
auto_execution_mode: 1
---

# Build Prototype Workflow
As a Solution architect, build a prototype that validates a given business hypothesis within an 80-hour timeframe. The prototype must include all necessary features to test the hypothesis, complete with working source code, documentation, and automated validation evidence.

## Input Parameters: $ARGUMENTS (Optional)
**Accepts:** Business hypothesis | Feature idea | Problem statement | User need description

**Example Inputs:**
- "Test if small business owners will pay for automated invoice tracking"
- "Validate market demand for markdown-to-slides conversion"
- "Build prototype for real-time collaboration on documents"

## Output
**Deliverables in mvp/ folder:**
- `mvp-scope-and-journeys.md` - Validation plan with hypothesis and user journeys
- `src/` - Complete working source code (HTML, JS, CSS, assets)
- `README.md` - Setup and launch instructions
- `deployment-guide.md` - Deployment procedures
- `test-results/` - Automated validation evidence with screenshots
- Print the following: 
  - List of rules used by the workflow in bulleted format
  - Evaluation Scores in tabular format with average score. 
  - Evaluation summary (less than 100 words).
  **Do not save as file.**

## Execution Flow

### Core Principles
- **Code-first delivery**: Working source code is primary output
- **Validation-focused**: Every feature enables hypothesis testing
- **Minimal viable**: Build only what's needed for validation
- **Launch-ready**: Stakeholders can test immediately
- **Modern design**: Clean, accessible, contemporary interface
- **Time-boxed**: 80-hour constraint with priority-based scoping

### Hypothesis Definition (4 hours)

**Create mvp/ folder structure**
```bash
mkdir -p mvp/src
mkdir -p mvp/test-results/screenshots
```

**Analyze business hypothesis** (use sequential-thinking MCP)
- Extract core business assumption from input
- Identify validation success criteria
- Define primary and secondary user personas for testing
- Map validation user journeys

**Generate validation plan**

**Before writing MVP scope, list all features to build (ordered by priority):**
| Priority | Feature | Purpose | Est. Hours | Validates Hypothesis? |
|----------|---------|---------|------------|----------------------|
| 1 (High) | ... | ... | [X] | Yes/No |
| 2 | ... | ... | [X] | Yes/No |
| N (Low) | ... | ... | [X] | Yes/No |

**Priority Cut-off Rule:**
- Sum estimated hours from Priority 1 downward
- IF cumulative total ≤80 hours: Include ALL features
- IF cumulative total >80 hours: Draw cut-off line where sum reaches 80; exclude features below line
**Now expand each feature listed above (within scope).**

- Create `mvp/mvp-scope-and-journeys.md` with:
  - Business hypothesis statement
  - Validation success criteria
  - Primary and secondary user personas
  - Validation user journeys
  - MVP validation features (ordered by priority: highest to lowest)
  - 80-hour timeline breakdown
  - Priority cut-off line (if requirements exceed 80 hours)

**Request user approval**
- Present mvp-scope-and-journeys.md to user
- Wait for explicit approval before proceeding
- **STOP HERE until user confirms approval**

### Prototype Build (68 hours)

**Pre-implementation verification**
- Read approved mvp-scope-and-journeys.md file
- Create TodoWrite plan with all source files
- Verify folder structure exists

**Technology selection** (use sequential-thinking MCP for rapid decisions)
- Choose proven frameworks (Next JS/vanilla JS)
- Select UI components (prioritize shadcn/ui)
- Determine if backend needed (auto-detect from requirements. Prefer for the complex requirements)
- Plan minimal tech stack for validation
- **AI Component Selection** [CONDITIONAL: If hypothesis involves AI/LLM features]:
  - Determine if AI features are needed for validation (chatbot, Q&A, content generation)
  - If AI needed:
    - Use mock LLM responses for prototype (avoid API costs during validation)
    - Pre-configure 5-10 sample responses that demonstrate intended behavior
    - Include fallback UI for "AI is thinking" and error states
    - Document real AI integration path for post-validation phase
  - If RAG needed for validation:
    - Use static sample documents with predetermined answers
    - Mock retrieval results to demonstrate intended UX
    - Skip actual embedding/indexing (defer to production implementation)
  - **Cost Estimation**: Estimate API costs if real AI will be used in validation
    - Stay within 80-hour budget constraint
    - Prefer mocked responses over real API calls for prototype phase

**Priority-Based Scope Management:**
- List all requirements ordered from highest to lowest priority
- Estimate hours for each requirement
- Include ALL requirements if total fits within 80 hours
- IF total exceeds 80 hours:
  - Draw priority cut-off line where cumulative hours reach 80
  - Requirements above line: MUST implement
  - Requirements below line: EXCLUDED from prototype scope
  - Document excluded requirements for future iterations

**Generate working code** (use context7 MCP for framework guidance)
- Build validation interface using shadcn components
- Implement core hypothesis testing features
- Create feedback collection mechanisms
- Generate backend services if needed (Node.js/Express with mock data)

**File creation with path validation**
- Use `Write('mvp/src/filename')` for ALL files
- Verify each file: `ls -la mvp/src/filename`
- Track creation in TodoWrite
- Minimum required: index.html, app.js, style.css, package.json

**Modern UI implementation**
- Clean, contemporary interface design
- Neutral-first color system with purposeful accents
- Spacious layout with strong visual hierarchy
- Accessible contrast and responsive behavior
- Essential shadcn components only

### Documentation & Testing Setup (4 hours)

**Create documentation**
- `mvp/README.md` - Setup and launch guide
- `mvp/deployment-guide.md` - Deployment instructions
- Document validation procedures

**Prepare for testing**
- Define validation test scenarios
- Set up test environment configuration
- Document expected validation outcomes

### Automated Validation (4 hours)

**Launch prototype** (use Playwright MCP)
```
1. Navigate: mcp__playwright__browser_navigate(url)
2. Capture: mcp__playwright__browser_take_screenshot("mvp-launch.png")
```

**Test user journeys** (use Playwright MCP)
```
For each persona:
1. Snapshot: mcp__playwright__browser_snapshot()
2. Interact: mcp__playwright__browser_click/fill_form/type
3. Validate: mcp__playwright__browser_wait_for(expected_result)
4. Capture: mcp__playwright__browser_take_screenshot("journey-X.png")
```

**Validate feedback mechanisms**
- Test feedback collection features
- Verify submission workflows
- Document functionality

**Generate validation report**
- Create `mvp/test-results/validation-report.md`
- Document test results with screenshot evidence
- Assess hypothesis testing readiness

### Success Criteria
**Technical Success:**
- Prototype builds and runs without errors
- All validation features functional
- Professional UI suitable for user testing

**Business Success:**
- Clear value proposition demonstration
- Hypothesis testing enabled
- User feedback collection functional

**Process Success:**
- User approval obtained before implementation
- Working code delivered within 80 hours
- Complete documentation for stakeholder testing
- Priority scoping applied correctly (if requirements exceeded budget)

### Quality Assurance Framework

#### Completion Checklist

**Verify all deliverables exist:**
```bash
ls -d mvp/                              # MVP folder
ls mvp/mvp-scope-and-journeys.md        # Validation plan
ls -la mvp/src/                         # Source code folder
ls mvp/src/index.html                   # Entry point
ls mvp/src/app.js                       # Application logic
ls mvp/src/style.css                    # Styling
ls mvp/README.md                        # Setup guide
ls mvp/deployment-guide.md              # Deployment guide
ls -d mvp/test-results/                 # Test results folder
ls mvp/test-results/validation-report.md # Validation report
ls mvp/test-results/screenshots/        # Visual evidence
tree mvp/                               # Complete structure
```
## Guardrails
- `rules/ai-assistant-usage-policy.md`: Explicit commands; minimal output
- `rules/code-anti-patterns.md`: Avoid god objects, circular deps, magic constants
- `rules/dry-principle-guidelines.md`: Single source of truth; delta updates
- `rules/iterative-development-guide.md`: Strict phased workflow
- `rules/language-agnostic-standards.md`: KISS, YAGNI, size limits, clear naming
- `rules/markdown-styleguide.md`: Front matter, heading hierarchy, code fences
- `rules/performance-best-practices.md`: Optimize after measurement
- `rules/security-standards-owasp.md`: OWASP Top 10 alignment
- `rules/software-architecture-patterns.md`: Pattern selection, boundaries

### Extended Standards (apply based on task domain)
- `rules/code-documentation-standards.md`: Comment WHY, not WHAT
- `rules/react-development-standards.md`: React component patterns
- `rules/typescript-styleguide.md`: TypeScript typing & consistency
- `rules/web-accessibility-standards.md`: WCAG 2.2 AA validation
- `rules/backend-development-standards.md`: Service/controller patterns
- `rules/frontend-development-standards.md`: Frontend patterns
- `rules/ui-ux-design-standards.md`: Layout/interaction standards
- `rules/database-standards.md`: Schema/migration standards
- `rules/stored-procedure-standards.md`: Stored procedure patterns
- `rules/dotnet-architecture-standards.md`: .NET architecture patterns

**Selection**: Apply only standards matching task domain. Most specific overrides general.

**>>> ALWAYS: Execute Quality Evaluation. <<<**

## Quality Evaluation

### 4-Tier Prototype Assessment

| Tier | Dimension | Gate | Conditional |
|------|-----------|------|-------------|
| T1 | Build Success + Local Launch Ready | MUST PASS | No (always required) |
| T2 | Validation Stories Coverage | MUST=100% | No (always required) |
| T3 | Documentation Complete + Business Alignment | ≥80% | Yes (skip for <3 user journeys) |
| T4 | Timeline Adherence | ≥80% | Yes (skip if user waives time constraint) |

### Tier Definitions

**T1 - Build & Launch (REQUIRED)**
- Prototype must build without errors (npm run build exit 0)
- Prototype must launch and be accessible (npm start, URL responds)
- Required source files exist (index.html, app.js, style.css)
- Gate: MUST PASS (execution halts if build/launch fails)

**T2 - Validation Stories (REQUIRED)**
- All user journeys from mvp-scope-and-journeys.md must be implemented
- Each validation story enables hypothesis testing
- Gate: MUST=100% (all stories implemented)

**T3 - Documentation & Alignment (CONDITIONAL)**
- Skip Condition: <3 user journeys defined (simple prototypes need minimal docs)
- Documentation: README.md, deployment-guide.md, validation procedures
- Business alignment: Features map to hypothesis objectives
- Gate: ≥80% (or SKIPPED if condition met)

**T4 - Timeline Adherence (CONDITIONAL)**
- Skip Condition: User explicitly waives 80-hour constraint
- Hours tracked and documented ≤80 total
- Time breakdown by phase included
- Priority scoping applied correctly (if requirements exceeded 80 hours)
- Gate: ≥80% (or SKIPPED if condition met)

### Executable Verification

#### T1: Build & Launch
| Check | Command | Expected | Actual | Status |
|-------|---------|----------|--------|--------|
| Build | `npm run build` or project build | exit 0 | [result] | PASS/FAIL |
| Launch | `npm start` or launch cmd | exit 0 | [result] | PASS/FAIL |
| Files | `ls mvp/src/` | index.html, app.js, style.css | [result] | PASS/FAIL |
| URL Access | curl/fetch localhost:3000 | 200 OK | [result] | PASS/FAIL |

#### T2: Validation Stories
| Check | Threshold | Actual | Score |
|-------|-----------|--------|-------|
| Stories Implemented | = defined count | [N]/[M] | [X]% |
| Features Mapped | = objective count | [N]/[M] | [X]% |

```
Validation Coverage = (implemented journeys / defined journeys) × 100%
T2 Score = Validation Coverage (MUST = 100%)
```

#### T3: Documentation & Alignment [CONDITIONAL]
Status: [EVALUATED / SKIPPED - <3 journeys]

| Check | Threshold | Actual | Score |
|-------|-----------|--------|-------|
| README.md | exists | [yes/no] | [computed] |
| deployment-guide.md | exists | [yes/no] | [computed] |
| validation-report.md | exists | [yes/no] | [computed] |
| Feature-Objective Mapping | 100% | [N]/[M] | [X]% |

```
Doc Score = (docs present / 3) × 100%
Alignment Score = (aligned features / total features) × 100%
T3 Score = Average(Doc Score, Alignment Score)
```

#### T4: Timeline Adherence [CONDITIONAL]
Status: [EVALUATED / SKIPPED - user waived]

| Check | Threshold | Actual | Score |
|-------|-----------|--------|-------|
| Total Hours | ≤80 | [hours] | [computed] |
| Time Breakdown | documented | [yes/no] | PASS/FAIL |
| Phase Distribution | balanced | [yes/no] | PASS/FAIL |
| Priority Scoping | applied if needed | [yes/no/N/A] | PASS/FAIL |

```
Timeline Score = (80 - actual_hours) ≥ 0 ? 100% : max(0, (160 - overage) / 160 × 100%)
Priority Compliance = (scope exceeded 80h AND priority cut-off applied) ? 100% : (scope ≤80h) ? 100% : 0%
T4 Score = Average(Timeline Score, Priority Compliance)
```

### Overall Assessment

| Tier | Dimension | Score | Gate | Result |
|------|-----------|-------|------|--------|
| T1 | Build & Launch | [PASS/FAIL] | MUST | [P/F] |
| T2 | Validation Stories | [X]% | 100% | [P/F] |
| T3 | Docs & Alignment | [X]% | ≥80% | [P/F/S] |
| T4 | Timeline | [X]% | ≥80% | [P/F/S] |

**Verdict**: [PASS / CONDITIONAL PASS / FAIL]

**Top 3 Weaknesses:**
1. [Tier] - [Dimension] ([X]%): [Specific issue]
2. [Tier] - [Dimension] ([X]%): [Specific issue]
3. [Tier] - [Dimension] ([X]%): [Specific issue]

**Critical Failures**: [List MUST gates that failed, or "None"]

---

*This workflow creates validation prototypes for hypothesis testing, not complete applications. Focus is on rapid validation through minimal working software.*