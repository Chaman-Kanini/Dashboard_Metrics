---
description: Generates comprehensive implementation tasks from feature requirements, user stories, or functional specifications with thorough research, context integration, and quality validation
auto_execution_mode: 1
---

# Unified Task Generator
As a Senior Software Engineer expert in Full Stack development, generate comprehensive implementation tasks based on the provided input. This unified command handles all task generation scenarios with consistent quality and thorough research approach.

## Input Parameter: $ARGUMENTS (Mandatory)
**Accepts:** User story file path | User story URL | User story text | Feature requirements | Functional specification

### Argument Types:
1. **User Story File**: Path to us_XXX.md file (e.g., .propel/context/tasks/us_001/us_001.md)
2. **User Story URL**: URL pointing to user story specification
3. **User Story Text**: Direct user story content in "As a... I want... so that..." format
4. **Feature Requirements**: Path to requirements specification
5. **Functional Specification**: General functional description

**Optional Parameters:**
- `--skip-history`: Skip git history analysis and findings registry lookup for faster execution (default: false)

### User Story Input Processing
**When $ARGUMENTS contains user story (file, URL, or text):**
1. **Extract US ID**: Parse us_XXX identifier from file path, content, or generate if text input
2. **Create Task Folder**: Ensure `/.propel/context/tasks/us_<ID>/` directory exists
3. **Task File Naming**: Generate tasks as `task_<seqnum>_<descriptive_name>.md` within US folder
4. **Parent Story Reference**: Maintain traceability to parent user story in all tasks
5. **Acceptance Mapping**: Map implementation tasks to user story acceptance criteria

### US ID Extraction Algorithm
**File Input**: Extract us_XXX from file path using pattern matching
- Pattern: `/us_(\d{3})/` or `us_(\d{3})\.md`
- Example: `.propel/context/tasks/us_001/us_001.md` -> Extract `us_001`

**URL Input**:
- First attempt: Parse URL path for us_XXX pattern
- If not found: Fetch URL content and search for US ID in content
- Pattern: `US[_-]?(\d{3,4})`

**Text Input**:
- Search for existing US ID in text: `US[_-]?(\d{3,4})`

**Fallback Behavior**:
- If no US ID can be extracted or found -> Create tasks in `/.propel/context/tasks/` folder directly
- Use standard task numbering: `task_XXX_<descriptive_name>.md`
- Log clearly where tasks are being created (US folder vs. root Tasks folder)

## Output
- Artifact generation: `/.propel/context/tasks/us_<ID>/*.md`
- Print the following: 
    - List of rules used by the workflow in bulleted format
    - Evaluation Scores in tabular format with average score. 
    - Evaluation summary (less than 100 words).
    **Do not save as file.**

**Note:**
- **File Handling**: IF file exists → UPDATE changed sections only (delta mode). IF file does not exist → CREATE complete file.
- Generate the output using the .propel/templates/task-template.md and `.propel/templates/design-reference-template.md` (for UI tasks only) templates.

### Output Specifications

#### File Organization Strategy:
**For User Story Tasks (US ID found in input):**
- **Directory**: `/.propel/context/tasks/us_<ID>/`
- **File Pattern**: `task_<seqnum>_<descriptive_name>.md`
- **Example**: `/.propel/context/tasks/us_001/task_001_implement_login_ui.md`
- **Trigger**: Valid us_XXX pattern extracted from file path, URL, or text content

**For General Tasks (no US ID found - fallback):**
- **Directory**: `/.propel/context/tasks/us_<short_descriptive_name>/`
- **File Pattern**: `task_<seqnum>_<descriptive_name>.md`
- **Example**: `/.propel/context/tasks/task_001_setup_database.md`
- **Trigger**: No valid US ID extractable from input

**Sequence Number Logic**:
- Auto-increment based on existing task files in the target directory
- Use zero-padded 3-digit format (001, 002, 003...)
- Separate sequence per us_<ID> folder
- Descriptive name should reflect primary functionality being implemented

### Directory Management

#### US ID Extraction Priority
1. **Parse Input**: Attempt to extract us_XXX from input using patterns defined above
2. **Validate Format**: Check if extracted ID matches us_XXX pattern (3-digit numeric)
3. **Fallback to Root**: If no valid US ID found -> use `/.propel/context/tasks/us_<short_descriptive_name>/` directly

