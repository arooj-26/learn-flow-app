import Layout from '@/components/Layout';
import ChatPanel from '@/components/ChatPanel';

const DEMO_STUDENT_ID = '00000000-0000-0000-0000-000000000001';

export default function ChatPage() {
  return (
    <Layout>
      <div className="max-w-3xl mx-auto h-[calc(100vh-120px)]">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-white">Chat with Python Tutor</h1>
          <p className="text-slate-400 mt-1">
            Ask about concepts, get debugging help, or request code reviews
          </p>
        </div>
        <div className="h-[calc(100%-80px)]">
          <ChatPanel studentId={DEMO_STUDENT_ID} />
        </div>
      </div>
    </Layout>
  );
}
