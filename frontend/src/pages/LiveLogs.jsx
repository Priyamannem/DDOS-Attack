import React, { useEffect, useState } from 'react';
import client from '../api/client';
import { RefreshCcw, Search, AlertTriangle, CheckCircle, Ban, Activity } from 'lucide-react';
import { clsx } from 'clsx';

const LiveLogs = () => {
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('');

    const fetchLogs = async () => {
        try {
            const res = await client.get('/admin/logs/recent?limit=200');
            if (res.data.success) {
                setLogs(res.data.logs);
            }
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchLogs();
        const interval = setInterval(fetchLogs, 5000);
        return () => clearInterval(interval);
    }, []);

    const filteredLogs = logs.filter(l =>
        (l.ip && l.ip.includes(filter)) ||
        (l.path && l.path.includes(filter)) ||
        (l.method && l.method.includes(filter))
    );

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold text-white">Live Traffic Logs</h2>
                    <p className="text-gray-400 text-sm">Real-time incoming request monitoring</p>
                </div>
                <div className="flex space-x-4">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-4 h-4" />
                        <input
                            type="text"
                            placeholder="Search IP, Path..."
                            className="bg-surface border border-white/10 rounded-lg pl-10 pr-4 py-2 text-sm text-white focus:outline-none focus:border-primary/50 w-64 transition-all"
                            value={filter}
                            onChange={(e) => setFilter(e.target.value)}
                        />
                    </div>
                    <button
                        onClick={fetchLogs}
                        className="p-2 bg-surface border border-white/10 rounded-lg hover:bg-white/5 text-gray-400 hover:text-white transition-colors"
                    >
                        <RefreshCcw className="w-5 h-5" />
                    </button>
                </div>
            </div>

            <div className="bg-surface/50 backdrop-blur-xl border border-white/5 rounded-2xl overflow-hidden shadow-xl">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-white/5 border-b border-white/5 text-xs uppercase text-gray-400 font-medium">
                                <th className="p-4">Time</th>
                                <th className="p-4">IP Address</th>
                                <th className="p-4">Method</th>
                                <th className="p-4">Path</th>
                                <th className="p-4">Status</th>
                                <th className="p-4">Lat. (ms)</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/5">
                            {filteredLogs.map((log) => (
                                <tr key={log.id} className="hover:bg-white/5 transition-colors group">
                                    <td className="p-4 text-sm text-gray-400 font-mono whitespace-nowrap">
                                        {new Date(log.timestamp).toLocaleTimeString()}
                                    </td>
                                    <td className="p-4 text-sm font-medium text-white group-hover:text-primary transition-colors font-mono">
                                        {log.ip}
                                    </td>
                                    <td className="p-4">
                                        <span className={clsx(
                                            "px-2 py-1 rounded text-xs font-bold",
                                            log.method === 'GET' && "bg-blue-500/10 text-blue-400",
                                            log.method === 'POST' && "bg-green-500/10 text-green-400",
                                            log.method === 'DELETE' && "bg-red-500/10 text-red-400",
                                            log.method === 'PUT' && "bg-orange-500/10 text-orange-400",
                                        )}>
                                            {log.method}
                                        </span>
                                    </td>
                                    <td className="p-4 text-sm text-gray-300 max-w-xs truncate" title={log.path}>
                                        {log.path}
                                    </td>
                                    <td className="p-4">
                                        <div className="flex items-center space-x-2">
                                            {log.status_code >= 400 ? <AlertTriangle className="w-4 h-4 text-warning" /> : <div className="w-2 h-2 rounded-full bg-success"></div>}
                                            <span className={clsx(
                                                "text-sm font-medium",
                                                log.status_code >= 400 ? "text-warning" : "text-success"
                                            )}>
                                                {log.status_code}
                                            </span>
                                        </div>
                                    </td>
                                    <td className="p-4 text-sm text-gray-400 tabular-nums">
                                        {log.process_time_ms ? log.process_time_ms.toFixed(2) : '-'}
                                    </td>
                                </tr>
                            ))}
                            {filteredLogs.length === 0 && (
                                <tr>
                                    <td colSpan="6" className="p-8 text-center text-gray-500">
                                        No logs found matching criteria
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default LiveLogs;