#### Directory Creation Logic
**With Valid US ID Found**:
- **Directory**: `/.propel/context/tasks/us_<ID>/`
- **File Pattern**: `task_<seqnum>_<descriptive_name>.md`
- **Sequence**: Continue from highest existing task number in US folder
- **Example**: `/.propel/context/tasks/us_001/task_001_implement_login_form.md`

**Without Valid US ID (Fallback)**:
- **Directory**: `/.propel/context/tasks/us_<short_descriptive_name>/`
- **File Pattern**: `task_<seqnum>_<descriptive_name>.md`
- **Sequence**: Continue from highest existing task number in root Tasks folder
- **Example**: `/.propel/context/tasks/us_setup_db/task_001_setup_database.md`

#### Task Organization Examples
```
.propel/context/tasks/
+-- us_001/                          # US ID found (us_001)
|   +-- us_001.md
|   +-- task_001_implement_login_form.md
|   +-- task_002_add_validation_logic.md
|   +-- task_003_create_unit_tests.md
+-- us_002/                          # US ID found (us_002)
|   +-- us_002.md
|   +-- task_001_setup_password_reset.md
+-- us_general_setup/                # US ID not found -> fallback directory
|   +-- us_general_setup.md
|   +-- task_001_general_setup.md
+-- us_oauth_integration/            # US ID not found -> fallback directory
|   +-- task_001_oauth_integration.md
+-- us_db_integration/               # US ID not found -> fallback directory
    +-- task_001_database_integration.md

```

#### Logging and Transparency
- **Always log** the decision: "Creating tasks in us_XXX folder" or "No US ID found, creating tasks in root /.propel/context/tasks/us_<short_descriptive_name>/"
- **Document reasoning** for task placement in task files
- **Maintain clear traceability** between input type and output location

## Core Principles
- **Story-Task Mapping**: One task maps to one requirement/story only
- **Size Constraints**: Split tasks exceeding 8 hours into smaller units
- **Technology Separation**: Separate tasks by stack (frontend, backend, database)

## Quality Standard: One-Shot Example

**Example of well-decomposed tasks from US_042 (Password Reset):**

**User Story:** US_042 - User Password Reset via Email
- **Acceptance Criteria:** 4 GWT criteria covering email delivery, secure form, old password rejection, link expiration
- **Technology Stack:** React 18.2 (FE), Node.js 20.x + Express (BE), PostgreSQL 14 (DB)

**Generated Task Decomposition:**

---

**File 1:** `.propel/context/tasks/us_042/task_001_fe_password_reset_ui.md`

**Task:** Implement Password Reset UI (Frontend)
**Effort:** 5 hours
**Layer:** Frontend (React)

**Implementation Checklist (7 items ≤ 8 limit):**
- [ ] Create ForgotPasswordForm component with email input field
- [ ] Add form validation (email format check)
- [ ] Implement "Send Reset Link" button with loading state
- [ ] Create PasswordResetForm component (for reset page from email link)
- [ ] Add password strength indicator (8+ chars, uppercase, number, special char)
- [ ] Display success/error messages (link sent, expired, reset successful)
- [ ] Add unit tests for both components (React Testing Library)

**Traceability:** US_042 AC-1, AC-2, AC-4 | FR-005 | UXR-023

---

**File 2:** `.propel/context/tasks/us_042/task_002_be_password_reset_api.md`

**Task:** Implement Password Reset API (Backend)
**Effort:** 6 hours
**Layer:** Backend (Node.js + Express)

**Implementation Checklist (8 items = 8 limit):**
- [ ] Create POST `/api/auth/forgot-password` endpoint (email param)
- [ ] Generate secure reset token (crypto.randomBytes, 32 bytes)
- [ ] Store token in DB with 24h expiration timestamp
- [ ] Integrate email service to send reset link
- [ ] Create POST `/api/auth/reset-password` endpoint (token + new password)
- [ ] Validate token (not expired, exists in DB) and password complexity
- [ ] Hash new password (bcrypt) and update user record
- [ ] Implement rate limiting (max 3 requests per 5 minutes per email)

**Traceability:** US_042 AC-1, AC-2, AC-3, AC-4 | FR-005 | NFR-012

---

**File 3:** `.propel/context/tasks/us_042/task_003_db_password_reset_schema.md`

**Task:** Add Password Reset Schema & Migration (Database)
**Effort:** 2 hours
**Layer:** Database (PostgreSQL)

