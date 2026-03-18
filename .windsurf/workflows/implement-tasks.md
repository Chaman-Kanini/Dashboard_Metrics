---
description: Implements features, fixes bugs, and completes development tasks using comprehensive task files with systematic validation and quality control
auto_execution_mode: 1
---

# Unified Task Executor
As a Software Engineer expert in Full Stack development (polyglot developer), implement the task. This unified command handles all task implementation scenarios with consistent quality and adhering to core principles and standards.

## Input Parameter (Task File)s: $ARGUMENTS (Mandatory)

Implement features, fix bugs, or complete development tasks using comprehensive task files. This command ensures systematic, high-quality implementation with thorough validation and quality control.

**Optional Parameters:**
- `--skip-history`: Skip findings registry lookup for faster execution (default: false)

## Output
- Added / updated source files
- Print the following: 
    - List of rules adopted by the workflow in bulleted format
    - Evaluation Scores in tabular format with average score. 
    - Evaluation summary (less than 100 words).
    - Mark the ToDo tasks as completed ([x]).
    **Do not save as file.** (console output only)

## Execution Flow

### Core Principles
- Load and comprehend the complete task file before starting implementation
- Understand all context by reviewing docs/spec.md, docs/design.md, docs/models.md and existing codebase
- Verify task completion status - terminate if already completed with "All tasks were implemented"
- Follow all task instructions and extend research when additional context is needed
- Update task file sections based on current codebase state and implementation progress
- Split complex implementations by technology stack (frontend, backend, database) when applicable
- Use TodoWrite tool for systematic progress tracking throughout implementation
- Request explicit confirmation for destructive changes that affect multiple files
- Validate each step before proceeding to maintain code quality and functionality
- **Critical:** Do not copy-paste publicly available code as-is - adapt, understand, and integrate following project patterns
- All code must be understood, adapted, and validated by the team.
- Existing codebase pattern compliance is mandatory for quality implementation.

### Deep Implementation Methodology

Optimize for implementation success and code quality over execution speed. Use systematic approach with comprehensive validation.

*** 1. Task Comprehension and Planning ***
- **Task Analysis**: Parse complete task file including context, requirements, and validation criteria
- **UI Impact Assessment**: Determine if task requires UI changes and load design assets accordingly
- **Design Asset Review**: Load Figma links OR design images from task context (UI tasks only)
- **Visual Specification Analysis**: Extract pixel-perfect implementation requirements from design assets
- **Component Design Mapping**: Map visual designs to code components (UI tasks only)
- **Design System Integration**: Apply design tokens and style specifications (UI tasks only)
- **Codebase Assessment**: Review existing code patterns, conventions, and integration points
- **Impact Analysis**: List cascading effects by answering: (1) What existing features touch this code? (2) What APIs/interfaces change? (3) What tests need updating?
- **Pattern Recognition**: Identify existing implementation patterns to follow for consistency
- **Dependency Mapping**: Understand task dependencies and execution order requirements

*** 1b. Historical Context Check *** (Optional: skip with --skip-history)

**Selective Registry Lookup**:
- Grep `.propel/learnings/findings-registry.md` for task's target files ONLY
- Extract matching entries (max 5 most recent per file)
- Skip if no matches found

**Console Warning** (if matches found):
Display compact warning, do NOT add to context window beyond warning display:
```
HISTORICAL ISSUES DETECTED
File: <path>
Previous findings: <count>
  - [<date>] <category>: <issue>
Recommendation: Review past issues before modifying.
```

*** 2. Implementation Planning ***
- **Deep Reasoning Phase**: For each requirement, answer: (1) What files need changes? (2) What is the expected behavior? (3) What are the edge cases? (4) What tests verify correctness?
- **Task Breakdown**: Use TodoWrite to create detailed, trackable implementation steps
- **Technology Separation**: Plan frontend, backend, and database components independently when applicable
- **Restoration Points**: Plan strategic code backup points for easy rollback if needed
- **Validation Strategy**: Define testing and validation approach for each implementation step

