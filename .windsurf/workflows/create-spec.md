---
description: Generates functional requirements from feature specifications or direct text input. Creates spec.md with FR-XXX requirements and Use Case analysis with PlantUML diagrams.
auto_execution_mode: 1
---

# Spec Generator
As an expert Business Analyst and Product Manager, generate Functional Requirements (FR-XXX) and Use Case specifications. This workflow focuses on business requirements and user-facing functionality.

## Input Parameters

### $ARGUMENTS (Mandatory) - Project Scope File
**Accepts:** Feature specifications | Business requirements | Project scope documents | User needs text
**Supported File Types:** .pdf | .txt | .md | .docx

### $AI_TRIAGE (Optional) - AI Suitability Assessment
**Default:** `true`
- `true` - Run Phase 0 GenAI Suitability Triage, tag features with `[AI-CANDIDATE]`, `[DETERMINISTIC]`, or `[HYBRID]`
- `false` - Skip AI triage for pure deterministic projects. All requirements treated as deterministic by downstream workflows.

**Note:** When `$AI_TRIAGE=false`, the spec.md will contain no AI classification tags. Downstream workflows (design-architecture, etc.) will automatically treat this as a deterministic-only project and skip AI-related sections.

### Input Processing Instructions
**CRITICAL**: Before proceeding with requirements generation, you MUST determine input type and process accordingly:

#### Input Type Detection
1. **File Path Detection**: Check if `$ARGUMENTS` contains a file path (contains file extensions .pdf, .txt, .md, .docx)
2. **Direct Text Detection**: If `$ARGUMENTS` doesn't contain a file extension, treat it as direct specification text

#### Input Type Handling

This unified command automatically processes various requirement sources:

**Feature Specifications**
- **Source**: Feature request documents or descriptions
- **Focus**: New capability addition with business justification
- **Output**: Comprehensive spec with implementation roadmap

**Business Requirements**
- **Source**: Business case documents or strategic initiatives
- **Focus**: Business-driven functionality with ROI analysis
- **Output**: Business-aligned spec with success metrics

**Project Scope**
- **Source**: Project charter or scope documents
- **Focus**: Complete project requirements with phases
- **Output**: Phased spec with milestone definitions

**User Needs Analysis**
- **Source**: User research, feedback, or journey maps
- **Focus**: User-centric requirements with experience priorities
- **Output**: User-focused spec with usability criteria

#### File Input Processing
If `$ARGUMENTS` is a file path:
1. Verify file exists and read contents (supports .pdf, .txt, .md, .docx)
2. Validate content is readable and contains relevant specification information

#### Direct Text Processing
If `$ARGUMENTS` is direct text: Use it directly as source material for requirements generation.

#### Binary File Conversion (.docx/.pdf)
If native reading fails for .docx/.pdf, generate and run inline:
```bash
python -c "
import sys;from pathlib import Path;p=Path(sys.argv[1]);ext=p.suffix.lower()
if ext=='.docx':exec('try:from docx import Document\nexcept:__import__(\"subprocess\").check_call([sys.executable,\"-m\",\"pip\",\"install\",\"python-docx\",\"-q\"]);from docx import Document');print('\\n'.join(x.text for x in Document(p).paragraphs if x.text.strip()))
elif ext=='.pdf':exec('try:import pdfplumber\nexcept:__import__(\"subprocess\").check_call([sys.executable,\"-m\",\"pip\",\"install\",\"pdfplumber\",\"-q\"]);import pdfplumber');pdf=pdfplumber.open(p);print('\\n'.join(pg.extract_text()or'' for pg in pdf.pages));pdf.close()
" "$ARGUMENTS"
```
Use extracted text as input. If fails: request .md/.txt or pasted content.

#### Large files handling (>50KB):
1. First pass: Extract only headings/structure
2. Second pass: Extract sections containing "requirement", "acceptance", "must", "shall", "user story"
3. Skip: Appendix, revision history, references, background sections
4. If still too large: Summarize verbose paragraphs to bullet points

