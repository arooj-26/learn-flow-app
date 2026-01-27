import Link from 'next/link';
import { useRouter } from 'next/router';
import { BookOpen, Code, MessageSquare, ClipboardList, BarChart3, GraduationCap } from 'lucide-react';
import { ReactNode } from 'react';

const NAV_ITEMS = [
  { href: '/dashboard', label: 'Dashboard', icon: BarChart3 },
  { href: '/editor', label: 'Code Editor', icon: Code },
  { href: '/chat', label: 'Chat Tutor', icon: MessageSquare },
  { href: '/quizzes', label: 'Quizzes', icon: ClipboardList },
  { href: '/exercises', label: 'Exercises', icon: BookOpen },
];

const TEACHER_NAV = [
  { href: '/teacher', label: 'Teacher Dashboard', icon: GraduationCap },
];

interface LayoutProps {
  children: ReactNode;
  role?: 'student' | 'teacher';
}

export default function Layout({ children, role = 'student' }: LayoutProps) {
  const router = useRouter();
  const navItems = role === 'teacher' ? [...NAV_ITEMS, ...TEACHER_NAV] : NAV_ITEMS;

  return (
    <div className="flex h-screen bg-slate-900">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-800 border-r border-slate-700 flex flex-col">
        <div className="p-6 border-b border-slate-700">
          <h1 className="text-xl font-bold text-blue-400 flex items-center gap-2">
            <GraduationCap size={24} />
            LearnFlow
          </h1>
          <p className="text-xs text-slate-400 mt-1">Python Learning Platform</p>
        </div>

        <nav className="flex-1 p-4 space-y-1">
          {navItems.map(({ href, label, icon: Icon }) => {
            const active = router.pathname === href;
            return (
              <Link
                key={href}
                href={href}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                  active
                    ? 'bg-blue-600 text-white'
                    : 'text-slate-300 hover:bg-slate-700 hover:text-white'
                }`}
              >
                <Icon size={18} />
                {label}
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-slate-700">
          <div className="text-xs text-slate-500">
            Role: <span className="text-slate-300 capitalize">{role}</span>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <div className="p-6">{children}</div>
      </main>
    </div>
  );
}
