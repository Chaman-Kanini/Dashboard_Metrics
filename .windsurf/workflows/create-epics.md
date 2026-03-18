---
description: Generates epic decomposition from spec.md/codeanalysis.md, design.md, and models.md. Creates epics.md with EP-XXX epics, requirement mappings, priorities, and business value. Includes EP-TECH for green-field projects.
auto_execution_mode: 1
---

# Epic Generator

As an expert Product Manager and Business Analyst, generate comprehensive epic decomposition that maps all requirements to actionable development epics. This workflow creates epics.md by analyzing functional, non-functional, technical, data, and UX requirements from multiple source documents.

## Input Parameter: $ARGUMENTS (Optional)
**Accepts:** File path to requirements document | Free text epic scope
**Supported File Types:** .md | .txt | free text

### Input Processing Instructions
**CRITICAL**: Before proceeding with epic generation, you MUST determine input type and process accordingly:

#### Input Type Detection
1. **File Path Detection**: Check if `$ARGUMENTS` contains a file path (contains file extensions .md, .txt)
2. **Free Text Detection**: If `$ARGUMENTS` is text without file extension, treat as epic scope description
3. **Default Fallback**: If `$ARGUMENTS` is empty, use standard input files

#### File Input Processing
If `$ARGUMENTS` is a file path:
1. **File Existence Check**: Verify the file exists using appropriate tools
2. **Read File Contents**: Extract content from the provided file
3. **Content Validation**: Ensure file contains requirements for epic mapping

#### Free Text Processing
If `$ARGUMENTS` is free text:
1. **Text Validation**: Ensure text describes epic scope or feature set
2. **Context Integration**: Combine with default input files if available
3. **Epic Generation**: Create epics based on text scope

#### Default Input Processing
If `$ARGUMENTS` is not provided:
1. **Read spec.md**: Extract FR-XXX requirements and use cases (UXR-XXX in figma_spec.md if UI impact detected)
2. **Read codeanalysis.md**: Alternative to spec.md for brown-field projects
3. **Read design.md**: Extract NFR-XXX, TR-XXX, DR-XXX requirements
4. **Read models.md**: Reference for architectural context (optional) especially sequence diagrams for each of the use case
5. **Content Validation**: Ensure sufficient requirements exist for epic generation

#### Fallback Handling
- If spec.md/codeanalysis.md cannot be read: Request user to provide requirements source
- If design.md doesn't exist: Proceed with FR only, note missing technical requirements
- If no requirements found: Request user to run create-spec and design-architecture workflows first
- Note: UXR-XXX requirements are in figma_spec.md (if exists). Read figma_spec.md for UXR mapping.

## Output
- Artifact generation: `.propel/context/docs/epics.md`
- Print the following:
  - List of rules used by the workflow in bulleted format
  - Epic summary table (EP-XXX with mapped requirements count)
  - Evaluation Scores in tabular format with average score.
  - Evaluation summary (less than 100 words).
  **Do not save as file.** (console output only)

**Note:**
- **File Handling**: IF file exists → UPDATE changed sections only (delta mode). IF file does not exist → CREATE complete file.
- Always create the output file in manageable smaller chunks to manage memory and processing constraints.
- Always generate a single unified document.
- Generate the output using the `.propel/templates/epics-template.md` template.

## Essential Project Intelligence

### Reference Materials Integration
- **spec.md/codeanalysis.md**: Source for FR, UC requirements
- **figma_spec.md**: Source for UXR-XXX requirements (if exists - created by discovery-agent)
- **design.md**: Source for NFR, TR, DR requirements
- **models.md**: Architectural context for epic scoping
- **Existing Codebase**: Project type detection and existing feature analysis

*** Comprehensive requirement mapping with zero orphaned requirements is non-negotiable ***

### References Package
```yaml
- file: .propel/context/docs/spec.md
  why: FR and Use Case requirements

- file: .propel/context/docs/codeanalysis.md
  why: Alternative requirements source for brown-field projects

- file: .propel/context/docs/design.md
  why: NFR, TR, DR requirements for technical epics

- file: .propel/context/docs/models.md
  why: Architectural context for epic scoping

- file: .propel/context/docs/figma_spec.md
  why: UXR-XXX requirements and SCR-XXX screens (read if exists for requirement mapping)
```

## Core Principles
- **Zero Orphaned Requirements**: Every requirement maps to exactly one epic
- **Business Value Ordering**: Prioritize epics by business impact, then dependency
- **Manageable Scope**: Limit epics to ~12 requirements; split if exceeded