#### Design Asset Processing (UI Impact Only)
If requirements involve UI changes, extract design references:
- Figma links (figma.com/file/, figma.com/proto/)
- Image assets (.png, .jpg, .svg, .sketch) - copy to `.propel/context/design/`
- Design tokens (colors, typography, spacing)

#### Fallback Handling
- If file cannot be read: Request alternative path or paste content directly
- If no input provided: Request file path or specification text

## Output
- Artifact generation:
  - `.propel/context/docs/spec.md`
  - Print the following:
    - List of rules used by the workflow in bulleted format
    - Evaluation Scores in tabular format with average score.
    - Evaluation summary (less than 100 words).
    **Do not save as file.** (console output only)

**Note:**
- **File Handling**: IF file exists → UPDATE changed sections only (delta mode). IF file does not exist → CREATE complete file.
- Always create the output file in manageable smaller chunks to manage memory and processing constraints.
- Always generate a single unified document using `.propel/templates/requirements-template.md` template for spec
- spec.md structure is defined by the referenced template. Populate all template sections with analyzed content.

## Execution Flow

### Core Principles
- **FIRST**: Process `$ARGUMENTS` input according to Input Processing Instructions above
- **SECOND**: Extract and analyze the specification content. For hidden requirements, identify: (a) Implicit user expectations (b) Assumed system behaviors (c) Integration touchpoints
- **THIRD**: Analyze project scope and business context before requirements generation
- Review existing codebase (if available) to understand current state and constraints
- For each identified requirement, answer: (1) Who needs this? (2) What triggers it? (3) What is the success outcome? (4) What are the failure scenarios?
- Update existing sections incrementally when file exists; avoid complete overwrites
- Split complex requirements by functional areas when applicable
- Ensure requirements are testable, measurable, and aligned with business objectives
- Focus on Functional Requirements (FR-XXX)
- Generate a single unified document at .propel/context/docs/spec.md only

#### Content Processing Workflow
1. **Input Analysis**: Determine if `$ARGUMENTS` is file path or direct text
2. **Content Extraction**: Read file content OR use direct text as source material
3. **Content Parsing**: Extract key business requirements, user needs, and technical constraints
4. **Context Integration**: Combine extracted content with codebase analysis and business context
5. **Requirements Generation**: Create comprehensive spec based on processed specification content

### Deep Requirements Analysis Methodology (use Sequential-Thinking MCP)

Optimize for requirements completeness and implementation success over speed.

**Fallback Mechanism:** If the sequential-thinking MCP tool fails or is unavailable, automatically fall back to standard iterative analysis approach using Web fetch:
- Perform systematic step-by-step requirement analysis
- Use structured thinking with explicit validation checkpoints
- Apply the same comprehensive methodology without the sequential-thinking tool
- Ensure no degradation in analysis quality or completeness

#### 0. GenAI Suitability Triage [CONDITIONAL: $AI_TRIAGE=true]

**Execution Gate:**
- IF `$AI_TRIAGE=true` (default) → Execute this phase
- IF `$AI_TRIAGE=false` → SKIP this phase entirely, proceed to Phase 1

**When Executed ($AI_TRIAGE=true):**
Before deep analysis, scan requirements for AI-fit indicators:
- **AI-Fit Keywords:** "generate", "summarize", "answer questions", "extract", "classify", "recommend", "conversational"
- **Tag Features:** Mark each feature as `[AI-CANDIDATE]`, `[DETERMINISTIC]`, or `[HYBRID]`
- **Output:** AI fit summary in spec.md to inform downstream design-architecture workflow

Example tagging in FR section:
```
- FR-001: [DETERMINISTIC] System MUST calculate invoice totals
- FR-002: [AI-CANDIDATE] System MUST generate customer email responses
- FR-003: [HYBRID] System MUST recommend products (AI suggests, user confirms)
```

**When Skipped ($AI_TRIAGE=false):**
- Do NOT add `[AI-CANDIDATE]`, `[DETERMINISTIC]`, or `[HYBRID]` tags to requirements
- Downstream workflows will detect absence of AI tags and treat project as deterministic-only
- AI-related sections (AIR-XXX, AI Architecture Pattern) will be automatically skipped