*** 3. Quality Assurance Integration ***
- **Code Standards**: Ensure adherence to existing coding standards and project conventions
- **Test Strategy**: Plan unit test creation/updates as mandatory part of implementation
- **Error Handling**: Implement comprehensive error handling following project patterns

### Essential Project Intelligence Integration

*** 1. Reference Materials Analysis ***
- **Codebase Patterns**: Follow existing code organization, naming conventions, and architectural decisions
- **Documentation Standards**: Maintain consistency with existing documentation and inline comments
- **Testing Patterns**: Follow established testing strategies and validation approaches

*** 2. External Code Usage Policy ***
When referencing external code (Stack Overflow, GitHub, documentation examples):
- **Understand** the code completely before adapting
- **Verify** license compatibility (avoid GPL/AGPL in proprietary projects)
- **Audit** for security vulnerabilities and code quality
- **Adapt** to match existing project patterns and conventions
- **Document** the source and rationale for adaptation
- **Test** thoroughly as if it were original code

Why this matters:
- **Legal**: Incompatible licenses can create IP issues
- **Security**: Public code may contain vulnerabilities or malicious code
- **Quality**: May not meet enterprise standards
- **Maintainability**: Team must understand all code in production
- **Customization**: Rarely fits requirements without modification

### Systematic Implementation Framework

*** Phase 1: Task Loading and Preparation ***
**Task File Analysis**
- Load and parse complete task file structure
- Extract all requirements, context, and validation criteria
- Identify completion status of existing todo items
- Update task understanding based on current codebase state
- Map visual components to existing code patterns (UI tasks only)
- Identify design system tokens for consistent styling (UI tasks only)
- Analyze existing codebase for patterns and integration points
- Use `mcp__context7__resolve-library-id` (Context7 MCP) to lock framework/library versions present in the task and codebase before fetching guidance
- Use `mcp__context7__get-library-docs` (Context7 MCP) for technology-specific, version-specific documentation, code examples, design principles and coding standards
- Perform additional web research if task context requires updates
- Document any gaps or additional research findings
**Context Gathering** (if available)

**Selective Context Loading Protocol:**
Load ONLY the reference documents relevant to this task's technology layer and requirements.

**For non-UI tasks (UI Impact = No):**
- SKIP figma_spec.md, designsystem.md, and wireframe files entirely

**For UI tasks (UI Impact = Yes):**
- Load figma_spec.md for UXR-XXX requirements and screen specifications
- Load designsystem.md for design tokens
- Load wireframe files from task's Design References table

**Targeted Reading Strategy:**
- From spec.md: Extract ONLY the FR-XXX and UC-XXX IDs listed in this task's Requirement Reference
  - **CRITICAL**: If any requirement is tagged [UNCLEAR], HALT execution and notify user
- From design.md: Extract ONLY Technology Stack and NFR/TR/DR mapped to this task
  - **CRITICAL**: If any NFR/TR/DR is tagged [UNCLEAR], HALT execution and notify user
- From models.md: Read ONLY the sequence diagram for the UC-XXX referenced by this task
- From epics.md: Read ONLY the parent epic context
- From figma_spec.md (if UI task): Extract ONLY UXR-XXX listed in task
  - **CRITICAL**: If any UXR-XXX is tagged [UNCLEAR], HALT execution and notify user

**[UNCLEAR] Requirement Gate:**
- Before implementing ANY task, validate that ZERO requirements are tagged [UNCLEAR]
- If [UNCLEAR] found: Display message "Task blocked: Requirements [list IDs] require clarification. Run requirement refinement workflow first."
- Do NOT proceed with implementation until all requirements are clarified

