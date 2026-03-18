---
description: Standalone quality evaluation workflow that validates any workflow output against templates and requirements with conditional checks per workflow type
auto_execution_mode: 1
---

# Standalone Output Evaluator

As an expert Quality Assurance Engineer, perform comprehensive post-hoc quality evaluation on workflow outputs. This workflow validates template adherence, content patterns, cross-reference traceability, and semantic quality with conditional assessment logic per workflow type.

## Input Parameters

### $OUTPUT_FILE (Mandatory)
Path to the generated artifact to evaluate (e.g., `.propel/context/docs/epics.md`)

### $TEMPLATE_FILE (Optional)
Path to the template file. If not provided, auto-detected from output file path.

### $SCOPE_FILES (Optional)
Comma-separated input scope files. If not provided, auto-detected from `.propel/context/docs/` based on workflow type.

### --workflow-type (Optional)
Explicit workflow type override. If not provided, auto-detected from output file name.

**Supported Workflow Types:**
- spec, design, epics, model, figma-spec, codebase
- user-story, task, bug-task
- test-plan, test-workflow, e2e-workflow, unit-test
- task-review, ui-review, code-review

## Output
- Print evaluation report to console with 4-tier quality assessment
- **Scoring Scale**: 0-100 (percentage-based scoring for all tiers)
- **Do not save as file** (console output only)

## Auto-Detection Logic

### Workflow Type Detection from Output File Path

```
.propel/context/docs/spec.md → spec
.propel/context/docs/design.md → design
.propel/context/docs/epics.md → epics
.propel/context/docs/models.md → model
.propel/context/docs/figma_spec.md → figma-spec
.propel/context/docs/codeanalysis.md → codebase
.propel/context/tasks/us_*/us_*.md → user-story
.propel/context/tasks/*/task_*.md → task
.propel/context/tasks/bug_*/task_*.md → bug-task
.propel/context/docs/test_plan_*.md → test-plan
.propel/context/test/tw_*.md → test-workflow
.propel/context/test/e2e_*.md → e2e-workflow
.propel/context/tasks/*/unittest/*.md → unit-test
.propel/context/tasks/*/reviews/task-review-*.md → task-review
.propel/context/tasks/*/reviews/ui-review-*.md → ui-review
.propel/code-reviews/review_*.md → code-review
```

### Template Auto-Detection

```yaml
spec → .propel/templates/requirements-template.md
design → .propel/templates/design-specification-template.md
epics → .propel/templates/epics-template.md
model → .propel/templates/design-model-templates.md
figma-spec → .propel/templates/figma-specification-template.md
codebase → .propel/templates/codebase-analysis-template.md
user-story → .propel/templates/user-story-template.md
task → .propel/templates/task-template.md
bug-task → .propel/templates/issue-triage-template.md
test-plan → .propel/templates/test-plan-template.md
test-workflow → .propel/templates/automated-testing-template.md
e2e-workflow → .propel/templates/automated-e2e-template.md
unit-test → .propel/templates/unit-test-template.md
task-review → .propel/templates/task-analysis-template.md
ui-review → .propel/templates/design-analysis-template.md
code-review → .propel/templates/code-review-template.md
```

### Scope Files Auto-Detection

```yaml
spec: [input scope doc provided by user]
design: [spec.md]
epics: [spec.md, design.md]
model: [spec.md, design.md]
figma-spec: [spec.md]
codebase: [existing codebase]
user-story: [epics.md, spec.md]
task: [us_*.md, design.md]
bug-task: [bug report]
test-plan: [spec.md, design.md]
test-workflow: [spec.md]
e2e-workflow: [spec.md]
unit-test: [us_*.md]
task-review: [task_*.md]
ui-review: [task_*.md]
code-review: [changed files]
```

## Execution Flow

### Phase 1: Input Processing
1. Parse $OUTPUT_FILE path
2. Auto-detect workflow type from file path pattern
3. Auto-detect template file based on workflow type
4. Auto-detect scope files based on workflow type
5. Override with explicit parameters if provided
6. Log detected configuration for transparency

### Phase 2: Five-Tier Evaluation

## Tier 1: Template Structure Adherence

**Goal:** Verify output contains all required template sections and no additional/deferred sections

**Criteria:**
| Check | Description | Impact |
|-------|-------------|--------|
| Missing Sections | Template sections not present in output | -20 per section |
| Additional Sections | Output sections not defined in template | -10 per section |

