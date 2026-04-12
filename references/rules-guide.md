# Rules Guide

## Purpose
This guide provides standard operating procedures for creating and managing project rules that govern AI agent behavior.

## Standard Operating Procedures (SOPs)

### Creating New Rules
1. Identify the trigger condition (file type, action, context)
2. Define the rule scope (glob pattern or specific files)
3. Write clear, actionable constraints
4. Include examples of correct/incorrect behavior

### Rule Structure
```markdown
---
trigger: [trigger_type]
globs: [file_patterns]
description: [brief description of rule purpose]
---

# [Rule Title]

## Executive Summary
[One sentence explaining the rule's purpose]

## Critical Constraints
- 🔴 **NEVER** [prohibited action]
- 🟡 **ALWAYS** [required action]
- 🟢 **CONSIDER** [recommended action]

## Code Patterns
### When to Apply
[Describe conditions under which rule applies]

### Examples
✅ **Good**: [Correct example]
❌ **Bad**: [Incorrect example]

## Context Injection Points
[List places where this rule should be applied]
```

### Rule Activation Types
- **File-based**: Triggered when specific file types are modified
- **Action-based**: Triggered by specific actions (commits, deployments)
- **Context-based**: Triggered by project context or state
- **Model Decision**: Triggered during decision-making processes