**Standard Context:**
- Review `.propel/context/docs/spec.md` for FR-XXX requirements (UXR-XXX NOT in spec.md)
- Review `.propel/context/docs/design.md` for NFR-XXX, TR-XXX, DR-XXX requirements
- Review `.propel/context/docs/epics.md` for epic context and requirement groupings
- Review `.propel/context/docs/models.md` for architectural views and sequence diagrams
- Review `.propel/context/docs/codeanalysis.md` for existing system understanding
- Review `.propel/context/docs/figma_spec.md` for UXR-XXX requirements (UI tasks only)
**Load Design Reference** (if available, UI tasks only)
- Read `.propel/context/docs/figma_spec.md` for screen specifications, state requirements, and flow definitions
- Read `.propel/context/docs/designsystem.md` for design tokens (colors, typography, spacing) and component mappings
- Load Figma URLs OR design images from design reference sections
- Load wireframe files from task's Design References table (supports HTML, PNG, JPG, or external URL)
- Use design-to-code mappings from `designsystem.md`
- Extract pixel-perfect requirements from `figma_spec.md` screen state specifications
- Search for "[technology] best practices [current year]" to find recent guides
- Look for popular repositories on GitHub that exemplify good practices

**Architectural Context Loading** (if available)
- Read `.propel/context/docs/models.md` for:
  - Sequence diagrams relevant to the task's use cases
  - Component architecture for integration understanding
  - Data flow diagrams for data handling
  - ERD for entity relationships

**AI Context Loading** (if task maps to AIR-XXX requirements)
- Check task's AI References section for AI Impact = Yes
- If AI Impact = Yes, load the following:
  - Read prompt templates from task's Prompt Template Path (e.g., `prompts/[feature]/`)
  - Load guardrails configuration from task's Guardrails Config path
  - Verify AI/ML stack versions match design.md technology stack
  - Review `.propel/context/docs/design.md` for:
    - AIR-XXX requirements (functional, quality, safety, operational)
    - AI Pattern selection (RAG / Tool Calling / Fine-tuning / Hybrid)
    - AI Component Stack (Model Provider, Vector Store, AI Gateway)
- Extract AI-specific acceptance criteria from AIR requirements:
  - Quality thresholds (hallucination rate, latency targets)
  - Safety requirements (PII redaction, ACL enforcement)
  - Operational constraints (token budget, circuit breakers)

*** Phase 2: Implementation Planning ***
**Strategic Planning**
- Create comprehensive TodoWrite plan with all implementation steps
- Break down complex tasks into manageable, testable units
- Plan technology stack separation (frontend/backend/database) when needed
- Identify precise code modification targets using line numbers, function names, variables
- Replace clever code with obvious code
- Eliminate nested structures where possible
- Use early returns to reduce indentation

- **MANDATORY**: Include "Generate evaluation metrics report" as final todo item before task completion

**Quality Planning**
- Define validation commands and success criteria for each step
- Plan unit test creation/updates for all new functionality
- Establish restoration points for complex code changes
- Define completion criteria and validation gates

*** Phase 3: Systematic Implementation ***

**Component Name Validation** (unit test tasks only):

**Detection:**
```
IF task file contains "## Components Under Test" table:
  Apply validation
ELSE:
  Skip validation
```

**Validation Steps:**

1. **Extract Component Names:**
   - Read test_plan_*.md file
   - Parse "Components Under Test" table
   - Extract component names and file paths

2. **Search Actual Codebase:**
   ```
   FOR each component in test plan:
     IF file exists at specified path:
       Read file and extract actual class/function/service names

       IF test plan name differs from actual name:
         Auto-correct to actual name
         Log: "Corrected: [TestPlanName] -> [ActualName]"
       ELSE:
         Log: "Verified: [ComponentName]"
   ```

3. **Validate Import Paths:**
   ```
   FOR each mock dependency in test plan:
     Read component file
     Extract import statements

     IF mock name does not match any import:
       Search for similar import name
       Auto-correct to actual import
       Log: "Corrected mock: [TestPlanMock] -> [ActualImport]"
   ```

4. **Use Corrected Names:**
   - Generate test code using actual component names
   - Generate imports using actual import paths
   - Generate mocks using actual dependency names

**Code Implementation**
- Use `.propel/context/docs/figma_spec.md` for screen and state specifications (UI tasks only)
- Use `.propel/context/docs/designsystem.md` for design tokens (colors, typography, spacing)
- Navigate to Figma URLs OR view design images from design reference documents during implementation
- Follow component mappings defined in `designsystem.md` sections
- Execute implementation following TodoWrite plan systematically
- Implement all required code following existing project patterns
- Mark each completed todo task as [X] in the task file progressively

