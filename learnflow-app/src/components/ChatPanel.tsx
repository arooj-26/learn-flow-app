import { useState, useRef, useEffect, useCallback } from 'react';
import { Send, Bot, User as UserIcon, Loader2, Sparkles, RefreshCw, Trash2 } from 'lucide-react';
import { useSession } from '@/lib/auth-client';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  agent?: string;
  timestamp: Date;
  isStreaming?: boolean;
}

interface ChatPanelProps {
  topicId?: string;
  code?: string;
}

export default function ChatPanel({ topicId, code }: ChatPanelProps) {
  const { data: session } = useSession();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '0',
      role: 'assistant',
      content: "Hi! I'm your AI Python tutor powered by advanced language models. I can help you with:\n\n- **Learning Python concepts** from basics to advanced\n- **Debugging your code** and explaining errors\n- **Code reviews** and best practices\n- **Practice exercises** tailored to your level\n\nI also search the web for the latest Python information when needed. What would you like to learn today?",
      agent: 'python-tutor',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [hasAI, setHasAI] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Get conversation history for context
  const getConversationHistory = useCallback(() => {
    return messages
      .filter((m) => m.id !== '0') // Exclude initial greeting
      .slice(-10) // Keep last 10 messages for context
      .map((m) => ({
        role: m.role,
        content: m.content,
      }));
  }, [messages]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || isLoading) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    // Add placeholder for streaming
    const assistantMsgId = (Date.now() + 1).toString();
    setMessages((prev) => [
      ...prev,
      {
        id: assistantMsgId,
        role: 'assistant',
        content: '',
        agent: 'python-tutor',
        timestamp: new Date(),
        isStreaming: true,
      },
    ]);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          message: text,
          topicId,
          code,
          conversationHistory: getConversationHistory(),
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const result = await response.json();
      const fullResponse = result.response?.explanation || result.response || "I couldn't generate a response.";
      setHasAI(result.hasAI || false);

      // Simulate streaming effect
      await simulateStreaming(assistantMsgId, fullResponse, result.agent || 'python-tutor');
    } catch (error) {
      console.error('Chat error:', error);
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantMsgId
            ? {
                ...msg,
                content: 'Sorry, I had trouble connecting. Please try again.',
                agent: 'error',
                isStreaming: false,
              }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  // Simulate streaming text effect
  const simulateStreaming = async (msgId: string, fullText: string, agent: string) => {
    const words = fullText.split(' ');
    let currentText = '';

    for (let i = 0; i < words.length; i++) {
      currentText += (i === 0 ? '' : ' ') + words[i];

      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === msgId
            ? { ...msg, content: currentText, agent, isStreaming: i < words.length - 1 }
            : msg
        )
      );

      // Small delay for streaming effect (faster for code blocks)
      if (words[i].includes('```')) {
        await new Promise((r) => setTimeout(r, 5));
      } else {
        await new Promise((r) => setTimeout(r, 15));
      }
    }

    // Mark as complete
    setMessages((prev) =>
      prev.map((msg) =>
        msg.id === msgId ? { ...msg, isStreaming: false } : msg
      )
    );
  };

  const handleClearChat = () => {
    setMessages([
      {
        id: '0',
        role: 'assistant',
        content: "Chat cleared! I'm ready to help you learn Python. What would you like to know?",
        agent: 'python-tutor',
        timestamp: new Date(),
      },
    ]);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const agentLabel = (agent?: string) => {
    const labels: Record<string, string> = {
      'concepts-agent': 'Concepts',
      'debug-agent': 'Debug',
      'code-review-agent': 'Review',
      'python-tutor': 'AI Tutor',
      'triage-agent': 'Tutor',
      'error': 'Error',
    };
    return agent ? labels[agent] || 'AI Tutor' : 'AI Tutor';
  };

  // Render markdown-like content with code blocks
  const renderContent = (content: string) => {
    const parts = content.split(/(```[\s\S]*?```)/g);

    return parts.map((part, index) => {
      if (part.startsWith('```')) {
        const lines = part.split('\n');
        const language = lines[0].replace('```', '').trim();
        const code = lines.slice(1, -1).join('\n');

        return (
          <pre key={index} className="bg-slate-900 rounded-lg p-3 my-2 overflow-x-auto border border-slate-700">
            {language && (
              <div className="text-xs text-slate-500 mb-2 font-mono">{language}</div>
            )}
            <code className="text-sm text-green-400 font-mono whitespace-pre">{code}</code>
          </pre>
        );
      }

      // Regular text with formatting
      return (
        <span key={index} className="whitespace-pre-wrap">
          {part.split(/(\*\*.*?\*\*|\`[^`]+\`)/g).map((segment, i) => {
            if (segment.startsWith('**') && segment.endsWith('**')) {
              return (
                <strong key={i} className="text-white font-semibold">
                  {segment.slice(2, -2)}
                </strong>
              );
            }
            if (segment.startsWith('`') && segment.endsWith('`')) {
              return (
                <code key={i} className="bg-slate-700 px-1.5 py-0.5 rounded text-blue-300 text-sm font-mono">
                  {segment.slice(1, -1)}
                </code>
              );
            }
            // Handle bullet points
            return segment.split('\n').map((line, j) => {
              if (line.trim().startsWith('- ')) {
                return (
                  <span key={`${i}-${j}`}>
                    {j > 0 && '\n'}
                    <span className="text-blue-400">{'  \u2022 '}</span>
                    {line.trim().slice(2)}
                  </span>
                );
              }
              return j > 0 ? '\n' + line : line;
            });
          })}
        </span>
      );
    });
  };

  return (
    <div className="flex flex-col h-full bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-slate-700 bg-gradient-to-r from-slate-800 to-slate-750 flex items-center justify-between">
        <h2 className="text-sm font-semibold text-white flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
            <Sparkles size={16} className="text-white" />
          </div>
          <div>
            <span>AI Python Tutor</span>
            {hasAI && (
              <span className="ml-2 text-xs bg-green-500/20 text-green-400 px-2 py-0.5 rounded-full">
                AI Powered
              </span>
            )}
          </div>
        </h2>
        <div className="flex items-center gap-2">
          {session?.user && (
            <span className="text-xs text-slate-400">
              {session.user.name}
            </span>
          )}
          <button
            onClick={handleClearChat}
            className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-700 rounded-lg transition"
            title="Clear chat"
          >
            <Trash2 size={14} />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-3 animate-slide-up ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
          >
            <div
              className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                msg.role === 'user'
                  ? 'bg-blue-600'
                  : 'bg-gradient-to-br from-purple-500 to-blue-600'
              }`}
            >
              {msg.role === 'user' ? <UserIcon size={14} /> : <Bot size={14} />}
            </div>
            <div className={`max-w-[85%] ${msg.role === 'user' ? 'text-right' : ''}`}>
              {msg.role === 'assistant' && msg.agent && (
                <span className="text-[10px] text-slate-500 font-medium uppercase tracking-wide flex items-center gap-1">
                  {agentLabel(msg.agent)}
                  {msg.isStreaming && (
                    <span className="inline-block w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse" />
                  )}
                </span>
              )}
              <div
                className={`mt-1 px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white rounded-tr-sm'
                    : 'bg-slate-700 text-slate-200 rounded-tl-sm'
                }`}
              >
                <div>{renderContent(msg.content)}</div>
                {msg.isStreaming && (
                  <span className="inline-block w-2 h-4 bg-blue-400 ml-1 animate-pulse" />
                )}
              </div>
              <span className="text-[10px] text-slate-600 mt-1 block">
                {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
          </div>
        ))}
        {isLoading && messages[messages.length - 1]?.content === '' && (
          <div className="flex gap-3 animate-slide-up">
            <div className="w-8 h-8 rounded-full flex items-center justify-center bg-gradient-to-br from-purple-500 to-blue-600">
              <Bot size={14} />
            </div>
            <div className="px-4 py-3 bg-slate-700 rounded-2xl rounded-tl-sm flex items-center gap-2">
              <Loader2 size={16} className="animate-spin text-blue-400" />
              <span className="text-sm text-slate-400">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Questions */}
      {messages.length <= 1 && (
        <div className="px-4 pb-2">
          <div className="flex flex-wrap gap-2">
            {[
              'How do I use for loops?',
              'Explain list comprehensions',
              'What are decorators?',
              'Help me debug my code',
            ].map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => {
                  setInput(suggestion);
                  inputRef.current?.focus();
                }}
                className="text-xs px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded-full transition"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="p-3 border-t border-slate-700 bg-slate-800/50">
        <div className="flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything about Python..."
            className="flex-1 px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-xl text-sm text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="px-4 py-2.5 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-500 hover:to-purple-500 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {isLoading ? (
              <Loader2 size={16} className="animate-spin" />
            ) : (
              <Send size={16} />
            )}
          </button>
        </div>
        <p className="text-[10px] text-slate-500 mt-2 text-center">
          AI responses are for learning purposes. Always verify code before production use.
        </p>
      </div>
    </div>
  );
}
