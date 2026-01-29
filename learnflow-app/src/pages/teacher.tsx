import { useState } from 'react';
import Layout from '@/components/Layout';
import TeacherStudentRow from '@/components/TeacherStudentRow';
import MasteryBadge from '@/components/MasteryBadge';
import { GraduationCap, AlertTriangle, Users, TrendingDown, Plus, Loader2 } from 'lucide-react';
import { useRequireAuth } from '@/components/withAuth';

// Demo data - in production, fetched from progress-agent + DB
const CLASS_DATA = {
  name: 'Python 101 - Fall 2026',
  students: [
    { student_id: '1', name: 'Alice Chen', overall_mastery: 82, struggling_topics: [] },
    { student_id: '2', name: 'Bob Martinez', overall_mastery: 55, struggling_topics: ['Functions', 'OOP'] },
    { student_id: '3', name: 'Carol Kim', overall_mastery: 91, struggling_topics: [] },
    { student_id: '4', name: 'David Patel', overall_mastery: 28, struggling_topics: ['Control Flow', 'Lists', 'Functions'] },
    { student_id: '5', name: 'Eva Johnson', overall_mastery: 45, struggling_topics: ['Data Structures'] },
    { student_id: '6', name: 'Frank Lee', overall_mastery: 67, struggling_topics: [] },
    { student_id: '7', name: 'Grace Wang', overall_mastery: 73, struggling_topics: [] },
    { student_id: '8', name: 'Henry Brown', overall_mastery: 35, struggling_topics: ['Basics', 'Control Flow'] },
  ],
};

const MODULE_STATS = [
  { name: 'Basics', avgMastery: 72, struggling: 1 },
  { name: 'Control Flow', avgMastery: 58, struggling: 2 },
  { name: 'Data Structures', avgMastery: 45, struggling: 1 },
  { name: 'Functions', avgMastery: 38, struggling: 2 },
  { name: 'OOP', avgMastery: 25, struggling: 1 },
  { name: 'Files', avgMastery: 12, struggling: 0 },
  { name: 'Errors', avgMastery: 8, struggling: 0 },
  { name: 'Libraries', avgMastery: 5, struggling: 0 },
];