**Update task file checkboxes**: After completing each todo in TodoWrite, immediately update the corresponding checkbox in the source task.md file using Edit tool (`[ ]` -> `[X]`)
- Maintain precise targeting using line numbers and function references
- Preserve existing functionality while adding new features

**MCP Validation Loop (pre-commit)** (use Sequential-thinking MCP)
- **Plan**: Run `mcp__sequential_thinking__plan` to materialize a verification checklist from the task's acceptance criteria and NFRs.
- **Critique**: Run `mcp__sequential_thinking__critique` mapping real repo evidence (files/endpoints/tests) to each checklist item; capture Pass/Gap/Fail with pointers.
- **Reflect**: Run `mcp__sequential_thinking__reflect` to summarize risks and generate the minimal fix list and missing tests to address before proceeding.
- **Architecture Validation**: Verify implementation aligns with models.md architectural views
- **Sequence Alignment**: Check implementation follows models.md sequence diagram flows

**Continuous Validation**
- Run validation commands after each significant implementation step
- Fix any failures immediately before proceeding
- Re-run validations until all pass successfully

**Design Reference Validation** (UI tasks only):
- Use `.propel/context/docs/figma_spec.md` for screen state validation criteria
- Use `.propel/context/docs/designsystem.md` for design token validation
- Use Playwright MCP to capture screenshots of implemented UI against specifications
- Compare implementation against visual assets referenced in design documents (Figma OR images)
- Compare implementation against Hi-Fi wireframe HTML files referenced in task's Design References table
- Validate design tokens match specifications defined in `designsystem.md`
- Check responsive behavior against breakpoints specified in `figma_spec.md`
- Verify component implementations match mappings in `designsystem.md`
- Use Context7 MCP for the review of implemented code against the design principles and coding guidelines
- Update todo progress in real-time

**Quality Validation**
- Execute complete validation suite as defined in task file
- Verify all checklist items are completed successfully
- Ensure unit tests are created/updated and passing
- Validate logical correctness against requirements

**Integration Testing**
- Test integration with existing functionality to prevent regressions
- Validate error handling and edge case scenarios
- Confirm adherence to coding standards and project conventions
- Verify proper documentation and code comments

**Technology Stack Considerations**
- **Frontend Tasks**: Handle UI/UX, client-side logic, and user interactions independently
- **Backend Tasks**: Manage server-side logic, APIs, and business rules separately
- **Database Tasks**: Handle data modeling, migrations, and queries in focused tasks
- **Infrastructure Tasks**: Manage deployment, configuration, and system setup independently
- **AI Tasks** (if AI Impact = Yes): Handle AI/ML components with specialized implementation:
  - **Prompt Engineering**: Configure and version prompt templates in `prompts/` directory
  - **RAG Pipeline**: Implement chunking, embedding, indexing, and retrieval logic
  - **Guardrails**: Implement input sanitization, output validation, and schema enforcement
  - **LLM Integration**: Configure model provider, API keys, rate limiting, and error handling
  - **Fallback Logic**: Implement confidence thresholds and deterministic fallback paths
  - **Audit Logging**: Log prompts/responses for observability (redact PII before logging)
  - **Token Management**: Enforce token budgets and implement request batching if needed

**Code Quality Requirements**
- **Pattern Consistency**: Follow existing codebase patterns and architectural decisions
- **Error Handling**: Implement comprehensive error handling following project standards
- **Testing Coverage**: Ensure unit tests cover all new functionality and edge cases
- **Documentation**: Maintain clear code comments and update relevant documentation
- **Performance**: Consider performance implications and follow project optimization patterns

### Error Recovery and Rollback Procedures

#### Error Handling Strategy
- **Immediate Validation**: Validate after each significant code change
- **Rollback Planning**: Use established restoration points for quick recovery
- **Pattern-Based Fixes**: Apply error patterns from task file for systematic resolution
- **Iterative Resolution**: Fix-validate-retest cycle until all validations pass