**Execution:**
```
1. Grep("^## ", template_file) → expected_sections
2. Grep("^## ", output_file) → actual_sections
3. missing_sections = expected_sections - actual_sections
4. extra_sections = actual_sections - expected_sections
5. Score = 100 - (20 × missing_count) - (10 × extra_count)
```

**Gate:** MUST = 100%

**Evidence:** List missing sections and additional sections (deferred from template)

---

## Tier 2: Content Pattern Verification (Conditional per Workflow Type)

### IF workflow_type == "spec":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| FR Requirements | `FR-\d{3}` | ≥ 5 | Functional requirements count |
| Use Cases | `UC-\d{3}` | ≥ 3 | Use case count |
| PlantUML Diagrams | ` ```plantuml` | ≥ UC_count | Diagram coverage |
| MUST Statements | `MUST\s+` | ≥ FR_count | Requirement clarity |
| UNCLEAR Tags | `\[UNCLEAR\]` | Note count | Ambiguity tracking |

### ELSE IF workflow_type == "design":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| NFR Requirements | `NFR-\d{3}` | ≥ 3 | Non-functional requirements |
| TR Requirements | `TR-\d{3}` | ≥ 2 | Technical requirements |
| DR Requirements | `DR-\d{3}` | ≥ 1 | Data requirements |
| Tech Stack Table | `Technology Stack` section exists | 1 | Stack documented |
| AI Consideration | IF no `[AI-CANDIDATE]` tags in spec.md, verify "AI Consideration: Not applicable" present | - | Deterministic confirmation |
| AIR Requirements | IF spec.md has `[AI-CANDIDATE]` or `[HYBRID]`, verify `AIR-\d{3}` exists | ≥ 3 | AI requirements when applicable |

### ELSE IF workflow_type == "epics":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| Epic IDs | `EP-\d{3}` | ≥ 1 | Epic count |
| Mapped FR | `FR-\d{3}` | = source count from spec.md | Requirement coverage |
| Mapped NFR | `NFR-\d{3}` | = source count from design.md | Technical coverage |
| Business Value | `Business Value:` | = EP count | Value statements |
| UI Impact | `UI Impact:` | = EP count | UI assessment |
| EP-TECH Present | IF green-field detected | 1 | Infrastructure epic |
| EP-DATA Present | IF entities in design.md OR DR ≥ 2 | 1 | Data layer epic |

### ELSE IF workflow_type == "model":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| PlantUML Blocks | `@startuml` | ≥ 2 | Diagram count |
| Mermaid Blocks | ` ```mermaid` | ≥ 1 | Alternative diagrams |
| Sequence Diagrams | `@startuml.*sequence` | = UC count from spec.md | Use case coverage |

### ELSE IF workflow_type == "figma-spec":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| UXR Requirements | `UXR-\d{3}` | ≥ 5 | UX requirements |
| Screen IDs | `SCR-\d{3}` | ≥ 3 | Screen inventory |
| UXR-to-SCR Mapping | Check table completeness | All UXR map to screens | Coverage validation |
| Persona Coverage | Persona matrix exists | 1 | Persona documentation |

### ELSE IF workflow_type == "user-story":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| Story Format | `As a.*I want.*so that` | 1 | INVEST format |
| GWT Criteria | `Given.*When.*Then` | ≥ 3 | Acceptance criteria |
| Edge Cases | Edge Cases section non-empty | 1 | Boundary handling |
| Parent Epic | Parent Epic reference populated | 1 | Traceability |
| Requirement Tags | Requirement Tags populated | 1 | Requirements mapping |
| Visual Design Context | IF UI-impacting, verify Visual Design Context populated | - | Design references |
| Wireframe Status | IF UI-impacting, verify wireframe status (AVAILABLE/PENDING/EXTERNAL/N/A) | 1 | Wireframe tracking |

### ELSE IF workflow_type == "task":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| AC Extracted | Acceptance Criteria from user story | Present | Requirements trace |
| Implementation Plan | Section non-empty | 1 | Execution plan |
| Expected Changes | Table populated | 1 | Impact documentation |
| Checklist Items | Implementation checklist | ≤ 8 | Task sizing |
| Technology Stack | Table populated | 1 | Stack compliance |
| Design References | IF UI Impact = Yes, verify Design References table populated | - | UI specifications |
| AI References | IF AI Impact = Yes, verify AI References table populated | - | AI specifications |