export default function TeacherDashboard() {
  // Require teacher role - redirects to dashboard if not a teacher
  const { user, isReady } = useRequireAuth({ requiredRole: 'teacher' });

  const [tab, setTab] = useState<'overview' | 'students' | 'struggles' | 'create'>('overview');
  const [newExercise, setNewExercise] = useState({ title: '', description: '', topic: 'basics', difficulty: 'medium', starterCode: '' });

  const classMastery = Math.round(CLASS_DATA.students.reduce((s, st) => s + st.overall_mastery, 0) / CLASS_DATA.students.length);
  const strugglingStudents = CLASS_DATA.students.filter((s) => s.struggling_topics.length > 0);

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
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <GraduationCap className="text-blue-400" />
            Teacher Dashboard
          </h1>
          <p className="text-slate-400 mt-1">{CLASS_DATA.name}</p>
        </div>

        {/* Summary cards */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-4">
            <div className="flex items-center gap-2 text-slate-400 text-xs mb-1"><Users size={14} /> Students</div>
            <p className="text-2xl font-bold text-white">{CLASS_DATA.students.length}</p>
          </div>
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-4">
            <div className="flex items-center gap-2 text-slate-400 text-xs mb-1"><TrendingDown size={14} /> Class Mastery</div>
            <p className="text-2xl font-bold text-white">{classMastery}%</p>
          </div>
          <div className="bg-slate-800 border border-red-800 rounded-xl p-4">
            <div className="flex items-center gap-2 text-red-400 text-xs mb-1"><AlertTriangle size={14} /> Struggling</div>
            <p className="text-2xl font-bold text-red-400">{strugglingStudents.length}</p>
          </div>
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-4">
            <div className="flex items-center gap-2 text-slate-400 text-xs mb-1"><GraduationCap size={14} /> Mastered</div>
            <p className="text-2xl font-bold text-green-400">{CLASS_DATA.students.filter(s => s.overall_mastery >= 91).length}</p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 mb-6 bg-slate-800 rounded-lg p-1 w-fit">
          {(['overview', 'students', 'struggles', 'create'] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition ${tab === t ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'}`}>
              {t === 'create' ? 'Create Exercise' : t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {/* Tab content */}
        {tab === 'overview' && (
          <div>
            <h2 className="text-lg font-semibold text-white mb-4">Module Performance</h2>
            <div className="grid grid-cols-4 gap-4">
              {MODULE_STATS.map((mod) => (
                <div key={mod.name} className="bg-slate-800 border border-slate-700 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-medium text-white text-sm">{mod.name}</h3>
                    {mod.struggling > 0 && (
                      <span className="text-xs text-red-400">{mod.struggling} struggling</span>
                    )}
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="flex-1 h-2 bg-slate-700 rounded-full">
                      <div
                        className={`h-full rounded-full ${
                          mod.avgMastery >= 71 ? 'bg-green-500' :
                          mod.avgMastery >= 41 ? 'bg-yellow-500' : 'bg-red-500'
                        }`}
                        style={{ width: `${mod.avgMastery}%` }}
                      />
                    </div>
                    <span className="text-sm font-bold text-slate-300 w-10 text-right">{mod.avgMastery}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {tab === 'students' && (
          <div className="space-y-2">
            <h2 className="text-lg font-semibold text-white mb-4">All Students</h2>
            {CLASS_DATA.students
              .sort((a, b) => a.overall_mastery - b.overall_mastery)
              .map((student) => (
                <TeacherStudentRow key={student.student_id} student={student} />
              ))}
          </div>
        )}

        {tab === 'struggles' && (
          <div>
            <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <AlertTriangle className="text-red-400" /> Students Needing Help
            </h2>
            {strugglingStudents.length === 0 ? (
              <p className="text-slate-400">No students are currently struggling.</p>
            ) : (
              <div className="space-y-4">
                {strugglingStudents.map((student) => (
                  <div key={student.student_id} className="bg-red-900/10 border border-red-800 rounded-xl p-5">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-slate-600 rounded-full flex items-center justify-center font-bold text-white">
                          {student.name.charAt(0)}
                        </div>
                        <div>
                          <h3 className="font-semibold text-white">{student.name}</h3>
                          <p className="text-xs text-slate-400">Mastery: {student.overall_mastery}%</p>
                        </div>
                      </div>
                      <MasteryBadge mastery={student.overall_mastery} size="sm" />
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {student.struggling_topics.map((topic) => (
                        <span key={topic} className="px-3 py-1 bg-red-900/30 border border-red-700 rounded-full text-xs text-red-300">
                          {topic}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {tab === 'create' && (
          <div className="max-w-2xl">
            <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Plus className="text-green-400" /> Create New Exercise
            </h2>
            <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 space-y-4">
              <div>
                <label className="block text-sm text-slate-400 mb-1">Title</label>
                <input
                  type="text" value={newExercise.title}
                  onChange={(e) => setNewExercise(p => ({ ...p, title: e.target.value }))}
                  className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:border-blue-500"
                  placeholder="e.g., Build a Calculator"
                />
              </div>
              <div>
                <label className="block text-sm text-slate-400 mb-1">Description</label>
                <textarea
                  value={newExercise.description}
                  onChange={(e) => setNewExercise(p => ({ ...p, description: e.target.value }))}
                  className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:outline-none focus:border-blue-500 h-24 resize-none"
                  placeholder="Describe what the student needs to do..."
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm text-slate-400 mb-1">Topic</label>
                  <select
                    value={newExercise.topic}
                    onChange={(e) => setNewExercise(p => ({ ...p, topic: e.target.value }))}
                    className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm"
                  >
                    <option value="basics">Basics</option>
                    <option value="control-flow">Control Flow</option>
                    <option value="data-structures">Data Structures</option>
                    <option value="functions">Functions</option>
                    <option value="oop">OOP</option>
                    <option value="files">Files</option>
                    <option value="errors">Errors</option>
                    <option value="libraries">Libraries</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm text-slate-400 mb-1">Difficulty</label>
                  <select
                    value={newExercise.difficulty}
                    onChange={(e) => setNewExercise(p => ({ ...p, difficulty: e.target.value }))}
                    className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm"
                  >
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm text-slate-400 mb-1">Starter Code</label>
                <textarea
                  value={newExercise.starterCode}
                  onChange={(e) => setNewExercise(p => ({ ...p, starterCode: e.target.value }))}
                  className="w-full px-4 py-2 bg-slate-900 border border-slate-600 rounded-lg text-green-300 text-sm font-mono focus:outline-none focus:border-blue-500 h-32 resize-none"
                  placeholder="# Starter code for students"
                />
              </div>
              <button className="px-6 py-2.5 bg-green-600 text-white rounded-lg hover:bg-green-500 transition font-medium">
                Create Exercise
              </button>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}
