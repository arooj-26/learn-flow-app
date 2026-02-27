# LearnFlow Content Management

This directory contains all the learning content for the LearnFlow platform.

## Directory Structure

```
content/
├── modules/
│   ├── basics/
│   │   ├── variables-and-types.md
│   │   ├── operators.md
│   │   ├── input-output.md
│   │   └── strings.md
│   ├── control-flow/
│   │   ├── if-statements.md
│   │   ├── for-loops.md
│   │   ├── while-loops.md
│   │   └── break-continue.md
│   ├── data-structures/
│   │   ├── lists.md
│   │   ├── tuples.md
│   │   ├── dictionaries.md
│   │   ├── sets.md
│   │   └── list-comprehensions.md
│   ├── functions/
│   │   ├── defining-functions.md
│   │   ├── return-values.md
│   │   ├── arguments.md
│   │   ├── lambda-functions.md
│   │   └── scope.md
│   ├── oop/
│   │   ├── classes.md
│   │   ├── objects.md
│   │   ├── methods.md
│   │   ├── inheritance.md
│   │   └── polymorphism.md
│   ├── files/
│   │   ├── reading-files.md
│   │   ├── writing-files.md
│   │   ├── file-context.md
│   │   └── json-csv.md
│   ├── errors/
│   │   ├── try-except.md
│   │   ├── exception-types.md
│   │   ├── raising-exceptions.md
│   │   └── custom-exceptions.md
│   └── libraries/
│       ├── import-statements.md
│       ├── standard-library.md
│       ├── pip-packages.md
│       └── virtual-environments.md
├── TEMPLATE.md
└── README.md
```

## Adding New Content

### 1. Copy the Template

Copy `TEMPLATE.md` to the appropriate module folder with the correct filename.

**File naming convention:**
- Use lowercase with hyphens
- Match the topic name from the database
- Example: "Variables & Types" → `variables-and-types.md`

### 2. Write the Content

The markdown file has two sections:

#### Main Content
Write your lesson content using standard markdown:
- Use `#`, `##`, `###` for headings
- Use code blocks with \`\`\`python
- Use tables, lists, and emphasis as needed

#### Exercises Section
Exercises are defined in YAML format between special comments:

```markdown
<!-- EXERCISE_START -->
```yaml
exercises:
  - title: "Exercise Title"
    difficulty: basic  # basic, intermediate, or advanced
    description: "What the student needs to do"
    starter_code: |
      # Code that appears in the editor

    expected_output: "What the output should be"
    hints:
      - "Hint 1"
      - "Hint 2"
    solution: |
      # Optional solution code
```
<!-- EXERCISE_END -->
```

### 3. Exercise Guidelines

Each topic should have **6 exercises**:
- 2 Basic (difficulty: basic)
- 2 Intermediate (difficulty: intermediate)
- 2 Advanced (difficulty: advanced)

**Exercise fields:**
| Field | Required | Description |
|-------|----------|-------------|
| title | Yes | Short descriptive title |
| difficulty | Yes | basic, intermediate, or advanced |
| description | Yes | Clear instructions for the student |
| starter_code | Yes | Initial code in the editor |
| expected_output | Yes | What output is expected |
| hints | Yes | Array of helpful hints |
| solution | No | Complete solution (optional) |

### 4. Update the Content Parser

If you add a new topic that doesn't match existing mappings, update the `TOPIC_FILE_MAP` in `src/lib/content-parser.ts`:

```typescript
const TOPIC_FILE_MAP: Record<string, string> = {
  'Topic Name': 'module-folder/topic-filename.md',
  // ... other mappings
};
```

## Testing Your Content

1. Restart the Next.js development server
2. Navigate to the topic in the app
3. Verify:
   - Content renders correctly
   - All 6 exercises appear
   - Code editor loads starter code
   - Hints display properly

## Best Practices

1. **Clear explanations** - Start simple, build complexity
2. **Code examples** - Show before explaining
3. **Progressive difficulty** - Exercises should build on each other
4. **Helpful hints** - Guide without giving away the answer
5. **Practical examples** - Use real-world scenarios

## Markdown Tips

### Code Blocks
```markdown
\`\`\`python
def example():
    return "Hello"
\`\`\`
```

### Tables
```markdown
| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |
```

### Important Notes
```markdown
> **Note:** Important information here.
```

## Questions?

If you need help adding content, check existing files for examples or ask the team.