**Implementation Checklist (4 items ≤ 8 limit):**
- [ ] Create `password_reset_tokens` table (id, user_id, token_hash, expires_at, created_at)
- [ ] Add index on token_hash for fast lookup
- [ ] Add foreign key constraint to users table (user_id)
- [ ] Write migration script with rollback support

**Traceability:** US_042 | FR-005 | DR-018 (data retention)

---

**Why this example demonstrates quality:**

✅ **Technology Layer Separation:** 3 separate files (FE / BE / DB)
✅ **Per-File Sizing:** Each file has ≤8 checklist items and ≤8 hours effort
✅ **Independent Testability:** Each task can be implemented and tested separately
✅ **Traceability:** All tasks reference parent US_042 and specific acceptance criteria
✅ **No Cross-Layer Violations:** FE task doesn't mention DB schemas, BE task doesn't mention React components

❌ **Anti-pattern to avoid:** Creating one giant `task_001_implement_password_reset.md` with 19 checklist items mixing FE/BE/DB work (violates per-file limit and layer purity)

## Execution Flow

### Delta Processing Protocol
**Before generating any output:**
1. Check if target output file (`task_<seqnum>_<name>.md`) already exists
2. If EXISTS: Read current content, identify only sections requiring update, EDIT those sections only
3. If NOT EXISTS: Generate complete new file
4. Log: "Mode: [Delta update to X sections | New file creation]"

### 1. Input Processing
- Detect input type and extract US ID using defined patterns
- Create appropriate folder structure based on US ID presence
- Read spec.md, design.md, epics.md, and models.md for context

#### Tech Stack Extraction
**Before any task generation:**
1. Read `.propel/context/docs/design.md` → Extract technology stack
2. Parse into structured format: `{frontend: {name, version}, backend: {name, version}, database: {name, version}}`
3. **If Context7 available**: Call `mcp__context7__resolve-library-id` for EACH technology
4. **If Context7 unavailable**: Use web search with EXACT version string: "[technology] [version] official documentation [year]"
5. **FAIL FAST**: If design.md missing or tech stack section absent → STOP, request clarification

#### Selective Context Loading
**Load ONLY relevant context for the user story's scope:**

**From spec.md:**
- Extract ONLY the FR-XXX and UC-XXX IDs listed in the user story's Requirement Tags
- **CRITICAL**: SKIP any requirements tagged with [UNCLEAR] - do NOT create tasks for them
- Skip unrelated functional requirements

**From design.md:**
- Extract ONLY Technology Stack section
- Extract ONLY NFR/TR/DR IDs that map to the parent epic
- **CRITICAL**: SKIP any NFR/TR/DR tagged with [UNCLEAR]

**From models.md:**
- Read ONLY the sequence diagrams for UC-XXX IDs mapped to the target user story
- Skip all other diagrams, ERD, deployment, and context views

**From figma_spec.md (if UI-impacting):**
- Extract ONLY UXR-XXX IDs listed in the user story
- **CRITICAL**: SKIP any UXR-XXX tagged with [UNCLEAR]

**[UNCLEAR] Requirement Handling:**
- If a user story references [UNCLEAR] requirements, generate a placeholder task with status "BLOCKED - Requires Requirement Clarification"
- Document which [UNCLEAR] requirements block the task
- Do NOT generate implementation tasks until requirements are clarified

### 2. Task Decomposition Rule
- **Per-File Limits**: Each task file must have <=8 todos AND <=8 hours estimated effort
- **One Layer Per File**: Each technology layer (FE/BE/DB/Infra/AI) = separate task file
- **Decomposition Strategy**:
  1. Split by technology layer FIRST — each layer becomes its own `task_XXX_<layer>_*.md` file
  2. Within a layer, split further if todos >8 or effort >8 hours
  3. Each file must be independently testable
  4. Maintain traceability: Task File -> User Story -> Epic
- **Validation Gate**: Before finalizing, verify EACH file meets limits. If any file exceeds limits, split into additional files.

### 2a. AI Task Layer [CONDITIONAL: If user story maps to AIR-XXX]

**Detection Gate:**
```
Grep("AIR-\d{3}", user_story_file) → air_requirements
IF air_requirements.count > 0 → Generate AI layer tasks
```

