import { useState } from 'react';
import Layout from '@/components/Layout';
import CodeEditor from '@/components/CodeEditor';
import ChatPanel from '@/components/ChatPanel';
import { useRequireAuth } from '@/components/withAuth';
import { Loader2 } from 'lucide-react';

const DEMO_TOPIC_ID = '00000000-0000-0000-0000-000000000010';

export default function EditorPage() {
  const { user, isReady } = useRequireAuth();
  const [lastCode, setLastCode] = useState('');
  const [executionCount, setExecutionCount] = useState(0);

  if (!isReady || !user) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <Loader2 className="animate-spin text-blue-400" size={32} />
      </div>
    );
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-white">Python Code Editor</h1>
          <p className="text-slate-400 mt-1">Write, run, and get feedback on your Python code</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4" style={{ minHeight: 'calc(100vh - 200px)' }}>
          {/* Editor - full width on mobile, 2/3 on desktop */}
          <div className="lg:col-span-2 min-h-[360px]">
            <CodeEditor
              topicId={DEMO_TOPIC_ID}
              onExecutionResult={(result) => {
                setExecutionCount((c) => c + 1);
              }}
            />
          </div>

          {/* Chat - full width on mobile, 1/3 on desktop */}
          <div className="lg:col-span-1 min-h-[320px]">
            <ChatPanel
              topicId={DEMO_TOPIC_ID}
              code={lastCode}
            />
          </div>
        </div>
      </div>
    </Layout>
  );
}