#### Quality Assurance Gates
- **Code Review**: Self-review against project standards before completion
- **Test Validation**: All tests must pass before marking task complete
- **Integration Check**: Verify no regressions in existing functionality
- **Documentation Review**: Ensure all changes are properly documented

### Completion and Validation Framework

#### Completion Criteria
- [ ] **MCP Critique Resolved**: All critical Gaps from `mcp__sequential_thinking__critique`/`reflect` are fixed or explicitly waived with rationale
- [ ] **Context7 Alignment**: At least one validation pass confirms implemented patterns align with versioned guidance fetched via Context7
- [ ] **Architecture Alignment**: Implementation consistent with models.md diagrams
- [ ] **Epic Traceability**: Task traces through story -> epic -> requirements
- [ ] **Screen Spec Compliance**: Implementation matches screen specifications in figma_spec.md (UI tasks only)
- [ ] **Visual Fidelity**: UI matches visual assets referenced in figma_spec.md and designsystem.md (UI tasks only)
- [ ] **Design Token Accuracy**: All colors, typography, spacing applied per designsystem.md specifications (UI tasks only)
- [ ] **Component Mapping**: Implementation follows component mappings defined in designsystem.md (UI tasks only)
- [ ] **State Coverage**: All 5 states (Default/Loading/Empty/Error/Validation) implemented per figma_spec.md (UI tasks only)
- [ ] **Responsive Validation**: All breakpoints behave per figma_spec.md specifications (UI tasks only)
- [ ] **Pixel-Perfect Screenshots**: Playwright validation confirms implementation matches design specifications (UI tasks only)
- [ ] **AIR Requirements Met**: All mapped AIR-XXX requirements implemented and validated (AI tasks only)
- [ ] **Prompt Templates Versioned**: Prompt templates stored in `prompts/` with version control (AI tasks only)
- [ ] **Guardrails Implemented**: Input sanitization and output validation in place (AI tasks only)
- [ ] **Fallback Logic Tested**: Low-confidence and error scenarios trigger deterministic fallback (AI tasks only)
- [ ] **Token Budget Enforced**: Token limits configured per AIR-O01 requirements (AI tasks only)
- [ ] **Audit Logging Active**: Prompts/responses logged (PII redacted) for observability (AI tasks only)
- [ ] **Task Implementation**: All todo items in task file marked as completed [X]
- [ ] **Code Quality**: Implementation follows existing project patterns and standards
- [ ] **Testing**: Unit tests created/updated and all tests passing
- [ ] **Validation**: All validation commands execute successfully
- [ ] **Integration**: No regressions in existing functionality
- [ ] **Documentation**: Code properly documented and comments updated
- [ ] **Error Handling**: Comprehensive error scenarios handled appropriately
- [ ] **Requirements Compliance**: All original requirements fully implemented
- [ ] **Evaluation Metrics Generated**: Complete metrics table populated with measured values and evidence

## Final Deliverables
**Implementation Report**
- Complete list of updated/created files with descriptions
- Summary of changes made relative to project structure
- Validation results and test coverage confirmation
- Any logical errors identified and resolved

**Evaluation Metrics Report** (Mandatory)
- Complete evaluation metrics table with measured values
- Production readiness assessment

## Guardrails
- `rules/ai-assistant-usage-policy.md`: Explicit commands; minimal output
- `rules/code-anti-patterns.md`: Avoid god objects, circular deps, magic constants **[CRITICAL]**
- `rules/dry-principle-guidelines.md`: Single source of truth; delta updates
- `rules/iterative-development-guide.md`: Strict phased workflow
- `rules/language-agnostic-standards.md`: KISS, YAGNI, size limits, clear naming **[CRITICAL]**
- `rules/markdown-styleguide.md`: Front matter, heading hierarchy, code fences
- `rules/performance-best-practices.md`: Optimize after measurement
- `rules/security-standards-owasp.md`: OWASP Top 10 alignment **[CRITICAL]**
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

