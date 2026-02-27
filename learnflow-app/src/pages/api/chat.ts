/**
 * AI-Powered Python Tutor Chat API
 * Features:
 * - Real-time streaming responses
 * - Web search for up-to-date information
 * - Conversation context maintenance
 * - Python-focused tutoring
 */
import type { NextApiRequest, NextApiResponse } from 'next';
import { auth } from '@/lib/auth';
import OpenAI from 'openai';

// Initialize OpenAI client (will be null if no API key)
const openai = process.env.OPENAI_API_KEY
  ? new OpenAI({ apiKey: process.env.OPENAI_API_KEY })
  : null;

// System prompt for the Python tutor
const PYTHON_TUTOR_SYSTEM_PROMPT = `You are an expert Python tutor for the LearnFlow learning platform. Your role is to help students learn Python programming effectively.

## Your Teaching Style:
- Be patient, encouraging, and supportive
- Explain concepts clearly with practical examples
- Use code examples with proper syntax highlighting (use \`\`\`python code blocks)
- Break down complex topics into digestible parts
- Ask clarifying questions when needed
- Provide hints rather than direct answers when appropriate
- Celebrate progress and correct mistakes gently

## Your Capabilities:
- Explain Python concepts from basics to advanced
- Help debug code and explain errors
- Review code and suggest improvements
- Provide practice exercises
- Answer questions about Python libraries and best practices
- Help with algorithms and data structures

## Response Format:
- Use markdown formatting for clarity
- Include code examples when helpful
- Use bullet points for lists
- Bold important terms
- Keep responses focused but comprehensive

## Important Guidelines:
- Stay focused on Python and programming topics
- If asked about non-Python topics, gently redirect to Python learning
- Always encourage students to try coding themselves
- Provide multiple approaches when relevant
- Reference official Python documentation concepts when applicable

Remember: Your goal is to help students become confident Python programmers!`;

// Web search function using DuckDuckGo
async function searchWeb(query: string): Promise<string> {
  try {
    const searchQuery = encodeURIComponent(`Python ${query}`);
    const response = await fetch(
      `https://api.duckduckgo.com/?q=${searchQuery}&format=json&no_html=1&skip_disambig=1`
    );

    if (!response.ok) {
      return '';
    }

    const data = await response.json();

    let searchResults = '';

    // Get abstract if available
    if (data.Abstract) {
      searchResults += `**Reference:** ${data.Abstract}\n`;
      if (data.AbstractURL) {
        searchResults += `Source: ${data.AbstractURL}\n`;
      }
    }

    // Get related topics
    if (data.RelatedTopics && data.RelatedTopics.length > 0) {
      const topics = data.RelatedTopics
        .filter((t: any) => t.Text)
        .slice(0, 3)
        .map((t: any) => t.Text)
        .join('\n');
      if (topics) {
        searchResults += `\n**Related Information:**\n${topics}`;
      }
    }

    return searchResults;
  } catch (error) {
    console.error('Web search error:', error);
    return '';
  }
}

