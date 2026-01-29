import Layout from '@/components/Layout';
import ChatPanel from '@/components/ChatPanel';
import { useRequireAuth } from '@/components/withAuth';
import { Loader2 } from 'lucide-react';

export default function ChatPage() {
  const { user, isReady } = useRequireAuth();

  if (!isReady || !user) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <Loader2 className="animate-spin text-blue-400" size={32} />
      </div>
    );
  }

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
          <ChatPanel />
        </div>
      </div>
    </Layout>
  );
}
