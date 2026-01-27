import { useState } from 'react';
import Layout from '@/components/Layout';
import CodeEditor from '@/components/CodeEditor';
import ChatPanel from '@/components/ChatPanel';

const DEMO_STUDENT_ID = '00000000-0000-0000-0000-000000000001';
const DEMO_TOPIC_ID = '00000000-0000-0000-0000-000000000010';

export default function EditorPage() {
  const [lastCode, setLastCode] = useState('');
  const [executionCount, setExecutionCount] = useState(0);

  return (
    <Layout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-white">Python Code Editor</h1>
          <p className="text-slate-400 mt-1">Write, run, and get feedback on your Python code</p>
        </div>

        <div className="grid grid-cols-3 gap-4 h-[calc(100vh-180px)]">
          {/* Editor - 2 cols */}
          <div className="col-span-2">
            <CodeEditor
              studentId={DEMO_STUDENT_ID}
              topicId={DEMO_TOPIC_ID}
              onExecutionResult={(result) => {
                setExecutionCount((c) => c + 1);
              }}
            />
          </div>

          {/* Chat - 1 col */}
          <div className="col-span-1">
            <ChatPanel
              studentId={DEMO_STUDENT_ID}
              topicId={DEMO_TOPIC_ID}
              code={lastCode}
            />
          </div>
        </div>
      </div>
    </Layout>
  );
}