**>>> ALWAYS: Execute Quality Evaluation. Print evaluation report to console. <<<**

## Quality Evaluation

### 4-Tier Implementation Assessment

| Tier | Dimension | Gate | Conditional |
|------|-----------|------|-------------|
| T1 | Build Success | MUST PASS | No (always required) |
| T2 | Requirements Fulfilled + Task Checklist | MUST=100% / ≥80% | No (always required) |
| T3 | Security Scan + Code Quality | ≥80% | Yes (skip if no security-sensitive changes) |
| T4 | Architecture + Standards Adherence | ≥80% | Yes (skip for trivial tasks ≤3 files) |

**Task Type**: [FE/BE/DB/Integration/Infrastructure/AI]

---

### Tier 1: Build Verification (REQUIRED)

**Goal:** Verify implementation compiles and passes basic validation

| Check | Command | Expected | Actual | Status |
|-------|---------|----------|--------|--------|
| Build | Project build command | exit 0 | [result] | PASS/FAIL |
| Lint | Project lint command | 0 errors | [result] | PASS/FAIL |

**Gate:** MUST PASS - Execution halts if build fails

---

### Tier 2: Requirements Fulfillment (REQUIRED)

**Goal:** Verify all task requirements and checklist items are completed

#### Requirements Implementation
| Check | Metric | Threshold | Actual | Score |
|-------|--------|-----------|--------|-------|
| Requirements Implemented | implemented / total | 100% | [N]/[M] | [X]% |

**Execution:**
```
1. Read task file → Extract acceptance criteria and requirements
2. Read implementation → Verify each requirement is addressed
3. Coverage = (implemented / total requirements) × 100%
```

#### Task Checklist Completion
| Check | Metric | Threshold | Actual | Score |
|-------|--------|-----------|--------|-------|
| Checklist Items | [x] items / total | ≥80% | [N]/[M] | [X]% |

**Execution:**
```
Read task file
Extract "## Implementation Checklist" section
IF "### AI Test Implementation Checklist" subsection exists:
  Include that subsection as well

Within extracted section(s):
  Grep("- \[x\]", section_content) -> completed_count (case insensitive)
  Grep("- \[ \]", section_content) -> pending_count
Total = completed_count + pending_count
Task Checklist Completion = (completed_count / total) × 100%
```

**Gate:** Requirements = 100%, Checklist ≥ 80%

---

### Tier 3: Security & Code Quality (CONDITIONAL)

**Skip Condition:** Task has no security-sensitive changes (no auth, no data handling, no external APIs, no user input processing)

**Goal:** Verify implementation meets security and code quality standards

| Check | Command/Method | Threshold | Actual | Score |
|-------|----------------|-----------|--------|-------|
| Security Scan | `npm audit` or equivalent | 0 critical/high | [result] | PASS/FAIL |
| Secrets Detection | grep for API keys, passwords | 0 found | [result] | PASS/FAIL |
| Code Complexity | Cyclomatic complexity | ≤10 per function | [count] | [X]% |
| Code Duplication | Duplicate code blocks | 0 | [count] | [X]% |
| Linter Warnings | Project linter | ≤5 warnings | [count] | [X]% |

**Scoring:**
```
Security Score = (security_scan == PASS && secrets == 0) ? 100% : 0%
Quality Score = Average of (Complexity, Duplication, Linter) scores
Tier 3 Score = (Security Score × 0.5) + (Quality Score × 0.5)
```

**Gate:** ≥ 80% aggregate (or SKIPPED if condition met)

---

### Tier 4: Architecture & Standards Adherence (CONDITIONAL)

**Skip Condition:** Trivial task (≤3 files changed, no new patterns introduced, no architectural decisions)

**Goal:** Verify implementation aligns with architectural decisions and coding standards

| Check | Validation | Threshold | Actual | Score |
|-------|------------|-----------|--------|-------|
| Architectural Alignment | models.md sequence/component consistency | Aligned | [yes/no] | PASS/FAIL |
| Design Token Compliance | designsystem.md adherence (UI tasks only) | 100% | [X]% | [X]% |
| Language Standards | Project coding conventions followed | Compliant | [yes/no] | PASS/FAIL |
| Pattern Consistency | Matches existing codebase patterns | Consistent | [yes/no] | PASS/FAIL |

