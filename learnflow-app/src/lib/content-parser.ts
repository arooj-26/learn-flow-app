/**
 * Content Parser - Reads markdown files and extracts content and exercises
 *
 * Markdown files should have the following structure:
 * 1. Main content in markdown format
 * 2. Exercises in YAML format between <!-- EXERCISE_START --> and <!-- EXERCISE_END -->
 */

import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import { marked } from 'marked';

const CONTENT_DIR = path.join(process.cwd(), 'content', 'modules');

// Map topic names to file paths (all 64 topics across 8 modules)
const TOPIC_FILE_MAP: Record<string, string> = {
  // Python Basics (8)
  'Variables & Data Types': 'basics/variables-and-types.md',
  'Numbers & Math': 'basics/numbers-and-math.md',
  'Strings': 'basics/strings.md',
  'String Methods': 'basics/string-methods.md',
  'Type Conversion': 'basics/type-conversion.md',
  'Input & Output': 'basics/input-output.md',
  'Comments & Style': 'basics/comments-and-style.md',
  'Boolean Logic': 'basics/boolean-logic.md',
  // Control Flow (8)
  'If Statements': 'control-flow/if-statements.md',
  'Elif & Else': 'control-flow/elif-and-else.md',
  'Comparison Operators': 'control-flow/comparison-operators.md',
  'Logical Operators': 'control-flow/logical-operators.md',
  'While Loops': 'control-flow/while-loops.md',
  'For Loops': 'control-flow/for-loops.md',
  'Break & Continue': 'control-flow/break-continue.md',
  'Nested Loops': 'control-flow/nested-loops.md',
  // Data Structures (8)
  'Lists': 'data-structures/lists.md',
  'List Methods': 'data-structures/list-methods.md',
  'Tuples': 'data-structures/tuples.md',
  'Dictionaries': 'data-structures/dictionaries.md',
  'Dictionary Methods': 'data-structures/dictionary-methods.md',
  'Sets': 'data-structures/sets.md',
  'List Comprehensions': 'data-structures/list-comprehensions.md',
  'Nested Structures': 'data-structures/nested-structures.md',
  // Functions (8)
  'Defining Functions': 'functions/defining-functions.md',
  'Parameters & Arguments': 'functions/parameters-and-arguments.md',
  'Return Values': 'functions/return-values.md',
  'Default Parameters': 'functions/default-parameters.md',
  'Variable Scope': 'functions/variable-scope.md',
  'Lambda Functions': 'functions/lambda-functions.md',
  'Recursion': 'functions/recursion.md',
  'Decorators': 'functions/decorators.md',
  // OOP (8)
  'Classes & Objects': 'oop/classes-and-objects.md',
  'Constructors': 'oop/constructors.md',
  'Instance Methods': 'oop/instance-methods.md',
  'Class Variables': 'oop/class-variables.md',
  'Inheritance': 'oop/inheritance.md',
  'Method Overriding': 'oop/method-overriding.md',
  'Polymorphism': 'oop/polymorphism.md',
  'Encapsulation': 'oop/encapsulation.md',
  // File Handling (8)
  'Opening Files': 'files/opening-files.md',
  'Reading Files': 'files/reading-files.md',
  'Writing Files': 'files/writing-files.md',
  'File Modes': 'files/file-modes.md',
  'CSV Files': 'files/csv-files.md',
  'JSON Files': 'files/json-files.md',
  'Context Managers': 'files/context-managers.md',
  'File Paths': 'files/file-paths.md',
  // Error Handling (8)
  'Try & Except': 'errors/try-and-except.md',
  'Multiple Exceptions': 'errors/multiple-exceptions.md',
  'Finally Block': 'errors/finally-block.md',
  'Raising Exceptions': 'errors/raising-exceptions.md',
  'Custom Exceptions': 'errors/custom-exceptions.md',
  'Assertions': 'errors/assertions.md',
  'Logging': 'errors/logging.md',
  'Debugging Techniques': 'errors/debugging-techniques.md',
  // Libraries & Modules (8)
  'Importing Modules': 'libraries/importing-modules.md',
  'Standard Library': 'libraries/standard-library.md',
  'Math Module': 'libraries/math-module.md',
  'Random Module': 'libraries/random-module.md',
  'Datetime Module': 'libraries/datetime-module.md',
  'OS Module': 'libraries/os-module.md',
  'pip & Packages': 'libraries/pip-and-packages.md',
  'Virtual Environments': 'libraries/virtual-environments.md',
};

export interface Exercise {
  id?: string;
  title: string;
  difficulty: 'basic' | 'intermediate' | 'advanced';
  description: string;
  starter_code: string;
  expected_output: string;
  hints: string[];
  solution?: string;
  completed?: boolean;
}

export interface TopicContent {
  content: string;
  exercises: Exercise[];
}

/**
 * Parse a markdown file and extract content and exercises
 */
export function parseTopicContent(topicName: string): TopicContent {
  const filePath = TOPIC_FILE_MAP[topicName];

  if (!filePath) {
    return getDefaultContent(topicName);
  }

  const fullPath = path.join(CONTENT_DIR, filePath);

  if (!fs.existsSync(fullPath)) {
    console.log(`Content file not found: ${fullPath}`);
    return getDefaultContent(topicName);
  }

  try {
    const fileContent = fs.readFileSync(fullPath, 'utf-8');
    return parseMarkdownContent(fileContent, topicName);
  } catch (error) {
    console.error(`Error reading content file: ${error}`);
    return getDefaultContent(topicName);
  }
}

