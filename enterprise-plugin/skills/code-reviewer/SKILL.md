# Code Reviewer Skill

## Skill Name
`code-reviewer`

## Description
Skill for automated code review with a focus on quality, readability, and best practices in projects related to Polish text processing.

## Capabilities
- Code style analysis
- Code duplication detection
- Suggestions for refactoring and improvement
- Integration with PR comments

## Usage
```yaml
skill: code-reviewer
options:
  language: ["python", "javascript", "typescript"]
  style-guide: "pep8"
  max-complexity: 10
```

## Output
Returns a list of suggestions in Markdown format with line references.