**AI Layer Task Types:**
| Task Type | When to Generate | Example Task Name |
|-----------|------------------|-------------------|
| Prompt Configuration | AIR-001 (generation) | `task_XXX_ai_prompt_setup.md` |
| RAG Pipeline | AIR-R01, AIR-R02, AIR-R03 | `task_XXX_ai_rag_pipeline.md` |
| Embedding Setup | RAG pattern selected | `task_XXX_ai_embedding_indexing.md` |
| Vector Store | RAG pattern selected | `task_XXX_ai_vectorstore_setup.md` |
| Guardrails | AIR-S01, AIR-S02, AIR-S03 | `task_XXX_ai_guardrails.md` |
| AI Gateway | AIR-O01, AIR-O02 | `task_XXX_ai_gateway_integration.md` |
| LLM Integration | Any AIR-XXX | `task_XXX_ai_llm_integration.md` |

**AI Task Checklist Requirements:**
Each AI layer task MUST include:
- [ ] Model provider configuration (API keys, endpoints)
- [ ] Prompt template with version control
- [ ] Input/output schema validation
- [ ] Error handling for model failures (timeout, rate limit, 5xx)
- [ ] Fallback logic for low-confidence responses
- [ ] Token budget enforcement
- [ ] Audit logging setup (prompts/responses)

**AI Task Separation:**
- **DO NOT** combine AI tasks with FE/BE tasks
- AI tasks focus on: prompt engineering, retrieval logic, model integration
- FE/BE tasks focus on: API endpoints, UI, business logic that consumes AI outputs

### Deep Research Methodology

Optimize for success probability over execution speed. Spawn multiple agents and subagents using batch tools for comprehensive analysis.

#### 1. Codebase Intelligence Gathering (use Sequential-Thinking MCP)
- **Screen Specification Analysis**: Read `.propel/context/docs/figma_spec.md` for screen inventory, states, and flow definitions (UI tasks only)
- **Design Token Analysis**: Read `.propel/context/docs/designsystem.md` for design tokens and component mappings (UI tasks only)
- **Hi-Fi Wireframe Loading**: For UI tasks, read corresponding wireframe from `.propel/context/wireframes/Hi-Fi/wireframe-SCR-XXX-{name}.html`
- **User Story Design Mapping**: Identify which user stories this task relates to and extract their screen references
- **Visual Asset Loading**: Load Figma URLs OR design images referenced in design documents for this task's user stories
- **Pattern Discovery**: Search for similar features/implementations in existing codebase
- **Impact Analysis**: Identify existing features requiring modification to maintain functionality
- **Reference Mapping**: Document files and patterns to reference in task design
- **Convention Documentation**: Catalog existing code styles, naming patterns, and architectural approaches
- **Test Pattern Analysis**: Review testing strategies and validation approaches used in the project
- **Best Practices Refresh**: Search for "[technology] best practices [current year]" to find recent guides

#### Design References Extraction (UI Tasks Only)

For each UI-impacting task, populate the "Design References" table in the task file:

**Step 1: Read Parent User Story**
- Parse user story file (`.propel/context/tasks/us_XXX/us_XXX.md`)
- Extract "Visual Design Context" section values:
  - Screen ID(s): SCR-XXX
  - Figma Spec Reference: figma_spec.md#SCR-XXX
  - Hi-Fi Wireframe paths
  - UXR Mappings: UXR-XXX

**Step 2: Enrich from figma_spec.md (for each SCR-XXX)**
- Grep figma_spec.md for SCR-XXX section
- Extract: Figma frame URL (node-id), route/path, required states, component requirements
- Extract: UXR-XXX requirements mapped to this screen

**Step 3: Locate Wireframe Files (Multiple Formats)**
1. **Search for local wireframes** (priority order):
   - Glob: `.propel/context/wireframes/Hi-Fi/wireframe-SCR-XXX-*.html`
   - Glob: `.propel/context/wireframes/Hi-Fi/wireframe-SCR-XXX-*.png`
   - Glob: `.propel/context/wireframes/Hi-Fi/wireframe-SCR-XXX-*.jpg`
   - Glob: `.propel/context/wireframes/Hi-Fi/wireframe-SCR-XXX-*.jpeg`

2. **Check parent user story for external wireframe**:
   - Read user story's "Wireframe References" table
   - IF Status = "EXTERNAL" AND Type = "URL": Use provided URL
   - IF Status = "AVAILABLE": Use provided path (supports all formats)

