import Link from 'next/link';
import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';
import {
  BookOpen, Code, MessageSquare, ClipboardList, BarChart3, GraduationCap,
  LogOut, User, ChevronDown, ChevronRight, Target
} from 'lucide-react';
import { ReactNode } from 'react';
import { useAuth } from '@/contexts/AuthContext';

interface Module {
  id: string;
  name: string;
}

const NAV_ITEMS = [
  { href: '/dashboard', label: 'Dashboard', icon: BarChart3 },
  { href: '/editor', label: 'Code Editor', icon: Code },
  { href: '/chat', label: 'Chat Tutor', icon: MessageSquare },
  { href: '/exercises', label: 'Exercises', icon: BookOpen },
];

const TEACHER_NAV = [
  { href: '/teacher', label: 'Teacher Dashboard', icon: GraduationCap },
];

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const router = useRouter();
  const { user, isLoading, signOut } = useAuth();
  const [quizExpanded, setQuizExpanded] = useState(false);
  const [modules, setModules] = useState<Module[]>([]);
  const [userRole, setUserRole] = useState<'student' | 'teacher'>('student');

  // Fetch user role from our users table
  useEffect(() => {
    if (user) {
      fetchUserRole();
      fetchModules();
    }
  }, [user]);

  const fetchUserRole = async () => {
    try {
      const response = await fetch('/api/user/me', { credentials: 'include' });
      if (response.ok) {
        const data = await response.json();
        setUserRole(data.role || 'student');
      }
    } catch (error) {
      console.error('Failed to fetch user role:', error);
    }
  };

  const navItems = userRole === 'teacher' ? [...NAV_ITEMS, ...TEACHER_NAV] : NAV_ITEMS;

  const fetchModules = async () => {
    try {
      const response = await fetch('/api/modules', {
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setModules(data.modules || []);
      }
    } catch (error) {
      console.error('Failed to fetch modules:', error);
    }
  };

  const handleSignOut = async () => {
    await signOut();
  };

  const isQuizActive = router.pathname.startsWith('/quizzes');

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

        <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
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

          {/* Quizzes Section with expandable modules */}
          <div className="pt-2">
            <button
              onClick={() => setQuizExpanded(!quizExpanded)}
              className={`w-full flex items-center justify-between gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                isQuizActive
                  ? 'bg-purple-600 text-white'
                  : 'text-slate-300 hover:bg-slate-700 hover:text-white'
              }`}
            >
              <div className="flex items-center gap-3">
                <Target size={18} />
                Quizzes
              </div>
              {quizExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            </button>

            {/* Expandable module list */}
            {quizExpanded && (
              <div className="mt-1 ml-4 space-y-0.5">
                <Link
                  href="/quizzes"
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs transition-colors ${
                    router.pathname === '/quizzes' && !router.query.moduleId
                      ? 'bg-purple-500/30 text-purple-300'
                      : 'text-slate-400 hover:bg-slate-700 hover:text-white'
                  }`}
                >
                  <ClipboardList size={14} />
                  All Quizzes
                </Link>
                {modules.map((mod) => (
                  <Link
                    key={mod.id}
                    href={`/quizzes?moduleId=${mod.id}`}
                    className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs transition-colors ${
                      router.query.moduleId === mod.id
                        ? 'bg-purple-500/30 text-purple-300'
                        : 'text-slate-400 hover:bg-slate-700 hover:text-white'
                    }`}
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-slate-500" />
                    {mod.name}
                  </Link>
                ))}
              </div>
            )}
          </div>
        </nav>

        {/* User info and logout */}
        <div className="p-4 border-t border-slate-700">
          {isLoading ? (
            <div className="animate-pulse">
              <div className="h-4 bg-slate-700 rounded w-24 mb-2"></div>
              <div className="h-3 bg-slate-700 rounded w-16"></div>
            </div>
          ) : user ? (
            <div className="space-y-3">
              {/* User info */}
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-slate-600 flex items-center justify-center">
                  {user.image ? (
                    <img
                      src={user.image}
                      alt={user.name}
                      className="w-8 h-8 rounded-full object-cover"
                    />
                  ) : (
                    <User size={16} className="text-slate-300" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-white truncate">{user.name}</p>
                  <p className="text-xs text-slate-400 truncate">{user.email}</p>
                </div>
              </div>

              {/* Role badge */}
              <div className="flex items-center justify-between">
                <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                  userRole === 'teacher'
                    ? 'bg-purple-900/30 text-purple-300 border border-purple-700'
                    : 'bg-blue-900/30 text-blue-300 border border-blue-700'
                }`}>
                  {userRole === 'teacher' ? 'Teacher' : 'Student'}
                </span>

                {/* Logout button */}
                <button
                  onClick={handleSignOut}
                  className="flex items-center gap-1 px-2 py-1 text-xs text-slate-400 hover:text-white hover:bg-slate-700 rounded transition"
                >
                  <LogOut size={14} />
                  Logout
                </button>
              </div>
            </div>
          ) : (
            <Link
              href="/login"
              className="flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-500 transition"
            >
              Sign In
            </Link>
          )}
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <div className="p-6">{children}</div>
      </main>
    </div>
  );
}