### ELSE IF workflow_type == "bug-task":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| Root Cause | Root Cause Analysis populated | 1 | Diagnosis complete |
| Reproduction Steps | Steps to Reproduce populated | 1 | Reproducibility |
| Impact Assessment | Impact Assessment populated | 1 | Severity documented |
| Fix Overview | Fix Overview populated | 1 | Solution defined |
| Expected Changes | Table populated | 1 | Change documentation |

### ELSE IF workflow_type == "test-plan":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| Test Cases | `TC-` | ≥ 5 | Test coverage |
| Functional Tests | Functional test cases exist | 1 | Core functionality |
| NFR Tests | IF NFR-XXX in scope, verify NFR test cases exist | - | Non-functional testing |
| E2E Journey Tests | E2E journey test cases exist | 1 | User flows |
| AI Test Cases | IF AIR-XXX in scope, verify AI test cases exist | - | AI component testing |
| Traceability Matrix | Matrix populated | 1 | Coverage mapping |

### ELSE IF workflow_type == "test-workflow":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| Test Cases | `TC-` | ≥ 3 | Test count |
| Test Types | HP, EC, ER types present | 3 types | Coverage variety |
| YAML Steps | YAML steps format for each test | = TC count | Automation ready |
| Page Objects | Page Objects section populated | 1 | Maintainability |

### ELSE IF workflow_type == "e2e-workflow":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| Journey Flow | Journey Flow table populated | 1 | Flow documentation |
| Phase Steps | Phase-based step structure | Present | Organization |
| Session Requirements | Section populated | 1 | Environment setup |

### ELSE IF workflow_type == "unit-test":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| Test Cases | Test case entries | ≥ 3 | Coverage count |
| GWT Format | Given/When/Then format | Present | Clarity standard |
| Mocking Strategy | Mocking Strategy table populated | 1 | Test isolation |
| Coverage Target | Coverage Target section populated | 1 | Quality goal |
| AI Test Cases | IF AIR-XXX in scope, verify AI test cases section exists | - | AI testing |

### ELSE IF workflow_type == "task-review":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| Verdict | Verdict (Pass/Conditional Pass/Fail) present | 1 | Decision documented |
| Traceability Matrix | Traceability Matrix populated | 1 | Coverage validation |
| Fix Plan | IF Fail verdict, Fix Plan section present | - | Remediation plan |

### ELSE IF workflow_type == "ui-review":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| Summary | Summary populated | 1 | Overview present |
| Findings Structured | Blockers/High/Medium/Nitpicks | 4 sections | Severity classification |
| Testing Coverage | Metrics present | 1 | Coverage documented |

### ELSE IF workflow_type == "code-review":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| Executive Summary | Summary populated | 1 | Overview present |
| Findings Summary | Table with severity counts | 1 | Issue quantification |
| Severity Groups | Issue sections | Present | Organization |
| OWASP Matrix | OWASP Top 10 matrix populated | 1 | Security validation |
| AI Security | IF AI changes detected, verify AI/LLM Security Assessment section present | - | AI security review |

### ELSE IF workflow_type == "codebase":
| Pattern | Regex | Threshold | Description |
|---------|-------|-----------|-------------|
| Tech Stack Inventory | Tables populated | 1 | Stack documented |
| Source Organization | Tree populated | 1 | Structure mapped |
| API Inventory | Inventory populated | 1 | Endpoints documented |
| Security Assessment | Section present | 1 | Security analyzed |

**Scoring:**
```
FOR each pattern:
  actual_count = grep(pattern, output_file)
  pattern_score = (actual_count / threshold) × 100% (capped at 100%)
Tier 2 Score = Average of all pattern scores
```

**Gate:** ≥ 80%

---

## Tier 3: Cross-Reference Traceability (Conditional)

### IF workflow_type IN ["epics", "user-story", "task", "test-plan"]:

**Requirements Traceability:**
```
1. Read scope files → Extract all requirement IDs (FR, NFR, TR, DR, UXR, AIR)
2. **FILTER OUT [UNCLEAR] requirements** → These should NOT be in coverage calculations
3. valid_source_reqs = all_requirements - unclear_requirements
4. Read output file → Extract all referenced requirement IDs
5. coverage = (referenced ∩ valid_source_reqs) / valid_source_reqs × 100%
6. orphaned = valid_source_reqs - referenced (requirements not covered)
7. hallucinated = referenced - valid_source_reqs (IDs not in source or marked [UNCLEAR])
```