#### 1. Business Context Analysis
For business context, document for each stakeholder: Role, Primary goal, Key constraint. Then proceed:
- **Stakeholder Identification**: Map all stakeholders and their requirements priorities
- **Business Objectives**: Align features with strategic business goals and KPIs
- **User Journey Mapping**: Document end-to-end user flows and interaction points
- **Success Metrics**: Define measurable success criteria and acceptance standards
- **Risk Assessment**: Identify business risks and mitigation strategies

#### 2. Technical Feasibility Assessment
- **Integration Requirements**: Identify system dependencies and integration points
- **Performance Implications**: Analyze scalability and performance requirements
- **Security Considerations**: Document security requirements and compliance needs

#### 3. Design and User Experience Analysis (UI Impact Only)
**Apply only if requirements include user interface changes:**
- **UI Impact Assessment**: Clearly identify which features require UI modifications
- **Visual Design Requirements**: Extract design specifications from wireframes/*
- **Design System Mapping**: Document colors, typography, spacing, components (UI only)
- **UI/UX Patterns**: Identify interaction patterns and micro-animations
- **Responsive Design**: Document breakpoints and adaptive behaviors
- **Accessibility Standards**: WCAG compliance requirements from designs

#### 4. Existing System Analysis (If Applicable)
- **Current State Documentation**: Map existing features and functionality
- **Gap Analysis**: Identify differences between current and desired states
- **Impact Assessment**: Analyze effects on existing features and workflows
- **Migration Requirements**: Document data migration and transition needs
- **Backward Compatibility**: Ensure existing functionality preservation

#### 5. External Research and Standards
- **Industry Best Practices**: Evaluate exemplar open source projects that implement these practices
- **Regulatory Compliance**: Perform targeted web searches to identify applicable regulations and standards
- **Competitive Analysis**: Reference style guides and standards from recognized organizations
- **User Research**: Incorporate user feedback and usability studies.
- **Community Insights**: Perform targeted web searches for up-to-date guides and community insights
- **Evaluate Information**: Consider the recency of information (prefer current practices over outdated ones). Note when practices are controversial or have multiple valid approaches

#### 6. Synthesize Findings
- Organize discoveries into clear categories (e.g., "Must Have", "Recommended", "Optional"). 
- Provide specific examples from real projects when possible
- Explain the reasoning behind each best practice
- Highlight any technology-specific or domain-specific considerations
- Provide links to authoritative sources for deeper exploration

### Essential Project Intelligence

#### Reference Materials Integration
- **Existing Codebase**: Analyze `app`, `client`, `backend`, `server`, custom folders for current implementation patterns
- **Documentation Standards**: Follow existing documentation patterns and conventions

*** Comprehensive understanding of business context and technical constraints is non-negotiable ***

#### References Package
```yaml
- url: [Industry standards documentation]
  why: [Compliance requirements and best practices]
  
- file: [existing/feature/path]
  why: [Current implementation to maintain compatibility]
  
- doc: [Framework/library documentation URL]
  section: [Architecture constraints and capabilities]
  critical: [Key limitations affecting requirements]

- stakeholder: [Stakeholder interview notes/feedback]
  priority: [Critical requirements from key stakeholders]
```

### Spec Generation Framework

#### Critical Context Integration

**Business Context**
- Stakeholder requirements and priorities
- Business objectives and success metrics
- User personas and journey maps
- Market analysis and competitive positioning

**Technical Context**
- Integration points and API requirements
- Performance and scalability considerations

**Requirements Specification**
- Detailed functional requirements with acceptance criteria (FR-XXX)
- Use Case specifications with PlantUML diagrams (UC-XXX)

**Design Context (UI Impact Only)**
- Visual references: Figma URLs OR design images (PNG, JPG, SVG, Sketch files)
- Design system tokens (colors, typography, spacing) for UI components
- Component specifications with visual asset references (Figma frames OR screenshots)
- Interaction patterns and animation requirements
- Responsive design breakpoints and behaviors

**Constraints and Dependencies**
- Technical limitations and workarounds
- External system dependencies
- Regulatory and compliance requirements
- Timeline and resource constraints

**Implementation Considerations**
- Development approach and methodology
- Testing strategy and validation criteria
- Deployment and rollout planning
- Maintenance and support requirements

#### Requirements Structure Architecture

**Before writing FR-XXX requirements, list all requirements to generate:**
| FR-ID | Summary |
|-------|---------|
| ... | ... |
**Now expand each FR listed above with full specification.**

**Functional Requirements (FR-XXX)**
- Feature specifications with detailed behaviors
- Business rules and logic documentation
- System capabilities and constraints
- Clear acceptance criteria for each requirement

**Use Case Analysis (UC-XXX)**
- Actor identification and system boundaries
- Success scenarios and alternative flows
- PlantUML diagrams for each use case
- Preconditions and postconditions

### Stakeholder Analysis Framework

#### Stakeholder Mapping
- **Primary Stakeholders**: Direct users and beneficiaries
- **Secondary Stakeholders**: Indirect users and support teams
- **Technical Stakeholders**: Development and operations teams
- **Business Stakeholders**: Management and decision makers

#### Requirements Prioritization
- **MoSCoW Method**: Must have, Should have, Could have, Won't have
- **Value vs Effort Matrix**: High value/low effort items prioritized
- **Risk Assessment**: Critical path and high-risk items identified
- **Dependencies Mapping**: Sequential requirements ordering

### Workflow Separation

**This Command Generates**: Requirements -> Use Cases
- Functional Requirements (FR-XXX)
- Use Case Analysis with PlantUML diagrams (UC-XXX)

**spec.md Document Structure** (per requirements-template.md):
- Goal statement with current vs desired state
- Why section (business value, integration, problems solved)
- What section (user-visible behavior, success criteria)
- Functional Requirements (FR-XXX) with MUST statements
- Use Case Analysis:
  - Actors & System Boundary
  - Use Case Specifications (UC-XXX) with PlantUML diagrams
- Risks & Mitigations (top 5, scoped to FR)
- Constraints & Assumptions (top 5, scoped to FR)

### Quality Assurance Framework

#### Pre-Delivery Checklist
- [ ] **Business Alignment**: Requirements align with business objectives and KPIs
- [ ] **Stakeholder Coverage**: All stakeholder needs identified and addressed
- [ ] **Testability**: All requirements have clear acceptance criteria
- [ ] **FR Completeness**: Functional requirements (FR-XXX) comprehensive
- [ ] **Clarity**: Requirements are unambiguous and well-documented
- [ ] **Traceability**: Requirements linked to business objectives and user needs
- [ ] **Risk Assessment**: Potential risks identified with mitigation strategies
- [ ] **Use Case Diagrams**: Each use case (UC-XXX) has corresponding PlantUML diagram

## Guardrails
- `rules/ai-assistant-usage-policy.md`: Explicit commands; minimal output
- `rules/code-anti-patterns.md`: Avoid god objects, circular deps, magic constants
- `rules/dry-principle-guidelines.md`: Single source of truth; delta updates **[CRITICAL]**
- `rules/iterative-development-guide.md`: Strict phased workflow **[CRITICAL]**
- `rules/language-agnostic-standards.md`: KISS, YAGNI, size limits, clear naming
- `rules/markdown-styleguide.md`: Front matter, heading hierarchy, code fences **[CRITICAL]**
- `rules/performance-best-practices.md`: Optimize after measurement
- `rules/security-standards-owasp.md`: OWASP Top 10 alignment

- `rules/uml-text-code-standards.md`: PlantUML/Mermaid notation standards

**>>> ALWAYS: Execute Quality Evaluation. Follow the 4-tier evaluation framework instructions to evaluate the outcomes. <<<**

## Quality Evaluation

- **Invoke**: `.windsurf/workflows/evaluate-output.md`
  - **$OUTPUT_FILE**: Primary artifact generated by this workflow (per Output section)
  - **$SCOPE_FILES**: Input source(s) provided to this workflow (per Input Parameters section)
  - **--workflow-type**: `spec`

---

*This spec generator ensures comprehensive, business-aligned requirements with FR-XXX and Use Case (UC-XXX) documentation for successful downstream workflows.*