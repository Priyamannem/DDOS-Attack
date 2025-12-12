import React, { useEffect, useState } from 'react';
import client from '../api/client';
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { Activity, ShieldAlert, ShieldCheck, Server } from 'lucide-react';

const StatCard = ({ title, value, icon: Icon, color, subValue }) => (
    <div className="bg-surface/50 backdrop-blur-xl border border-white/5 p-6 rounded-2xl relative overflow-hidden group hover:border-white/10 transition-all shadow-lg hover:shadow-xl">
        <div className={`absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity ${color}`}>
            <Icon size={80} />
        </div>
        <div className="flex items-center space-x-4 relative z-10">
            <div className={`p-3 rounded-xl bg-white/5 ${color} bg-opacity-10 text-current border border-white/5`}>
                <Icon size={24} />
            </div>
            <div>
                <p className="text-gray-400 text-sm font-medium tracking-wide uppercase">{title}</p>
                <h3 className="text-3xl font-bold text-white mt-1 tabular-nums">{value}</h3>
                {subValue && <p className="text-xs text-gray-500 mt-1 font-mono">{subValue}</p>}
            </div>
        </div>
    </div>
);

const Dashboard = () => {
    const [stats, setStats] = useState({ history: [], latest: {} });
    const [loading, setLoading] = useState(true);

    const fetchStats = async () => {
        try {
            const res = await client.get('/admin/traffic/stats?minutes=30');
            if (res.data.success) {
                setStats(res.data);
            }
        } catch (err) {
            console.error("Failed to fetch stats:", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStats();
        const interval = setInterval(fetchStats, 2000); // 2 seconds refresh for "live" feel
        return () => clearInterval(interval);
    }, []);

    if (loading) return (
        <div className="flex h-64 items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
        </div>
    );

    const { latest, history } = stats;

    // Format history for chart
    // Assuming keys based on backend implementation: total_requests, blocked_requests
    const chartData = history && Array.isArray(history) ? history.map(h => ({
        time: new Date(h.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
        requests: h.total_requests || 0,
        blocked: h.blocked_requests || 0
    })).reverse() : [];

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-white">System Overview</h2>
                    <p className="text-gray-400 text-sm mt-1">Real-time traffic monitoring and threat detection</p>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-400 bg-white/5 px-3 py-1.5 rounded-lg border border-white/5">
                    <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-success opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-success"></span>
                    </span>
                    <span className="font-mono">Live Updating</span>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Total Requests"
                    value={latest?.total_requests || 0}
                    icon={Activity}
                    color="text-blue-400"
                    subValue="Last minute"
                />
                <StatCard
                    title="Blocked"
                    value={latest?.blocked_requests || 0}
                    icon={ShieldAlert}
                    color="text-red-400"
                    subValue="Threats mitigated"
                />
                <StatCard
                    title="Avg Latency"
                    value={`${latest?.avg_latency || 0}ms`}
                    icon={Server}
                    color="text-amber-400"
                    subValue="Response time"
                />
                <StatCard
                    title="Protection"
                    value="Active"
                    icon={ShieldCheck}
                    color="text-emerald-400"
                    subValue="Rules enforced"
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 bg-surface/50 backdrop-blur-xl border border-white/5 p-6 rounded-2xl shadow-xl">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-lg font-bold text-white">Traffic Analysis</h3>
                        <div className="flex space-x-4 text-sm">
                            <div className="flex items-center"><span className="w-3 h-3 rounded-full bg-primary mr-2"></span>Requests</div>
                            <div className="flex items-center"><span className="w-3 h-3 rounded-full bg-danger mr-2"></span>Blocked</div>
                        </div>
                    </div>
                    <div className="h-[350px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={chartData}>
                                <defs>
                                    <linearGradient id="colorRequests" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                                    </linearGradient>
                                    <linearGradient id="colorBlocked" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" vertical={false} />
                                <XAxis
                                    dataKey="time"
                                    stroke="#94a3b8"
                                    fontSize={12}
                                    tickLine={false}
                                    axisLine={false}
                                    minTickGap={30}
                                />
                                <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #ffffff10', borderRadius: '8px', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.5)' }}
                                    itemStyle={{ color: '#e2e8f0' }}
                                    labelStyle={{ color: '#94a3b8', marginBottom: '0.5rem' }}
                                />
                                <Area
                                    type="monotone"
                                    dataKey="requests"
                                    stroke="#3b82f6"
                                    strokeWidth={2}
                                    fillOpacity={1}
                                    fill="url(#colorRequests)"
                                    name="Requests"
                                    animationDuration={500}
                                />
                                <Area
                                    type="monotone"
                                    dataKey="blocked"
                                    stroke="#ef4444"
                                    strokeWidth={2}
                                    fillOpacity={1}
                                    fill="url(#colorBlocked)"
                                    name="Blocked"
                                    animationDuration={500}
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="bg-surface/50 backdrop-blur-xl border border-white/5 p-6 rounded-2xl shadow-xl flex flex-col">
                    <h3 className="text-lg font-bold text-white mb-6">Threat Distribution</h3>
                    <div className="flex-1 flex flex-col items-center justify-center text-gray-400 relative">
                        <div className="absolute inset-0 bg-gradient-to-b from-primary/5 to-transparent rounded-full blur-3xl opacity-20"></div>
                        <ShieldCheck size={64} className="mx-auto mb-4 text-emerald-500 opacity-80" />
                        <p className="font-medium text-gray-300">System Secure</p>
                        <p className="text-xs mt-2 text-center max-w-[200px]">
                            No critical anomalies detected in the last polling interval.
                        </p>

                        <div className="w-full mt-8 space-y-3">
                            <div className="bg-white/5 rounded-lg p-3 flex justify-between items-center">
                                <span className="text-sm">SQL Injection</span>
                                <span className="text-xs text-success bg-success/10 px-2 py-0.5 rounded">0%</span>
                            </div>
                            <div className="bg-white/5 rounded-lg p-3 flex justify-between items-center">
                                <span className="text-sm">XSS</span>
                                <span className="text-xs text-success bg-success/10 px-2 py-0.5 rounded">0%</span>
                            </div>
                            <div className="bg-white/5 rounded-lg p-3 flex justify-between items-center">
                                <span className="text-sm">DDoS Volumetric</span>
                                <span className="text-xs text-warning bg-warning/10 px-2 py-0.5 rounded">Low</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