// Fallback knowledge base for when no AI API is available
const PYTHON_KNOWLEDGE: Record<string, string> = {
  'variable': `**Variables in Python**

Variables are containers for storing data values. In Python, you create a variable by assigning a value:

\`\`\`python
name = "Alice"    # String
age = 25          # Integer
price = 19.99     # Float
is_valid = True   # Boolean
\`\`\`

Key points:
- No need to declare types (Python is dynamically typed)
- Variable names are case-sensitive
- Use descriptive names (snake_case is preferred)`,

  'loop': `**Loops in Python**

Python has two main loop types:

**For Loop** - iterate over sequences:
\`\`\`python
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Using range
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4
\`\`\`

**While Loop** - repeat while condition is True:
\`\`\`python
count = 0
while count < 5:
    print(count)
    count += 1
\`\`\``,

  'function': `**Functions in Python**

Functions are reusable blocks of code:

\`\`\`python
# Basic function
def greet(name):
    return f"Hello, {name}!"

result = greet("Alice")  # "Hello, Alice!"

# Default parameters
def greet(name="World"):
    return f"Hello, {name}!"

# Multiple return values
def min_max(numbers):
    return min(numbers), max(numbers)

minimum, maximum = min_max([1, 5, 3])
\`\`\``,

  'list': `**Lists in Python**

Lists are ordered, mutable collections:

\`\`\`python
# Create
fruits = ["apple", "banana", "cherry"]

# Access
first = fruits[0]      # "apple"
last = fruits[-1]      # "cherry"

# Modify
fruits.append("date")  # Add to end
fruits.insert(0, "avocado")  # Insert at index
fruits.remove("banana")  # Remove by value
fruits.pop()           # Remove last

# Useful methods
len(fruits)            # Length
fruits.sort()          # Sort in place
\`\`\``,

  'class': `**Classes in Python (OOP)**

Classes define objects with attributes and methods:

\`\`\`python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hi, I'm {self.name}"

    def birthday(self):
        self.age += 1

# Usage
alice = Person("Alice", 25)
print(alice.greet())  # "Hi, I'm Alice"
\`\`\``,

  'error': `**Error Handling in Python**

Handle errors with try/except:

\`\`\`python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"Error: {e}")
finally:
    print("This always runs")

# Raising exceptions
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
\`\`\``,
};

// Generate response using AI or fallback
async function generateAIResponse(
  message: string,
  conversationHistory: Array<{ role: string; content: string }>
): Promise<{ response: string; source: string }> {
  // Try AI response first
  if (openai) {
    try {
      // Check if we should search the web for this query
      const shouldSearch = message.toLowerCase().includes('latest') ||
        message.toLowerCase().includes('new') ||
        message.toLowerCase().includes('2024') ||
        message.toLowerCase().includes('2025') ||
        message.toLowerCase().includes('update') ||
        message.toLowerCase().includes('current');

      let webContext = '';
      if (shouldSearch) {
        webContext = await searchWeb(message);
      }

      const messages: OpenAI.Chat.ChatCompletionMessageParam[] = [
        { role: 'system', content: PYTHON_TUTOR_SYSTEM_PROMPT },
        ...conversationHistory.map(msg => ({
          role: msg.role as 'user' | 'assistant',
          content: msg.content,
        })),
      ];

      // Add web search context if available
      if (webContext) {
        messages.push({
          role: 'system',
          content: `Here's some current information from the web that may help answer the question:\n\n${webContext}\n\nUse this information if relevant, but focus on teaching Python concepts clearly.`,
        });
      }

      messages.push({ role: 'user', content: message });

      const completion = await openai.chat.completions.create({
        model: 'gpt-4o-mini',
        messages,
        max_tokens: 1500,
        temperature: 0.7,
      });

      const response = completion.choices[0]?.message?.content || 'I apologize, I couldn\'t generate a response. Could you try rephrasing your question?';

      return { response, source: 'ai' };
    } catch (error) {
      console.error('OpenAI API error:', error);
      // Fall through to knowledge base
    }
  }

  // Fallback to knowledge base
  const lowerMessage = message.toLowerCase();

  for (const [keyword, response] of Object.entries(PYTHON_KNOWLEDGE)) {
    if (lowerMessage.includes(keyword)) {
      return { response, source: 'knowledge-base' };
    }
  }

  // Default response
  return {
    response: `I'm your Python tutor! I can help you with:

- **Variables & Types** - How to store and work with data
- **Control Flow** - if statements, for/while loops
- **Data Structures** - lists, dictionaries, tuples, sets
- **Functions** - Creating reusable code
- **Classes & OOP** - Object-oriented programming
- **Error Handling** - try/except blocks

${!openai ? '\n> **Note:** For more intelligent responses, add your OpenAI API key to the environment variables.\n' : ''}

What would you like to learn about?`,
    source: 'default',
  };
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Verify authentication
    const session = await auth.api.getSession({
      headers: req.headers as any,
    });

    if (!session?.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const { message, conversationHistory = [] } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Generate AI response
    const { response, source } = await generateAIResponse(message, conversationHistory);

    return res.status(200).json({
      agent: 'python-tutor',
      response: {
        explanation: response,
      },
      source,
      hasAI: !!openai,
    });
  } catch (error) {
    console.error('Chat API error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
