import { cn } from '../../lib/utils';
import { useAuth } from "../../auth/AuthContext";

export type PageId =
  | 'dashboard'
  | 'upload'
  | 'advisor'
  | 'forecast'
  | 'platform_management'
  | 'settings';

export interface NavItem {
  id: PageId;
  label: string;
  icon: React.ReactNode;
  badge?: string;
}

export const NAV_ITEMS: NavItem[] = [
  { id: 'dashboard', label: 'Dashboard', icon: <LayoutDashboardIcon /> },
  { id: 'upload', label: 'Upload Dataset', icon: <UploadIcon /> },
  { id: 'advisor', label: 'Executive Advisor', icon: <BotIcon />, badge: 'AI' },
  { id: 'forecast', label: 'Forecast Center', icon: <TrendingUpIcon /> },
  {
    id: 'platform_management',
    label: 'Platform Management',
    icon: <DatabaseIcon />,
  },
  { id: 'settings', label: 'Settings', icon: <SettingsIcon /> },
];

function DatabaseIcon() {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <ellipse cx="12" cy="5" rx="8" ry="3" />
      <path d="M4 5v7c0 1.7 3.6 3 8 3s8-1.3 8-3V5" />
      <path d="M4 12v7c0 1.7 3.6 3 8 3s8-1.3 8-3v-7" />
    </svg>
  );
}

function LayoutDashboardIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="3" width="7" height="9" rx="1.5" />
      <rect x="14" y="3" width="7" height="5" rx="1.5" />
      <rect x="14" y="12" width="7" height="9" rx="1.5" />
      <rect x="3" y="16" width="7" height="5" rx="1.5" />
    </svg>
  );
}
function UploadIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <path d="M7 9l5-5 5 5" />
      <path d="M12 4v12" />
    </svg>
  );
}
function BotIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="4" y="8" width="16" height="12" rx="2" />
      <path d="M12 8V4" />
      <circle cx="12" cy="3" r="1" />
      <circle cx="9" cy="13" r="1" />
      <circle cx="15" cy="13" r="1" />
      <path d="M9 17h6" />
      <path d="M2 14h2M20 14h2" />
    </svg>
  );
}
function TrendingUpIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 17l6-6 4 4 7-7" />
      <path d="M17 8h4v4" />
    </svg>
  );
}
function SettingsIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
    </svg>
  );
}

export function Logo({ collapsed = false }: { collapsed?: boolean }) {
  return (
    <div className="flex items-center gap-3">
      <div className="relative flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 shadow-lg shadow-brand-600/30">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
          <path d="M6 17V7l6 4 6-4v10" />
          <circle cx="12" cy="11" r="1.6" fill="white" stroke="none" />
        </svg>
        <span className="absolute -right-0.5 -top-0.5 h-3 w-3 rounded-full border-2 border-white bg-emerald-400" />
      </div>
      {!collapsed && (
        <div className="leading-tight">
          <p className="font-display text-[15px] font-bold tracking-tight text-slate-900">
            ExecuMind<span className="text-brand-600"> AI</span>
          </p>
          <p className="text-[10px] font-medium uppercase tracking-wider text-slate-400">
            Executive Intelligence
          </p>
        </div>
      )}
    </div>
  );
}

export function Sidebar({
  active,
  onNavigate,
  collapsed,
  onToggleCollapse,
  mobileOpen,
  onCloseMobile,
}: {
  active: PageId;
  onNavigate: (id: PageId) => void;
  collapsed: boolean;
  onToggleCollapse: () => void;
  mobileOpen: boolean;
  onCloseMobile: () => void;
}) {
  const { user } = useAuth();
  const { logout } = useAuth();

  const initials =
      user?.username
          ?.substring(0, 2)
          .toUpperCase() || "AD";

  return (
    <>
      {mobileOpen && (
        <div
          className="fixed inset-0 z-30 bg-slate-900/40 backdrop-blur-sm lg:hidden"
          onClick={onCloseMobile}
        />
      )}
      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-40 flex flex-col border-r border-slate-200 bg-white transition-all duration-300 lg:static lg:translate-x-0',
          collapsed ? 'w-[76px]' : 'w-[260px]',
          mobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        )}
      >
        {/* Header */}
        <div className={cn('flex h-16 items-center border-b border-slate-200 px-4', collapsed && 'justify-center px-0')}>
          {collapsed ? <Logo collapsed /> : <Logo />}
        </div>

        {/* Nav */}
        <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4">
          {!collapsed && (
            <p className="px-3 pb-2 pt-1 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
              Workspace
            </p>
          )}
          {NAV_ITEMS.map((item) => {
            const isActive = active === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  onNavigate(item.id);
                  onCloseMobile();
                }}
                title={collapsed ? item.label : undefined}
                className={cn(
                  'group relative flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-150',
                  collapsed && 'justify-center',
                  isActive
                    ? 'bg-brand-50 text-brand-700'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                )}
              >
                {isActive && (
                  <span className="absolute left-0 top-1/2 h-6 w-1 -translate-y-1/2 rounded-r-full bg-brand-600" />
                )}
                <span className={cn('shrink-0', isActive ? 'text-brand-600' : 'text-slate-400 group-hover:text-slate-600')}>
                  {item.icon}
                </span>
                {!collapsed && <span className="flex-1 text-left">{item.label}</span>}
                {!collapsed && item.badge && (
                  <span className="rounded-md bg-brand-600 px-1.5 py-0.5 text-[10px] font-semibold text-white">
                    {item.badge}
                  </span>
                )}
                {collapsed && item.badge && (
                  <span className="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-brand-600" />
                )}
              </button>
            );
          })}
        </nav>

        {/* Collapse toggle (desktop) */}
        <div className="hidden border-t border-slate-200 p-3 lg:block">
          <button
            onClick={onToggleCollapse}
            className={cn(
              'flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-slate-500 transition hover:bg-slate-50 hover:text-slate-800',
              collapsed && 'justify-center'
            )}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={cn('transition-transform duration-300', collapsed && 'rotate-180')}>
              <path d="M15 18l-6-6 6-6" />
            </svg>
            {!collapsed && <span>Collapse</span>}
          </button>
        </div>

        {/* User card */}
        <div className={cn('border-t border-slate-200 p-3', collapsed && 'px-2')}>
          <div className={cn('flex items-center gap-3 rounded-xl p-2', !collapsed && 'hover:bg-slate-50')}>
            <div className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-slate-700 to-slate-900 text-xs font-semibold text-white">
                {initials}
            </div>
            {!collapsed && (
              <div className="min-w-0 flex-1">
                <p className="truncate text-sm font-semibold text-slate-800">
                    {user?.username}
                </p>

                <p className="truncate text-xs text-slate-400">
                    Administrator
                </p>
              </div>
            )}
          </div>
        </div>
        <button
          onClick={logout}
          className="
              mt-3
              flex
              w-full
              items-center
              justify-center
              rounded-xl
              border
              border-slate-200
              px-3
              py-2
              text-sm
              font-medium
              text-slate-600
              transition
              hover:bg-red-50
              hover:text-red-600
          "
      >
          Logout
      </button>
      </aside>
    </>
  );
}