3. **Determine wireframe value**:
   - IF local file found: Set Status = "AVAILABLE", Type = [file extension], Path = actual path
   - IF external URL in user story: Set Status = "EXTERNAL", Type = "URL", Path = URL
   - IF neither found BUT UI Impact = Yes: Set structured placeholder (see below)
   - IF UI Impact = No: Set all to "N/A"

**Placeholder for Missing Wireframes (when UI Impact = Yes but no wireframe found):**
```markdown
| **Wireframe Status** | PENDING |
| **Wireframe Type** | N/A |
| **Wireframe Path/URL** | TODO: Upload to `.propel/context/wireframes/Hi-Fi/wireframe-SCR-XXX-{name}.[html|png|jpg]` or provide external URL |
```

**Step 4: Reference Design Tokens**
- From designsystem.md, identify sections relevant to this task's components
- Reference format: `designsystem.md#typography` or `designsystem.md#colors`

**Step 5: Populate Design References Table**
```markdown
## Design References (Frontend Tasks Only)
| Reference Type | Value |
|----------------|-------|
| **UI Impact** | Yes |
| **Figma URL** | [Figma frame URL with node-id from figma_spec.md, or N/A] |
| **Wireframe Status** | [AVAILABLE / PENDING / EXTERNAL / N/A] |
| **Wireframe Type** | [HTML / PNG / JPG / URL / N/A] |
| **Wireframe Path/URL** | [local path, external URL, or "TODO: Provide wireframe..."] |
| **Screen Spec** | [figma_spec.md#SCR-XXX, or N/A] |
| **UXR Requirements** | [UXR-XXX list from figma_spec.md, or N/A] |
| **Design Tokens** | [designsystem.md section reference, or N/A] |
```

> **Wireframe Status Legend:**
> - **AVAILABLE**: Local file exists at specified path
> - **PENDING**: UI-impacting task awaiting wireframe (provide file or URL)
> - **EXTERNAL**: Wireframe provided via external URL
> - **N/A**: Task has no UI impact

**Step 6: Non-UI Tasks**
- If task has no UI impact: Set UI Impact = "No" and all other fields = "N/A"

**Step 7: Validate Wireframe Format**
When wireframe path/URL is provided, validate format:

| Input Pattern | Validation | Status |
|---------------|------------|--------|
| `*.html` | File exists at path | AVAILABLE if exists |
| `*.png` | File exists at path | AVAILABLE if exists |
| `*.jpg` / `*.jpeg` | File exists at path | AVAILABLE if exists |
| `https://figma.com/*` | URL format valid | EXTERNAL |
| Other URL (`https?://.*`) | URL format valid | EXTERNAL |
| Empty/missing | N/A | PENDING if UI Impact = Yes |

#### 2. External Knowledge Acquisition
- **Implementation Research**: Search for similar features/patterns in open-source projects
- **Sample Code**: If Context7 available, use `mcp__context7__get-library-docs` with resolved IDs. Otherwise, web search "[technology] [version] official docs [year]". REJECT code referencing unlocked technologies.
- **Version Pinning** [Always]: Tech stack from design.md is the SOLE source of truth. Cross-check every library import against locked versions. Flag version > locked as INCOMPATIBLE.
- **Design Asset Integration**: Reference Figma links OR design images in task context (only when UI impact exists)
- **UI Implementation Guidance**: Include specific design specifications from visual assets (Figma frames OR image files)
- **Component Mapping**: Map design components to code implementation patterns
- **Visual Validation Criteria**: Define pixel-perfect implementation requirements using available design references
- **Style Guidelines**: Research project-specific or framework coding standards
- **Documentation Deep-Dive**: Library documentation with specific section URLs
- **Example Collection**: GitHub repositories, StackOverflow solutions, technical blog implementations
- **Best Practice Synthesis**: Industry patterns, performance considerations, and common pitfalls

#### 3. Contextual Clarification (When Needed)
- **Pattern Alignment**: Which existing implementations should be mirrored and their locations?
- **Integration Requirements**: How should new features integrate with existing systems?
- **Quality Standards**: What testing, documentation, and validation standards apply?

#### 4. Historical Issue Analysis (Optional: skip with --skip-history)

**Git History Check** (~3 commands):
- `git log --grep="fix\|bug" --oneline -5 -- <affected_files>` - Last 5 bug-related commits only
- `git shortlog -sn -5 -- <affected_files>` - Top 5 contributors only
- If >3 bug commits found, flag file as "High-Risk (frequent fixes)"

