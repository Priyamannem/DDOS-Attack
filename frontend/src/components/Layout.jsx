import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Activity, Shield, Globe, Menu, X } from 'lucide-react';
import { clsx } from 'clsx';

const Sidebar = ({ isOpen, toggle }) => {
    const links = [
        { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
        { to: '/logs', icon: Activity, label: 'Live Logs' },
        { to: '/rules', icon: Shield, label: 'Protection Rules' },
        { to: '/ip-manager', icon: Globe, label: 'IP Management' },
        { to: '/attack-simulator', icon: Activity, label: 'Attack Simulator' },
    ];

    return (
        <>
            {/* Mobile Backdrop */}
            {isOpen && (
                <div
                    className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
                    onClick={toggle}
                />
            )}

            <aside className={clsx(
                "fixed inset-y-0 left-0 z-50 w-64 bg-surface/50 backdrop-blur-xl border-r border-white/10 transition-transform duration-300 ease-in-out lg:translate-x-0 h-screen",
                isOpen ? "translate-x-0" : "-translate-x-full"
            )}>
                <div className="flex flex-col h-full">
                    <div className="h-16 flex items-center px-6 border-b border-white/10 shrink-0">
                        <Shield className="w-8 h-8 text-primary mr-3" />
                        <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
                            DDoS Guard
                        </h1>
                    </div>
                    <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
                        {links.map((link) => (
                            <NavLink
                                key={link.to}
                                to={link.to}
                                onClick={() => window.innerWidth < 1024 && toggle()}
                                className={({ isActive }) => clsx(
                                    "flex items-center px-4 py-3 rounded-xl transition-all duration-200 group relative overflow-hidden",
                                    isActive
                                        ? "text-primary shadow-[0_0_20px_rgba(59,130,246,0.15)] border border-primary/20 bg-primary/10"
                                        : "text-gray-400 hover:bg-white/5 hover:text-gray-100"
                                )}
                            >
                                {({ isActive }) => (
                                    <>
                                        <div className={clsx(
                                            "absolute inset-0 opacity-0 transition-opacity duration-300",
                                            isActive ? "bg-gradient-to-r from-primary/10 to-transparent opacity-100" : ""
                                        )} />
                                        <link.icon className={clsx("w-5 h-5 mr-3 z-10", isActive && "fill-current opacity-50")} />
                                        <span className="font-medium z-10">{link.label}</span>
                                    </>
                                )}
                            </NavLink>
                        ))}
                    </nav>
                    <div className="p-4 border-t border-white/10 shrink-0">
                        <div className="bg-gradient-to-br from-primary/10 to-secondary/10 rounded-xl p-4 border border-white/5 relative overflow-hidden group">
                            <div className="absolute inset-0 bg-gradient-to-r from-primary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                            <h4 className="text-sm font-bold text-gray-200 mb-1 z-10 relative">System Status</h4>
                            <div className="flex items-center z-10 relative">
                                <span className="relative flex h-2 w-2 mr-2">
                                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-success opacity-75"></span>
                                    <span className="relative inline-flex rounded-full h-2 w-2 bg-success"></span>
                                </span>
                                <span className="text-xs text-success font-semibold tracking-wide uppercase">Active Protection</span>
                            </div>
                        </div>
                    </div>
                </div>
            </aside>
        </>
    );
};

const Layout = ({ children }) => {
    const [sidebarOpen, setSidebarOpen] = React.useState(false);

    return (
        <div className="min-h-screen bg-darker text-gray-100 flex overflow-hidden bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-darker to-darker">
            <Sidebar isOpen={sidebarOpen} toggle={() => setSidebarOpen(!sidebarOpen)} />

            <div className="flex-1 flex flex-col lg:pl-64 min-h-screen transition-all duration-300 w-full relative">
                <header className="h-16 flex items-center justify-between px-6 border-b border-white/5 bg-darker/50 backdrop-blur-md sticky top-0 z-40">
                    <button
                        onClick={() => setSidebarOpen(!sidebarOpen)}
                        className="lg:hidden p-2 rounded-lg text-gray-400 hover:bg-white/5 focus:outline-none focus:ring-2 focus:ring-primary/50"
                    >
                        {sidebarOpen ? <X /> : <Menu />}
                    </button>
                    <div className="flex items-center space-x-4 ml-auto">
                        <div className="flex items-center space-x-2 text-xs font-mono text-gray-500 bg-white/5 px-3 py-1.5 rounded-full border border-white/5 hover:border-primary/20 transition-colors">
                            <span className="h-1.5 w-1.5 rounded-full bg-success animate-pulse"></span>
                            <span>Server Online</span>
                        </div>
                    </div>
                </header>

                <main className="flex-1 overflow-x-hidden overflow-y-auto p-4 md:p-8 scroll-smooth">
                    <div className="max-w-7xl mx-auto w-full animate-fade-in pb-10">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
};

export default Layout;