**Special Check for [UNCLEAR]:**
```
unclear_in_output = grep("[UNCLEAR]", output_file)
IF unclear_in_output > 0:
  FLAG: "Output contains [UNCLEAR] requirements - these should be in Backlog Refinement section only, not mapped to epics/stories/tasks"
```

**Gate:** coverage ≥ 80%, hallucinated = 0, unclear_in_output = 0 (or only in Backlog Refinement section)

### IF workflow_type == "model":

**Use Case Coverage:**
```
1. Read spec.md → Extract UC-XXX list
2. Read output file → Extract sequence diagram UC references
3. UC coverage = (diagrams with UC) / (total UC) × 100%
```

**Gate:** coverage ≥ 80%

### IF workflow_type == "task":

**Acceptance Criteria Trace:**
```
1. Read parent user story → Extract acceptance criteria
2. Read task → Check acceptance criteria section references them
```

**Gate:** All parent AC referenced

#### ELSE 
- Skip without gate and scoring as it is not applicable

**Scoring:**
```
Tier 3 Score = coverage percentage
```

---

## Tier 4: Semantic Quality (All Types)

**Using Sequential-Thinking MCP (with fallback to structured analysis):**

### Ambiguity Check
Flag sections with vague language ("appropriate", "as needed", "various") without specific criteria.

### Completeness Check
Identify placeholder values: [TBD], [TODO], [placeholder], [FILL IN]

### Consistency Check
Verify IDs referenced in one section match IDs defined in another.

### Contradiction Check
Identify conflicting statements within the document.

**Scoring:**
```
issue_count = ambiguity + placeholders + inconsistencies + contradictions
Tier 4 Score = MAX(0, 100 - (10 × issue_count))
```

**Gate:** ≥ 80%

---


## Output Format

```
===========================================================
         QUALITY EVALUATION: [workflow_type]
===========================================================

File Evaluated: [output file path]
Template Used:  [template file path]
Scope Files:    [comma-separated scope file paths]
Workflow Type:  [auto-detected or specified]

-----------------------------------------------------------
TIER 1: Template Structure
-----------------------------------------------------------
| Expected Section        | Found | Status  |
|-------------------------|-------|---------|
| [section name]          | Yes   | PASS    |
| [section name]          | No    | MISSING |

Score: [X]%  |  Gate: MUST=100%  |  Result: [PASS/FAIL]

-----------------------------------------------------------
TIER 2: Content Patterns ([workflow_type])
-----------------------------------------------------------
| Pattern         | Expected | Found | Score   |
|-----------------|----------|-------|---------|
| [pattern name]  | ≥ N      | M     | [X]%   |

Score: [X]%  |  Gate: ≥80%  |  Result: [PASS/FAIL]

-----------------------------------------------------------
TIER 3: Cross-Reference Traceability
-----------------------------------------------------------
Source Requirements: [N]
Referenced in Output: [M]
Coverage: [X]%
Orphaned: [list or "None"]
Hallucinated: [list or "None"]

Score: [X]%  |  Gate: ≥80%  |  Result: [PASS/FAIL]

-----------------------------------------------------------
TIER 4: Semantic Quality
-----------------------------------------------------------
| Check          | Issues Found | Details            |
|----------------|-------------|--------------------|
| Ambiguity      | [N]         | [list or "Clean"]  |
| Placeholders   | [N]         | [list or "Clean"]  |
| Consistency    | [N]         | [list or "Clean"]  |
| Contradictions | [N]         | [list or "Clean"]  |

Score: [X]%  |  Gate: ≥80%  |  Result: [PASS/FAIL]

-----------------------------------------------------------
OVERALL
-----------------------------------------------------------
| Tier | Score | Gate   | Result |
|------|-------|--------|--------|
| T1   | [X]%  | 100%   | [P/F]  |
| T2   | [X]%  | ≥80%   | [P/F]  |
| T3   | [X]%  | ≥80%   | [P/F]  |
| T4   | [X]%  | ≥80%   | [P/F]  |

Overall Score: [Weighted Average]%
Verdict: [PASS / CONDITIONAL PASS / FAIL]

Top 3 Weaknesses:
1. [Dimension] ([X]%): [Specific issue]
2. [Dimension] ([X]%): [Specific issue]
3. [Dimension] ([X]%): [Specific issue]

===========================================================
```

*This standalone evaluator provides comprehensive post-hoc quality assessment with conditional logic per workflow type, catching issues the inline evaluations might miss.*
