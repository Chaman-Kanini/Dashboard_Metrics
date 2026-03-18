# Task - [TASK_XXX]

## Requirement Reference
- User Story: [us_XXX] (extracted from input)
- Story Location: [.propel/context/tasks/us_XXX/us_XXX.md]
- Acceptance Criteria:  
    - [List of AC's applicable for the task. Read from the User Story]
- Edge Case:
    - [List of Edge Cases applicable for the task. Read from the User Story]

## Design References (Frontend Tasks Only)
| Reference Type | Value |
|----------------|-------|
| **UI Impact** | [Yes/No] |
| **Figma URL** | [Figma frame URL with node-id, or N/A] |
| **Wireframe Status** | [AVAILABLE / PENDING / EXTERNAL / N/A] |
| **Wireframe Type** | [HTML / PNG / JPG / URL / N/A] |
| **Wireframe Path/URL** | [local path, external URL, or "TODO: Provide wireframe..."] |
| **Screen Spec** | [figma_spec.md#SCR-XXX, or N/A] |
| **UXR Requirements** | [UXR-XXX, or N/A] |
| **Design Tokens** | [designsystem.md section reference, or N/A] |

> **Wireframe Status Legend:**
> - **AVAILABLE**: Local file exists at specified path
> - **PENDING**: UI-impacting task awaiting wireframe (provide file or URL)
> - **EXTERNAL**: Wireframe provided via external URL
> - **N/A**: Task has no UI impact
>
> If UI Impact = No, all design references should be N/A

### **CRITICAL: Wireframe Implementation Requirement (UI Tasks Only)**
**IF Wireframe Status = AVAILABLE or EXTERNAL:**
- **MUST** open and reference the wireframe file/URL during UI implementation
- **MUST** match layout, spacing, typography, and colors from the wireframe
- **MUST** implement all states shown in wireframe (default, hover, focus, error, loading)
- **MUST** validate implementation against wireframe at breakpoints: 375px, 768px, 1440px
- Run `/analyze-ux` after implementation to verify pixel-perfect alignment

## Applicable Technology Stack
| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | [e.g., React] | [e.g., 19.x] |
| Backend | [e.g., .NET] | [e.g., 8.0] |
| Database | [e.g., PostgreSQL] | [e.g., 16.x] |
| Library | [e.g., React Router] | [e.g., v7] |
| AI/ML | [e.g., OpenAI GPT-4, or N/A] | [e.g., gpt-4-turbo] |
| Vector Store | [e.g., Pinecone, pgvector, or N/A] | [e.g., v2] |
| AI Gateway | [e.g., LiteLLM, Portkey, or N/A] | [e.g., 1.x] |

**Note**: All code, and libraries, MUST be compatible with versions above.

## AI References (AI Tasks Only)
| Reference Type | Value |
|----------------|-------|
| **AI Impact** | [Yes/No] |
| **AIR Requirements** | [AIR-001, AIR-002, or N/A] |
| **AI Pattern** | [RAG / Tool Calling / Fine-tuning / Hybrid / N/A] |
| **Prompt Template Path** | [prompts/[feature]/, or N/A] |
| **Guardrails Config** | [config path, or N/A] |
| **Model Provider** | [OpenAI / Anthropic / Azure OpenAI / N/A] |

> **AI Impact Legend:**
> - **Yes**: Task involves LLM integration, RAG pipeline, prompt engineering, or AI infrastructure
> - **No**: Task is deterministic (FE/BE/DB only)
>
> If AI Impact = No, all AI references should be N/A

### **CRITICAL: AI Implementation Requirement (AI Tasks Only)**
**IF AI Impact = Yes:**
- **MUST** reference prompt templates from Prompt Template Path during implementation
- **MUST** implement guardrails for input sanitization and output validation
- **MUST** enforce token budget limits per AIR-O01 requirements
- **MUST** implement fallback logic for low-confidence responses
- **MUST** log all prompts/responses for audit (redact PII)
- **MUST** handle model failures gracefully (timeout, rate limit, 5xx errors)

## Task Overview
[High level Task description -- purpose, and capabilities]

## Dependent Tasks
- [List of mandatory tasks under 'Artefacts/Tasks' to be completed before the start of this task.]

## Impacted Components
- [List of impacted classes / modules. List updated or new along with project.]

## Implementation Plan
- [List of implementation plan to perform the task]
**Focus on how to implement**

## Current Project State
- [Project structure in tree format. Refer to 'app' folder for the Frontend and 'Server' for the backend code. Shall remain as placeholder to be updated during the execution of the task based on the completion of the dependent task.]

## Expected Changes
| Action | File Path | Description |
|--------|-----------|-------------|
| CREATE | [full path] | [what this new file does] |
| MODIFY | [full path] | [specific section/function to change] |
| DELETE | [full path] | [reason for removal] |

> Only list concrete, verifiable file operations. No speculative directory trees.

## External References
- [External URL links based on the research]

## Build Commands
- [Refer to applicable technology stack specific build commands](../.propel/build/)

## Implementation Validation Strategy
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)
- [ ] **[UI Tasks]** Visual comparison against wireframe completed at 375px, 768px, 1440px
- [ ] **[UI Tasks]** Run `/analyze-ux` to validate wireframe alignment
- [ ] **[AI Tasks]** Prompt templates validated with test inputs
- [ ] **[AI Tasks]** Guardrails tested for input sanitization and output validation
- [ ] **[AI Tasks]** Fallback logic tested with low-confidence/error scenarios
- [ ] **[AI Tasks]** Token budget enforcement verified
- [ ] **[AI Tasks]** Audit logging verified (no PII in logs)

## Implementation Checklist
- [List of todo to accomplish the task aligned with the implementation plan. Provide a provision to update the todo list based on the completion of the task.]
- **[UI Tasks - MANDATORY]** Reference wireframe from Design References table during implementation
- **[UI Tasks - MANDATORY]** Validate UI matches wireframe before marking task complete
- **[AI Tasks - MANDATORY]** Reference prompt templates from AI References table during implementation
- **[AI Tasks - MANDATORY]** Implement and test guardrails before marking task complete
- **[AI Tasks - MANDATORY]** Verify AIR-XXX requirements are met (quality, safety, operational)