**Git Fallback** (if git unavailable or commands fail):
- Skip git history check, proceed with registry lookup only"

**Findings Registry Lookup** (selective read):
- Read only the Index section from `.propel/learnings/findings-registry.md`
- If affected files appear in index, grep only those specific entries
- Do NOT read full registry - use index for O(1) lookup

**Output**: Single warning block if issues found, nothing if clean

#### MCP Fallback Protocol
**If Sequential-Thinking MCP unavailable:**
- Use structured analysis: List (1) dependencies, (2) risks, (3) edge cases explicitly
- Document: "Fallback: Manual structured analysis (MCP unavailable)"

**If Context7 MCP unavailable:**
- Use web search: "[technology] [version] official documentation [current year]"
- Document: "Fallback: Web search for docs (Context7 unavailable)"

### Essential Project Intelligence

#### Reference Materials Analysis
- **Codebase Structure**: Explore existing codebase (`app`, `backend`, `server` folders) for code patterns and architectural decisions
- **Documentation Review**: Study existing README files, API documentation, and inline code comments

#### Epic Context Integration
- **epics.md**: Reference EP-XXX for task grouping and priority
- **design.md**: Source of truth for architecture and entities
- **models.md**: Use sequence diagrams for workflow understanding
- **Requirement Traceability**: Trace tasks through User Story -> Epic -> Requirements

*** Codebase comprehension is non-negotiable for quality task generation ***

### Task Design Framework

#### Template Foundation
Base all tasks on `.propel/templates/task-template.md` structure for consistency.
Integrate design context from `.propel/templates/design-reference-template.md` for UI tasks only.

#### Critical Context Integration

**Documentation Context**
- Specific URLs with relevant sections highlighted
- API documentation with version-specific considerations
- Framework guides with implementation examples

**Architecture Context**
- System design patterns and their rationale
- Integration points and data flow diagrams  
- Performance and scalability considerations

**Implementation Context**
- Real code snippets from existing codebase
- Configuration examples and environment setup
- Error handling patterns used in the project

**Design Context (UI Impact Only)**
- **Screen Specifications**: From figma_spec.md (derived from epics.md UI impact)
- **Design Tokens**: From designsystem.md
- **Architectural Views**: From models.md (sequence diagrams for UC-XXX)
- **Epic Context**: From epics.md for task prioritization
- **Visual References**: Figma URLs OR design images from design documents
- **Component Specifications**: Component mappings from designsystem.md
- **Flow Definitions**: Prototype flows and interactions from figma_spec.md
- **Responsive Design**: Breakpoints and behaviors from figma_spec.md

**Visual Assets (From figma_spec.md and designsystem.md)**
- **Screen State Requirements**: All 5 states (Default/Loading/Empty/Error/Validation) from figma_spec.md
- **Component Documentation**: Visual specs from designsystem.md component mappings
- **Design-to-Code Mapping**: Guidelines extracted from design documents
- **Pixel-Perfect Requirements**: Implementation criteria from screen specifications

**Example Task Design Reference**:
```yaml
Design Context:
  screen_spec: .propel/context/docs/figma_spec.md#SCR-001
  design_tokens: .propel/context/docs/designsystem.md
  user_story: US-001 - User Login Interface
  visual_references:
    figma_url: https://figma.com/file/xyz?node-id=2:45
    hi_fi_wireframe: .propel/context/wireframes/Hi-Fi/wireframe-SCR-001-login.html
    # OR if no wireframes exist: hi_fi_wireframe: N/A
  design_tokens:
    primary_color: "#007AFF"
    typography: "SF Pro Display, 32px, 600"
  validation_criteria:
    screenshot_comparison: true
    pixel_tolerance: 5%
    responsive_breakpoints: [375px, 768px, 1440px]
```

**Critical Knowledge**
- Library-specific quirks and version compatibility issues
- Known limitations and workaround strategies
- Security considerations and compliance requirements

**Pattern Consistency**
- Existing approaches for similar functionality
- Naming conventions and code organization patterns
- Testing and validation strategies already established

#### Implementation Blueprint Architecture

**Pseudocode Foundation**
- Start with high-level algorithmic approach
- Break down complex operations into manageable steps
- Reference real files demonstrating similar patterns

