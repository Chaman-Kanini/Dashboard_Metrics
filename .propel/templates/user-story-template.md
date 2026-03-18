# User Story - [US_XXX]

## Quick Reference Schema
```yaml
# User Story:
  * ID: []              # Unique ID to be populated
  * Title: []           # To be populated
## Description:
   * []                 # To be populated ("As a ... I want ... so that ...")
## Acceptance Criteria:
   * []                 # To be populated (Given/When/Then)
## Edge Cases:
   * []                 # To be populated
## Traceability:
### Parent:
    * []                # mapped to epic ID
### Tags:
    * []                # To be populated (NFR, FR, TR, DR, UXR, AIR, <Platform tag>, <Domain tag>)
### Dependencies:
    * []                # To be populated (List of dependent user story IDs or N/A if none or not applicable)
```
---

## Story ID
   * ID Format: US_<unique seq num>

## Story Title
   * [Title of the story in less than 10 words]

## Description
  * Description Format: "As a..., I want..., so that..."

## Acceptance Criteria
  * Acceptance Criteria Format: "Given [initial state], When [action], Then [expected outcome]"

## Edge Cases
   * What happens when [boundary condition]?
   * How does system handle [error scenario]?

## Traceability
### Parent Epic
    * Epic : [Epic ID]

### Requirement Tags
    * [NFR, FR, TR, DR, UXR, AIR, <Platform tag>, <Domain tag>]

### Dependencies
    * [List of dependent user story IDs or N/A if none or not applicable]

## Visual Design Context (UI Stories Only)
### Screen Specifications
- **Screen ID(s)**: [SCR-XXX from figma_spec.md, or N/A if no UI impact]
- **Figma Spec Reference**: [.propel/context/docs/figma_spec.md#SCR-XXX, or N/A]

### Wireframe References
| Field | Value |
|-------|-------|
| **Status** | [AVAILABLE / PENDING / EXTERNAL / N/A] |
| **Type** | [HTML / PNG / JPG / URL / N/A] |
| **Path/URL** | [local path, external URL, or "TODO: Provide wireframe - upload to `.propel/context/wireframes/Hi-Fi/wireframe-SCR-XXX-{name}.[html|png|jpg]` or add external URL"] |

> **Wireframe Status Legend:**
> - **AVAILABLE**: Local file exists at specified path
> - **PENDING**: UI-impacting story awaiting wireframe (provide file or URL)
> - **EXTERNAL**: Wireframe provided via external URL
> - **N/A**: Story has no UI impact

### UX Requirements
- **UXR Mappings**: [UXR-XXX from figma_spec.md, or N/A if no UI impact]