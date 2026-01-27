import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2 } from 'lucide-react';
import { sendChatMessage } from '@/utils/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  agent?: string;
  timestamp: Date;
}

interface ChatPanelProps {
  studentId: string;
  topicId?: string;
  code?: string;
}

export default function ChatPanel({ studentId, topicId, code }: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '0',
      role: 'assistant',
      content: "Hi! I'm your Python tutor. Ask me anything about Python - how concepts work, help debugging errors, or code review. What would you like to learn?",
      agent: 'triage-agent',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
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

    try {
      const result = await sendChatMessage(studentId, text, topicId, code);
      const response = result.response;

      // Format response based on agent type
      let content = '';
      if (response.explanation) {
        content = response.explanation as string;
      } else if (response.error_explanation) {
        content = `**Error:** ${response.error_explanation}\n\n**Hint 1:** ${response.hint_1}\n\n**Hint 2:** ${response.hint_2}`;
      } else if (response.score !== undefined) {
        content = `**Code Score: ${response.score}/10**\n\n${(response.feedback as string[])?.join('\n') || ''}`;
      } else {
        content = JSON.stringify(response, null, 2);
      }

      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content,
          agent: result.agent,
          timestamp: new Date(),
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: 'Sorry, I had trouble connecting. Please try again.',
          agent: 'error',
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const agentLabel = (agent?: string) => {
    const labels: Record<string, string> = {
      'concepts-agent': 'Concepts',
      'debug-agent': 'Debug',
      'code-review-agent': 'Review',
      'triage-agent': 'Tutor',
    };
    return agent ? labels[agent] || agent : 'Tutor';
  };

  return (
    <div className="flex flex-col h-full bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
      <div className="px-4 py-3 border-b border-slate-700 bg-slate-750">
        <h2 className="text-sm font-semibold text-white flex items-center gap-2">
          <Bot size={16} className="text-blue-400" />
          Python Tutor Chat
        </h2>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-3 animate-slide-up ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
          >
            <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
              msg.role === 'user' ? 'bg-blue-600' : 'bg-slate-600'
            }`}>
              {msg.role === 'user' ? <User size={14} /> : <Bot size={14} />}
            </div>
            <div className={`max-w-[80%] ${msg.role === 'user' ? 'text-right' : ''}`}>
              {msg.role === 'assistant' && msg.agent && (
                <span className="text-[10px] text-slate-500 font-medium uppercase tracking-wide">
                  {agentLabel(msg.agent)}
                </span>
              )}
              <div className={`mt-1 px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white rounded-tr-sm'
                  : 'bg-slate-700 text-slate-200 rounded-tl-sm'
              }`}>
                <div className="whitespace-pre-wrap">{msg.content}</div>
              </div>
              <span className="text-[10px] text-slate-600 mt-1 block">
                {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex gap-3 animate-slide-up">
            <div className="w-8 h-8 rounded-full flex items-center justify-center bg-slate-600">
              <Bot size={14} />
            </div>
            <div className="px-4 py-3 bg-slate-700 rounded-2xl rounded-tl-sm">
              <Loader2 size={16} className="animate-spin text-blue-400" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-3 border-t border-slate-700">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleSend()}
            placeholder="Ask about Python concepts, debug help, or code review..."
            className="flex-1 px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-xl text-sm text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 transition"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="px-4 py-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-500 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}
