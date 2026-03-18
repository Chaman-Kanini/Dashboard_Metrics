---
description: Decomposes functional requirements into feature-level and E2E test workflow specifications for Playwright automation
auto_execution_mode: 1
---

# Automation Test Workflow Generator

As an expert QA Engineer and Test Automation Specialist, generate comprehensive test workflows from functional requirements. This command decomposes Use Cases into Happy Path, Edge Case, and Error test cases.

## Input Parameters

### $ARGUMENTS (Optional)
**Accepts:** spec.md path | Feature name | Use Case ID (UC-XXX)
**Default:** `.propel/context/docs/spec.md`

### --type (Optional)
**Accepts:** `feature` | `e2e` | `both`
**Default:** `both`

| Value | Behavior |
|-------|----------|
| `feature` | Generate HP, EC, ER tests only |
| `e2e` | Generate E2E journey tests only |
| `both` | Generate all test types (default) |

### Input Processing Instructions

**Step 1: Determine Source**
| Input | Action |
|-------|--------|
| Empty | Use `.propel/context/docs/spec.md` |
| File path | Read specified file |
| `UC-001` | Find UC in spec.md |
| `Login` | Search spec.md for matching UC |

**Step 2: Validate Input**
- If file path: Verify file exists
- If UC ID: Verify UC-XXX exists in spec.md
- If feature name: Find matching Use Case by name

## Output

| --type Value | Output File | Template Used |
|--------------|-------------|---------------|
| `feature` | `.propel/context/test/tw_<feature>.md` | `automated-testing-template.md` |
| `e2e` | `.propel/context/test/e2e_<journey>.md` | `automated-e2e-template.md` |
| `both` | Both files | Both templates |

- **Print** (console only):
  - Rules used (bulleted list)
  - Evaluation Scores (table)
  - Summary (<100 words)

**Note:** **File Handling**: IF file exists → UPDATE changed sections only (delta mode). IF file does not exist → CREATE complete file.

## Execution Flow

### Deep Research Methodology

**MCP Tools Required:**
- `mcp__sequential-thinking__sequentialthinking` - Systematic analysis
- `mcp__context7__resolve-library-id` - Pin Playwright version
- `mcp__context7__get-library-docs` - Fetch locator documentation

**Fallback:** If MCP unavailable, use structured iterative analysis.

### Step 1: Requirements Analysis
**Use:** `mcp__sequential-thinking__sequentialthinking`

1. Read `.propel/context/docs/spec.md`
2. Extract all Use Cases (UC-XXX)
3. Extract Functional Requirements (FR-XXX)
4. For each UC, identify:
   - Primary actor
   - Preconditions
   - Main success scenario
   - Alternative flows
   - Acceptance criteria

### Step 2: Technology Stack Detection
**Use:** `mcp__context7__resolve-library-id`, `mcp__context7__get-library-docs`

1. Resolve Playwright library ID
2. Fetch current Playwright locator patterns
3. Detect frontend framework (React/Angular/Vue) if applicable
4. Pin versions for consistent script generation

### Step 3: Test Case Decomposition (--type feature or both)
**Use:** `mcp__sequential-thinking__sequentialthinking`
**Condition:** Execute when --type is `feature` or `both`

For EACH Use Case, generate exactly 3 test types:

| Type | ID Pattern | Purpose | Priority |
|------|------------|---------|----------|
| Happy Path | TC-[UC]-HP-001 | Normal successful flow | P0 |
| Edge Case | TC-[UC]-EC-001 | Boundary conditions | P1 |
| Error Case | TC-[UC]-ER-001 | Invalid inputs/failures | P1 |

**Before writing test cases, list all tests:**
| TC-ID | Summary | Type |
|-------|---------|------|
| TC-UC001-HP-001 | [Summary] | happy_path |
| TC-UC001-EC-001 | [Summary] | edge_case |
| TC-UC001-ER-001 | [Summary] | error |

**Now expand each test listed above.**

### Step 3.5: E2E Journey Identification (--type e2e or both)
**Use:** `mcp__sequential-thinking__sequentialthinking`
**Condition:** Execute when --type is `e2e` or `both`

1. Identify user journeys that span multiple Use Cases
2. Map journey: UC-001 → UC-002 → UC-003 (e.g., Login → Dashboard → Create Order)
3. Define session continuity requirements
4. Identify shared test data across journey steps

**E2E Journey Pattern:**
| Journey ID | Name | UC Chain | Business Value |
|------------|------|----------|----------------|
| E2E-001 | [JOURNEY_NAME] | UC-001 → UC-002 → UC-003 | [VALUE] |

**E2E Test ID Pattern:** TC-E2E-[JOURNEY]-001

### Step 4: Selector Strategy Planning
**Use:** `mcp__context7__get-library-docs` + `mcp__sequential-thinking__sequentialthinking`

1. Fetch latest Playwright locator best practices
2. Map UI elements to role-based selectors
3. Document fallback selectors (testid) for custom components
4. Follow priority: getByRole > getByTestId > getByLabel > CSS

### Step 5: Template Population

| --type Value | Template | Output |
|--------------|----------|--------|
| `feature` | `.propel/templates/automated-testing-template.md` | Feature test workflow |
| `e2e` | `.propel/templates/automated-e2e-template.md` | E2E journey workflow |
| `both` | Both templates | Both outputs |

For each test case, include:
- step_id, action, target, expect
- Test data (inline YAML)
- Preconditions

### Step 6: Output Generation

| --type Value | Output File |
|--------------|-------------|
| `feature` | `.propel/context/test/tw_<feature>.md` |
| `e2e` | `.propel/context/test/e2e_<journey>.md` |
| `both` | Both files |

## Guardrails

- `rules/playwright-testing-guide.md`: Test independence, wait strategies
- `rules/playwright-typescript-guide.md`: Code quality, assertions
- `rules/playwright-standards.md`: Locator priority, anti-patterns
- `rules/language-agnostic-standards.md`: KISS, YAGNI
- `rules/markdown-styleguide.md`: Front matter, heading hierarchy

**>>> ALWAYS: Execute Quality Evaluation. Follow the 4-tier evaluation framework instructions to evaluate the outcomes. <<<**

## Quality Evaluation

- **Invoke**: `.windsurf/workflows/evaluate-output.md`
  - **$OUTPUT_FILE**: `.propel/context/test/tw_*.md`
  - **$SCOPE_FILES**: `.propel/context/docs/spec.md`
  - **--workflow-type**: `test-workflow`

---

*Generates test workflow specifications for Playwright automation script generation.*