## Execution Flow

### 1. Requirement Analysis
- Detect project type (green-field vs brown-field)
- Read all source documents to extract requirements
- Group requirements into logical epics by business outcome
- Generate epic table with requirement mappings
- Create detailed epic descriptions with priorities
- For green-field projects, always include EP-TECH as first epic

### 2. Project Type Detection

#### Green-field Detection
Check for green-field (new) project indicators:
- No existing codebase in `app`, `client`, `backend`, `server` folders
- No `.propel/context/docs/codeanalysis.md` file
- Requirements indicate new system creation
- No migration or backward compatibility requirements

**If Green-field Detected:**
- Create EP-TECH epic as first epic (highest priority)
- EP-TECH includes: Project scaffolding, CI/CD setup, development environment, base architecture

#### Brown-field Detection
Check for brown-field (existing) project indicators:
- Existing codebase present
- `.propel/context/docs/codeanalysis.md` exists
- Requirements reference existing features
- Migration or integration requirements present

**If Brown-field Detected:**
- Do NOT create EP-TECH epic
- Focus epics on feature enhancement and integration
- Consider backward compatibility in epic priorities

#### EP-DATA Detection 
Check for data layer epic triggers:
- `design.md` contains model entity definitions
- `design.md` contains DR-XXX requirements (≥3 data requirements)
- Sequence diagrams (`models.md`) show database interactions

**If EP-DATA Triggered:**
- Create EP-DATA epic (after EP-TECH if green-field, or as high-priority if brown-field)
- EP-DATA includes: Entity scaffolding, relationship mapping, constraints, seed/mock data
- Priority: Critical (blocks feature epics requiring data operations)

**If EP-DATA NOT Triggered:**
- DR-XXX requirements distributed across feature epics as normal
- No dedicated data layer epic needed

### 3. Research Process

#### Requirements Gathering (use Sequential-Thinking MCP)

**Fallback Mechanism:** If the sequential-thinking MCP tool fails or is unavailable, automatically fall back to standard iterative analysis approach using Web fetch:
- Perform systematic step-by-step requirements analysis
- Use structured thinking with explicit validation checkpoints
- Ensure no degradation in analysis quality or completeness

**Selective Context Loading:**

**From models.md:**
- Read ONLY the System Context Diagram and Component Architecture for epic scoping context
- Skip sequence diagrams, deployment, and ERD (these are for task-level detail)

**From spec.md/codeanalysis.md:**
- Extract all FR-XXX (Functional Requirements)
- Extract all UC-XXX (Use Cases)
- **CRITICAL**: SKIP any requirements tagged with [UNCLEAR] - do NOT map them to epics
- Document [UNCLEAR] requirements in a separate "Backlog Refinement" section for user clarification

**From figma_spec.md (if exists):**
- Extract all UXR-XXX (UX Requirements) for epic mapping
- **CRITICAL**: SKIP any UXR-XXX tagged with [UNCLEAR]
- Extract SCR-XXX screen references for UI Impact field
- Map UXR-XXX to appropriate epics

**From design.md:**
- Extract all NFR-XXX (Non-Functional Requirements)
- Extract all TR-XXX (Technical Requirements)
- Extract all DR-XXX (Data Requirements)
- **CRITICAL**: SKIP any NFR/TR/DR tagged with [UNCLEAR]
- Extract Core Entities for data-centric epics

**[UNCLEAR] Requirement Handling:**
- Create a "## Backlog Refinement Required" section in epics.md
- List all [UNCLEAR] tagged requirements with clarification questions
- These requirements will NOT be mapped to any epic until clarified

#### Requirements Analysis
- Total requirements count by category
- Identify requirement dependencies
- Group by functional area/outcome
- Detect cross-cutting concerns (security, performance)

#### Epic Grouping Strategy
**Grouping Principles:**
- Group by business outcome, not technical layer
- Keep related FR together (user-facing features)
- Map UXR-XXX from figma_spec.md to appropriate epics (when figma_spec.md exists)
- Group NFR + TR for infrastructure/platform epics
- Separate security/compliance into dedicated epic if >8 requirements
- Create data-focused epic for DR requirements if complex

### 4. Epic Generation Framework

**Before writing epics, list all epics to generate:**
| EP-ID | Epic Title | Requirement Count |
|-------|------------|-------------------|
| EP-TECH | (if green-field) | ... |
| EP-DATA | (if data layer detected) | ... |
| EP-001 | ... | ... |
| ... | ... | ... |
**Now expand each epic listed above.**

