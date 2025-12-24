/sdd-spec

**Purpose**: Generate implementation from explicit technical specifications for AI-assisted development

**Instructions**:
You are practicing Spec-Driven Development (SDD). Treat specifications as version control for thinking.

1. **Specification Structure**
   - **Product Requirements Document (PRD)**: Business goals, user needs, success metrics
   - **Technical Specification**: Architecture decisions, data models, API contracts
   - **Implementation Plan**: Concrete steps, file structure, testing strategy
   - All specs in Markdown for human readability and AI parseability

2. **SDD Workflow**
Requirement Change → Update Spec → Regenerate Implementation

- Changes to specs trigger automatic implementation updates
- Modify PRD → Affected implementation plans update automatically
- Change user story → Corresponding API endpoints regenerate
- Specs are source of truth, implementation is derived

3. **Specification Components**
- **Decision Records**: Why choices were made, alternatives considered
- **Interface Contracts**: APIs, data schemas, message formats
- **Constraints**: Performance, security, scalability requirements
- **Test Scenarios**: Expected behaviors, edge cases, failure modes

4. **AI Agent Integration**
- Expose specs through Figma MCP server or filesystem
- Ask agent to generate multiple implementations from same spec
- Explore design directions without rigid single implementation
- Use specs for what-if/simulation experiments

5. **Evolution Management**
- Specs are reviewable (PR process for technical decisions)
- Specs are evolvable (pivot by changing spec, not code)
- Maintain spec versioning with semantic versioning
- Link specs to implementation via automated tooling

**Output Format**:
- PRD.md (product requirements)
- SPEC.md (technical specification)
- IMPLEMENTATION.md (execution plan)
- DECISION-LOG.md (architectural decision records)

**Quality Validation**:
- Specs are explicit and unambiguous
- All assumptions documented in decision records
- Implementation derives deterministically from spec
- Specs pass "literal-minded AI" test (no implicit knowledge required)

**GitHub Spec Kit Integration**: Use https://github.com/github/spec-kit for tooling