/**
 * Parse markdown content and extract exercises
 */
function parseMarkdownContent(markdown: string, topicName: string): TopicContent {
  // Split content and exercises
  const exerciseStartMatch = markdown.match(/<!-- EXERCISE_START -->/);
  const exerciseEndMatch = markdown.match(/<!-- EXERCISE_END -->/);

  let mainContent = markdown;
  let exercises: Exercise[] = [];

  if (exerciseStartMatch && exerciseEndMatch) {
    const startIndex = exerciseStartMatch.index!;
    const endIndex = exerciseEndMatch.index! + '<!-- EXERCISE_END -->'.length;

    // Extract main content (everything before exercises)
    mainContent = markdown.substring(0, startIndex).trim();

    // Extract and parse exercises YAML
    const exerciseSection = markdown.substring(startIndex, endIndex);
    exercises = parseExercisesYaml(exerciseSection, topicName);
  }

  // Convert markdown to HTML
  const htmlContent = marked(mainContent);

  return {
    content: htmlContent as string,
    exercises,
  };
}

/**
 * Parse exercises from YAML section
 */
function parseExercisesYaml(section: string, topicName: string): Exercise[] {
  try {
    // Extract YAML content between ```yaml and ```
    const yamlMatch = section.match(/```yaml\s*([\s\S]*?)\s*```/);

    if (!yamlMatch) {
      return getDefaultExercises(topicName);
    }

    const yamlContent = yamlMatch[1];
    const parsed = yaml.load(yamlContent) as { exercises: Exercise[] };

    if (!parsed?.exercises || !Array.isArray(parsed.exercises)) {
      return getDefaultExercises(topicName);
    }

    // Add IDs and normalize
    return parsed.exercises.map((ex, index) => ({
      ...ex,
      id: `ex-${index + 1}`,
      starter_code: ex.starter_code?.trim() || '# Write your code here\n',
      expected_output: ex.expected_output?.trim() || '',
      hints: ex.hints || [],
      difficulty: ex.difficulty || 'basic',
    }));
  } catch (error) {
    console.error('Error parsing exercises YAML:', error);
    return getDefaultExercises(topicName);
  }
}

/**
 * Get default content when file doesn't exist
 */
function getDefaultContent(topicName: string): TopicContent {
  return {
    content: `
      <h2>${topicName}</h2>
      <p>Welcome to the ${topicName} lesson.</p>
      <p>This topic is coming soon! In the meantime, try the practice exercises below.</p>
      <h3>What You'll Learn</h3>
      <ul>
        <li>Core concepts of ${topicName.toLowerCase()}</li>
        <li>Common patterns and best practices</li>
        <li>Real-world applications</li>
      </ul>
    `,
    exercises: getDefaultExercises(topicName),
  };
}

/**
 * Generate default exercises for a topic
 */
function getDefaultExercises(topicName: string): Exercise[] {
  return [
    {
      id: 'ex-1',
      title: `${topicName} Basics 1`,
      difficulty: 'basic',
      description: `Practice basic ${topicName.toLowerCase()} concepts. Write code that demonstrates your understanding.`,
      starter_code: '# Write your solution here\n\n',
      expected_output: '',
      hints: ['Start with simple examples from the lesson'],
    },
    {
      id: 'ex-2',
      title: `${topicName} Basics 2`,
      difficulty: 'basic',
      description: `Continue practicing ${topicName.toLowerCase()} fundamentals.`,
      starter_code: '# Write your solution here\n\n',
      expected_output: '',
      hints: ['Build on what you learned in the previous exercise'],
    },
    {
      id: 'ex-3',
      title: `${topicName} Application`,
      difficulty: 'intermediate',
      description: `Apply ${topicName.toLowerCase()} in a practical scenario.`,
      starter_code: '# Write your solution here\n\n',
      expected_output: '',
      hints: ['Think about how this concept is used in real programs'],
    },
    {
      id: 'ex-4',
      title: `${topicName} Problem Solving`,
      difficulty: 'intermediate',
      description: `Solve a problem using ${topicName.toLowerCase()} techniques.`,
      starter_code: '# Write your solution here\n\n',
      expected_output: '',
      hints: ['Break the problem into smaller steps'],
    },
    {
      id: 'ex-5',
      title: `${topicName} Challenge`,
      difficulty: 'advanced',
      description: `Challenge yourself with this advanced ${topicName.toLowerCase()} exercise.`,
      starter_code: '# Write your solution here\n\n',
      expected_output: '',
      hints: ['Consider edge cases and optimization'],
    },
    {
      id: 'ex-6',
      title: `${topicName} Master`,
      difficulty: 'advanced',
      description: `Master ${topicName.toLowerCase()} with this final challenge.`,
      starter_code: '# Write your solution here\n\n',
      expected_output: '',
      hints: ['Combine multiple concepts you have learned'],
    },
  ];
}

/**
 * Get list of all available topics with content
 */
export function getAvailableTopics(): string[] {
  return Object.keys(TOPIC_FILE_MAP).filter(topicName => {
    const filePath = path.join(CONTENT_DIR, TOPIC_FILE_MAP[topicName]);
    return fs.existsSync(filePath);
  });
}

/**
 * Check if content file exists for a topic
 */
export function hasContent(topicName: string): boolean {
  const filePath = TOPIC_FILE_MAP[topicName];
  if (!filePath) return false;

  const fullPath = path.join(CONTENT_DIR, filePath);
  return fs.existsSync(fullPath);
}
