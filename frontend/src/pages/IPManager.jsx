import React, { useEffect, useState } from 'react';
import client from '../api/client';
import { Ban, CheckCircle, Trash2, Plus, Lock } from 'lucide-react';
import { clsx } from 'clsx';

const IPManager = () => {
    const [activeTab, setActiveTab] = useState('blocked');
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);

    // Add IP Form State
    const [newIP, setNewIP] = useState('');
    const [reason, setReason] = useState('');
    const [adding, setAdding] = useState(false);

    const fetchData = async () => {
        setLoading(true);
        try {
            let endpoint = '/admin/blocked_ips';
            if (activeTab === 'blacklist') endpoint = '/admin/blacklist';
            if (activeTab === 'whitelist') endpoint = '/admin/whitelist';

            const res = await client.get(endpoint);
            if (res.data.success) {
                // Backend returns different keys
                if (activeTab === 'blocked') setData(res.data.blocked_ips || []);
                if (activeTab === 'blacklist') setData(res.data.blacklist || []);
                if (activeTab === 'whitelist') setData(res.data.whitelist || []);
            }
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        if (activeTab === 'blocked') {
            const interval = setInterval(fetchData, 5000);
            return () => clearInterval(interval);
        }
    }, [activeTab]);

    const handleAdd = async (e) => {
        e.preventDefault();
        if (!newIP) return;
        setAdding(true);
        try {
            if (activeTab === 'blacklist') {
                await client.post('/admin/add_to_blacklist', { ip: newIP, reason: reason || 'Manual add' });
            } else if (activeTab === 'whitelist') {
                await client.post('/admin/add_to_whitelist', { ip: newIP });
            }
            setNewIP('');
            setReason('');
            fetchData();
        } catch (err) {
            alert('Failed to add IP');
        } finally {
            setAdding(false);
        }
    };

    const handleRemove = async (ip) => {
        if (!window.confirm(`Are you sure you want to remove ${ip}?`)) return;
        try {
            if (activeTab === 'blocked') {
                await client.post('/admin/unblock_ip', { ip });
            } else {
                await client.post('/admin/remove_ip', { ip });
            }
            fetchData();
        } catch (err) {
            alert('Failed to remove IP');
        }
    };

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold text-white">IP Management</h2>
                <p className="text-gray-400 text-sm">Manage access control lists and blocked IPs</p>
            </div>

            {/* Tabs */}
            <div className="flex space-x-1 bg-surface/50 p-1 rounded-xl w-fit border border-white/5 backdrop-blur-md">
                {[
                    { id: 'blocked', label: 'Blocked IPs', icon: Ban },
                    { id: 'blacklist', label: 'Blacklist', icon: Lock },
                    { id: 'whitelist', label: 'Whitelist', icon: CheckCircle },
                ].map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={clsx(
                            "flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 focus:outline-none",
                            activeTab === tab.id
                                ? "bg-primary text-white shadow-lg shadow-primary/25"
                                : "text-gray-400 hover:text-white hover:bg-white/5"
                        )}
                    >
                        <tab.icon className="w-4 h-4 mr-2" />
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* Add Form (Only for Blacklist/Whitelist) */}
            {activeTab !== 'blocked' && (
                <form onSubmit={handleAdd} className="bg-surface/50 border border-white/5 p-4 rounded-xl flex items-end gap-4 backdrop-blur-md animate-fade-in">
                    <div className="flex-1 space-y-1">
                        <label className="text-xs text-gray-400 font-medium">IP Address</label>
                        <input
                            type="text"
                            placeholder="e.g. 192.168.1.1"
                            className="w-full bg-darker border border-white/10 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-primary/50 transition-colors"
                            value={newIP}
                            onChange={(e) => setNewIP(e.target.value)}
                        />
                    </div>
                    {activeTab === 'blacklist' && (
                        <div className="flex-1 space-y-1">
                            <label className="text-xs text-gray-400 font-medium">Reason</label>
                            <input
                                type="text"
                                placeholder="e.g. Malicious Activity"
                                className="w-full bg-darker border border-white/10 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-primary/50 transition-colors"
                                value={reason}
                                onChange={(e) => setReason(e.target.value)}
                            />
                        </div>
                    )}
                    <button
                        type="submit"
                        disabled={adding || !newIP}
                        className="px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 text-white rounded-lg flex items-center transition-colors disabled:opacity-50"
                    >
                        <Plus className="w-4 h-4 mr-2" />
                        Add
                    </button>
                </form>
            )}

            {/* List */}
            <div className="bg-surface/50 backdrop-blur-xl border border-white/5 rounded-2xl overflow-hidden shadow-xl min-h-[400px]">
                {loading ? (
                    <div className="p-8 text-center text-gray-400">Loading...</div>
                ) : (
                    <table className="w-full text-left">
                        <thead>
                            <tr className="bg-white/5 border-b border-white/5 text-xs uppercase text-gray-400 font-medium">
                                <th className="p-4">IP Address</th>
                                {activeTab === 'blocked' ? <th className="p-4">Blocked Until</th> : null}
                                {activeTab !== 'whitelist' ? <th className="p-4">Reason</th> : null}
                                <th className="p-4 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/5">
                            {data.map((item, i) => {
                                // Data structure varies:
                                // Blocked & Blacklist might return objects with IP and fields.
                                // Whitelist might just be IP strings or objects.
                                // Safe access:
                                const ip = typeof item === 'object' ? (item.ip || item.address) : item;
                                const reasonText = item.reason || '-';
                                const blockedUntil = item.unblock_time ? new Date(item.unblock_time * 1000).toLocaleString() : (item.expires_at ? new Date(item.expires_at).toLocaleString() : '-');

                                return (
                                    <tr key={i} className="hover:bg-white/5 transition-colors group">
                                        <td className="p-4 font-mono text-sm text-white">{ip}</td>
                                        {activeTab === 'blocked' ? <td className="p-4 text-sm text-gray-400">{blockedUntil}</td> : null}
                                        {activeTab !== 'whitelist' ? <td className="p-4 text-sm text-gray-400">{reasonText}</td> : null}
                                        <td className="p-4 text-right">
                                            <button
                                                onClick={() => handleRemove(ip)}
                                                className="p-2 hover:bg-red-500/10 text-gray-400 hover:text-red-400 rounded-lg transition-colors"
                                                title="Remove / Unblock"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </button>
                                        </td>
                                    </tr>
                                )
                            })}
                            {data.length === 0 && (
                                <tr>
                                    <td colSpan="4" className="p-8 text-center text-gray-500">
                                        No entries found
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
};

export default IPManager;