**Execution:**
```
1. IF UI task: Validate design tokens from designsystem.md are applied correctly
2. Read models.md → Extract relevant sequence diagrams for task's use cases
3. Compare implementation flow against diagram flow
4. Check naming conventions, file organization, code patterns against existing codebase
```

**Gate:** ≥ 80% aggregate (or SKIPPED if condition met)

---

### Output Format

```
===========================================================
         IMPLEMENTATION EVALUATION: [task-id]
===========================================================

Task File:     [task file path]
Task Type:     [FE/BE/DB/Integration/Infrastructure/AI]
Files Changed: [count]

-----------------------------------------------------------
TIER 1: Build Verification
-----------------------------------------------------------
| Check        | Expected | Actual   | Status    |
|--------------|----------|----------|-----------|
| Build        | exit 0   | [result] | PASS/FAIL |
| Lint         | 0 errors | [result] | PASS/FAIL |

Score: [PASS/FAIL]  |  Gate: MUST PASS  |  Result: [PASS/FAIL]

-----------------------------------------------------------
TIER 2: Requirements Fulfillment
-----------------------------------------------------------
Requirements Implemented: [N]/[M] = [X]%
Checklist Completed:      [N]/[M] = [X]%

Missing Requirements: [list or "None"]
Pending Checklist:    [list or "None"]

Score: [X]%  |  Gate: Req=100%, Checklist≥80%  |  Result: [PASS/FAIL]

-----------------------------------------------------------
TIER 3: Security & Code Quality [CONDITIONAL]
-----------------------------------------------------------
Status: [EVALUATED / SKIPPED - reason]

| Check            | Threshold    | Actual  | Score     |
|------------------|--------------|---------|-----------|
| Security Scan    | 0 critical   | [N]     | PASS/FAIL |
| Secrets          | 0 found      | [N]     | PASS/FAIL |
| Complexity       | ≤10/function | [N]     | [X]%      |
| Duplication      | 0 blocks     | [N]     | [X]%      |
| Linter Warnings  | ≤5           | [N]     | [X]%      |

Score: [X]%  |  Gate: ≥80%  |  Result: [PASS/FAIL/SKIPPED]

-----------------------------------------------------------
TIER 4: Architecture & Standards [CONDITIONAL]
-----------------------------------------------------------
Status: [EVALUATED / SKIPPED - reason]

| Check                  | Expected   | Actual   | Status    |
|------------------------|------------|----------|-----------|
| Architectural Alignment| Aligned    | [yes/no] | PASS/FAIL |
| Design Tokens (UI)     | 100%       | [X]%     | PASS/FAIL |
| Language Standards     | Compliant  | [yes/no] | PASS/FAIL |
| Pattern Consistency    | Consistent | [yes/no] | PASS/FAIL |

Score: [X]%  |  Gate: ≥80%  |  Result: [PASS/FAIL/SKIPPED]

-----------------------------------------------------------
OVERALL ASSESSMENT
-----------------------------------------------------------
| Tier | Dimension                  | Score      | Gate    | Result  |
|------|----------------------------|------------|---------|---------|
| T1   | Build                      | [PASS/FAIL]| MUST    | [P/F]   |
| T2   | Requirements + Checklist   | [X]%       | 100%/80%| [P/F]   |
| T3   | Security + Quality         | [X]%       | ≥80%    | [P/F/S] |
| T4   | Architecture + Standards   | [X]%       | ≥80%    | [P/F/S] |

Verdict: [PASS / CONDITIONAL PASS / FAIL]

Top 3 Weaknesses:
1. [Tier] - [Dimension] ([X]%): [Specific issue]
2. [Tier] - [Dimension] ([X]%): [Specific issue]
3. [Tier] - [Dimension] ([X]%): [Specific issue]

Critical Failures: [List any MUST PASS gates that failed, or "None"]
===========================================================
```

---