import { useState } from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { Shield, Activity, Scan, FileWarning, FileText, Settings, Menu, X } from 'lucide-react';

const Layout = () => {
    const [sidebarOpen, setSidebarOpen] = useState(true);

    const navigation = [
        { name: 'Dashboard', path: '/', icon: Activity },
        { name: 'Scans', path: '/scans', icon: Scan },
        { name: 'Threats', path: '/threats', icon: FileWarning },
        { name: 'Reports', path: '/reports', icon: FileText },
        { name: 'Settings', path: '/settings', icon: Settings },
    ];

    return (
        <div className="min-h-screen bg-slate-950 text-slate-200">
            {/* Sidebar */}
            <aside className={`fixed left-0 top-0 h-full bg-slate-900 border-r border-slate-800 transition-all duration-300 z-50 ${sidebarOpen ? 'w-64' : 'w-20'}`}>
                {/* Logo */}
                <div className="flex items-center justify-between p-4 border-b border-slate-800">
                    {sidebarOpen ? (
                        <div className="flex items-center gap-2">
                            <div className="relative">
                                <Shield className="w-8 h-8 text-emerald-500" />
                                <div className="absolute inset-0 bg-emerald-500/20 blur-lg rounded-full animate-pulse"></div>
                            </div>
                            <span className="text-xl font-bold">
                                Threat<span className="text-emerald-500">Fusion</span>
                            </span>
                        </div>
                    ) : (
                        <Shield className="w-8 h-8 text-emerald-500 mx-auto" />
                    )}

                    <button
                        onClick={() => setSidebarOpen(!sidebarOpen)}
                        className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
                    >
                        {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
                    </button>
                </div>

                {/* Navigation */}
                <nav className="p-4 space-y-2">
                    {navigation.map((item) => {
                        const Icon = item.icon;
                        return (
                            <NavLink
                                key={item.path}
                                to={item.path}
                                end={item.path === '/'}
                                className={({ isActive }) =>
                                    `flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${isActive
                                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/50'
                                        : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
                                    }`
                                }
                            >
                                <Icon className="w-5 h-5" />
                                {sidebarOpen && <span className="font-medium">{item.name}</span>}
                            </NavLink>
                        );
                    })}
                </nav>

                {/* System Status */}
                {sidebarOpen && (
                    <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-slate-800">
                        <div className="glass rounded-lg p-3">
                            <div className="flex items-center gap-2 mb-2">
                                <div className="relative flex h-2 w-2">
                                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                                    <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                                </div>
                                <span className="text-xs text-emerald-400 font-medium">System Online</span>
                            </div>
                            <p className="text-xs text-slate-500">v1.0.0</p>
                        </div>
                    </div>
                )}
            </aside>

            {/* Main content */}
            <main className={`transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-20'}`}>
                <Outlet />
            </main>
        </div>
    );
};

export default Layout;