#### Epic Generation Content Rules

Follow the Epic Summary Table and Epic Description structure from `.propel/templates/epics-template.md`.

Apply the following content rules when populating the template:

**EP-TECH (Green-field Only):**
- **When to generate**: Green-field project detected (no existing codebase, no codeanalysis.md)
- **Position**: First epic (highest priority)
- **What to include**: Project scaffolding, CI/CD setup, development environment, base architecture
- **Business Value**: "Enables all subsequent development by establishing project foundation"
- **Key Deliverables**: Project structure, dev environment, CI/CD, base architecture, initial DB schema, auth foundation (if applicable)

**EP-DATA (When Data Layer Detected):**
- **When to generate**: design.md contains entity definitions OR DR-XXX ≥ 2
- **Position**: After EP-TECH if green-field, or as high-priority if brown-field
- **What to include**: Entity scaffolding, relationship mapping, constraints, seed/mock data
- **Business Value**: "Enables data operations for all feature epics requiring persistence"
- **Key Deliverables**: Entity creation (from models.md ERD), relationship mapping, data integrity rules, seed/mock data, migration scripts
- **Priority**: Critical (blocks feature epics requiring data operations)

**Feature Epics:**
- **Grouping principle**: By business outcome, not technical layer
- **Requirements mapping**: FR + UXR by functional area
- **Sizing rule**: One epic per major user outcome, limit ~12 requirements per epic
- **UI Impact determination**: Yes if figma_spec.md exists and epic maps UXR/SCR requirements
- **Screen References**: SCR-XXX list from figma_spec.md, or N/A if no UI impact

### 5. Design Generation
- Read template from `.propel/templates/epics-template.md`
- Populate epic table with all requirement mappings
- Generate detailed epic descriptions
- Use Write tool to create artifact `.propel/context/docs/epics.md`
- Ensure all template sections are populated with real data

### 6. Summary Presentation
- Present executive summary to user
- Display epic summary table with requirement counts
- Highlight EP-TECH if green-field project
- Provide link to detailed epics in `.propel/context/docs/epics.md`
- Present the Quality Assessment metrics

**Epic Validation (use sequential thinking MCP if available):**
- Validate all requirements are mapped to exactly one epic
- Ensure no orphaned requirements
- Verify epic sizing (5-12 requirements per epic)
- **Fallback**: Create explicit validation checklist and document decision rationale

### Quality Assurance Framework

#### Pre-Delivery Checklist
- [ ] **Project Type Detected**: Green-field or brown-field correctly identified
- [ ] **EP-TECH Included**: If green-field, EP-TECH is first epic
- [ ] **EP-DATA Included**: If entities in models.md or DR-XXX ≥2, EP-DATA is present
- [ ] **Requirement Coverage**: All FR, UXR, NFR, TR, DR mapped to exactly one epic
- [ ] **No Orphans**: Zero requirements without epic assignment
- [ ] **No Duplicates**: Each requirement appears in only one epic (unless explicitly shared)
- [ ] **Epic Sizing**: No epic exceeds ~12 requirements
- [ ] **UNCLEAR Handling**: [UNCLEAR] tagged requirements in backlog refinement list
- [ ] **Priority Ordering**: Epics ordered by business value then dependencies
- [ ] **Template Adherence**: Output follows epics-template.md structure

## Guardrails
- `rules/ai-assistant-usage-policy.md`: Explicit commands; minimal output
- `rules/dry-principle-guidelines.md`: Single source of truth; delta updates **[CRITICAL]**
- `rules/iterative-development-guide.md`: Strict phased workflow **[CRITICAL]**
- `rules/markdown-styleguide.md`: Front matter, heading hierarchy, code fences **[CRITICAL]**
- `rules/software-architecture-patterns.md`: Pattern selection, boundaries

**>>> ALWAYS: Execute Quality Evaluation. Follow the 4-tier evaluation framework instructions to evaluate the outcomes. <<<**

## Quality Evaluation

- **Invoke**: `.windsurf/workflows/evaluate-output.md`
  - **$OUTPUT_FILE**: `.propel/context/docs/epics.md`
  - **$SCOPE_FILES**: `.propel/context/docs/spec.md, .propel/context/docs/design.md`
  - **--workflow-type**: `epics`

---

*This epic generator ensures comprehensive requirement-to-epic mapping with proper business value alignment, priority ordering, and complete traceability.*
