import { useEffect, useState } from 'react';
import { Sidebar, type PageId } from './components/layout/Sidebar';
import { Topbar } from './components/layout/Topbar';
import { AssistantPanel } from './components/AssistantPanel';
import { DashboardPage } from './pages/DashboardPage';
import { UploadPage } from './pages/UploadPage';
import { AdvisorPage } from './pages/AdvisorPage';
import { ForecastPage } from './pages/ForecastPage';
import { SettingsPage } from './pages/SettingsPage';

export default function App() {
  const [page, setPage] = useState<PageId>('dashboard');
  const [collapsed, setCollapsed] = useState(false);
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const [assistantOpen, setAssistantOpen] = useState(false);

  // Keyboard shortcut: Cmd/Ctrl + K opens assistant
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setAssistantOpen((o) => !o);
      }
    }
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  function handleNavigate(p: PageId) {
    setPage(p);
  }

  return (
    <div className="flex h-screen overflow-hidden bg-slate-50">
      <Sidebar
        active={page}
        onNavigate={handleNavigate}
        collapsed={collapsed}
        onToggleCollapse={() => setCollapsed((c) => !c)}
        mobileOpen={mobileNavOpen}
        onCloseMobile={() => setMobileNavOpen(false)}
      />

      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar
          page={page}
          onOpenMobileNav={() => setMobileNavOpen(true)}
          onOpenAssistant={() => setAssistantOpen(true)}
        />

        <main className="flex-1 overflow-y-auto px-4 py-6 md:px-6 lg:px-8">
          <div key={page} className="animate-fade-in mx-auto max-w-7xl">
            {page === 'dashboard' && <DashboardPage onNavigate={handleNavigate} />}
            {page === 'upload' && <UploadPage />}
            {page === 'advisor' && <AdvisorPage />}
            {page === 'forecast' && <ForecastPage />}
            {page === 'settings' && <SettingsPage />}
          </div>
        </main>
      </div>

      <AssistantPanel open={assistantOpen} onClose={() => setAssistantOpen(false)} />
    </div>
  );
}