**Error Resilience Strategy**
- Identify potential failure points and mitigation approaches
- Document rollback procedures for destructive operations
- Plan validation checkpoints throughout implementation

**Before writing tasks, list all tasks to generate:**
| Task-ID | Summary | Technology Layer |
|---------|---------|------------------|
| ... | ... | ... |
**Now expand each task listed above.**

**Sequential Task Breakdown**
- List implementation tasks in logical dependency order
- Include mandatory unit test creation/updates for each component
- Define clear completion criteria and validation gates

**Versioned Doc Excerpts**
- Include excerpts/links for patterns the task expects (validation, transactions, async I/O, HTTP semantics). Use Context7 if available, otherwise web search with exact version string.


### Context Documentation Requirements

### Essential References Package
- **Technical Documentation**: All URLs, guides, and examples needed for implementation
- **Implementation Examples**: Complex code snippets with explanations and context
- **Integration Points**: How the feature connects with existing systems
- **Quality Gates**: Testing requirements, performance benchmarks, security validations


### Quality Assurance Framework

#### Pre-Delivery Checklist
- [ ] **User Story Validation**: Parent user story identified and referenced correctly
- [ ] **Folder Structure**: Tasks created in correct us_XXX folder when applicable
- [ ] **Task Numbering**: Sequential numbering within US folder maintained
- [ ] **Acceptance Mapping**: Tasks map to user story acceptance criteria
- [ ] **Story Traceability**: Each task references parent us_XXX appropriately
- [ ] **Version-Pinned Docs**: Documentation links with exact version references included for all critical patterns.
- [ ] **Sequential Plan Checklist**: A traceability-friendly checklist derived via `mcp__sequential_thinking__plan` is embedded for execution/analysis.
- [ ] **Screen Spec Loaded**: figma_spec.md read for screen inventory and state requirements (UI tasks only)
- [ ] **Design Tokens Loaded**: designsystem.md read for colors, typography, spacing (UI tasks only)
- [ ] **User Story Screen Mapping**: Task linked to specific screens (SCR-XXX) from figma_spec.md
- [ ] **Visual Assets Referenced**: Figma URLs OR design images loaded from design documents (UI tasks only)
- [ ] **Hi-Fi Wireframe Referenced**: UI tasks include wireframe file path from /.propel/context/wireframes/Hi-Fi/
- [ ] **Figma URL or N/A**: All tasks have explicit Figma_URL value (URL or N/A)
- [ ] **State Requirements Included**: All 5 states defined for each screen in task (UI tasks only)
- [ ] **Component Mapping**: Design components from designsystem.md mapped to code implementations
- [ ] **Validation Criteria Defined**: Pixel-perfect requirements from figma_spec.md included
- [ ] **Context Completeness**: All necessary implementation context included and accessible
- [ ] **Task Scope Validation**: Tasks are under 8 hours and properly split by technology stack when applicable
- [ ] **Technology Stack Separation**: Frontend, backend, database, and infrastructure tasks are independently manageable
- [ ] **Validation Executability**: All quality gates can be executed by AI without human intervention
- [ ] **Pattern Consistency**: References and follows established project patterns
- [ ] **Implementation Clarity**: Clear, unambiguous path from start to completion
- [ ] **Error Handling**: Comprehensive error scenarios documented with responses
- [ ] **Test Strategy**: Testing approach defined with specific validation criteria

## Guardrails
- `rules/ai-assistant-usage-policy.md`: Explicit commands; minimal output
- `rules/code-anti-patterns.md`: Avoid god objects, circular deps, magic constants **[CRITICAL]**
- `rules/dry-principle-guidelines.md`: Single source of truth; delta updates
- `rules/iterative-development-guide.md`: Strict phased workflow **[CRITICAL]**
- `rules/language-agnostic-standards.md`: KISS, YAGNI, size limits, clear naming **[CRITICAL]**
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

**>>> ALWAYS: Execute Quality Evaluation. Follow the 4-tier evaluation framework instructions to evaluate the outcomes. <<<**

## Quality Evaluation

- **Invoke**: `.windsurf/workflows/evaluate-output.md`
  - **$OUTPUT_FILE**: `.propel/context/tasks/us_XXX/task_*.md`
  - **$SCOPE_FILES**: `.propel/context/tasks/us_XXX/us_XXX.md, .propel/context/docs/design.md`
  - **--workflow-type**: `task`

---