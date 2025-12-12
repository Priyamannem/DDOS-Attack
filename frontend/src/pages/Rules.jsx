import React, { useEffect, useState } from 'react';
import client from '../api/client';
import { Save, RefreshCw, Shield, AlertCircle } from 'lucide-react';
import { clsx } from 'clsx';

const Rules = () => {
    const [formData, setFormData] = useState({
        max_req_per_sec: 10,
        max_req_per_min: 100,
        block_duration: 300,
        anomaly_threshold: 5000
    });
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [message, setMessage] = useState(null);

    const fetchRules = async () => {
        try {
            const res = await client.get('/admin/rules');
            if (res.data.success) {
                setFormData(res.data.rules);
            }
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRules();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: parseInt(value)
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSaving(true);
        setMessage(null);
        try {
            const res = await client.post('/admin/update_rules', formData);
            if (res.data.success) {
                setMessage({ type: 'success', text: 'Rules updated successfully' });
            }
        } catch (err) {
            setMessage({ type: 'error', text: 'Failed to update rules' });
        } finally {
            setSaving(false);
        }
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <div>
                <h2 className="text-2xl font-bold text-white">Protection Rules</h2>
                <p className="text-gray-400 text-sm">Configure DDoS mitigation thresholds</p>
            </div>

            {message && (
                <div className={clsx(
                    "p-4 rounded-xl border flex items-center mb-6 animate-fade-in",
                    message.type === 'success' ? "bg-success/10 border-success/20 text-success" : "bg-danger/10 border-danger/20 text-danger"
                )}>
                    {message.type === 'success' ? <Shield className="w-5 h-5 mr-2" /> : <AlertCircle className="w-5 h-5 mr-2" />}
                    {message.text}
                </div>
            )}

            <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Rate Limiting Card */}
                <div className="bg-surface/50 backdrop-blur-xl border border-white/5 p-6 rounded-2xl space-y-4">
                    <h3 className="text-lg font-semibold text-white flex items-center">
                        <Shield className="w-5 h-5 mr-2 text-primary" />
                        Rate Limiting
                    </h3>

                    <div className="space-y-2">
                        <label className="block text-sm font-medium text-gray-400">Max Requests Per Second</label>
                        <input
                            type="number"
                            name="max_req_per_sec"
                            value={formData.max_req_per_sec || ''}
                            onChange={handleChange}
                            className="w-full bg-darker border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary/50 transition-colors"
                        />
                        <p className="text-xs text-gray-500">Threshold for immediate blocking (per IP)</p>
                    </div>

                    <div className="space-y-2">
                        <label className="block text-sm font-medium text-gray-400">Max Requests Per Minute</label>
                        <input
                            type="number"
                            name="max_req_per_min"
                            value={formData.max_req_per_min || ''}
                            onChange={handleChange}
                            className="w-full bg-darker border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary/50 transition-colors"
                        />
                        <p className="text-xs text-gray-500">Sustained traffic threshold</p>
                    </div>
                </div>

                {/* Mitigation Card */}
                <div className="bg-surface/50 backdrop-blur-xl border border-white/5 p-6 rounded-2xl space-y-4">
                    <h3 className="text-lg font-semibold text-white flex items-center">
                        <AlertCircle className="w-5 h-5 mr-2 text-accent" />
                        Mitigation Policy
                    </h3>

                    <div className="space-y-2">
                        <label className="block text-sm font-medium text-gray-400">Block Duration (Seconds)</label>
                        <input
                            type="number"
                            name="block_duration"
                            value={formData.block_duration || ''}
                            onChange={handleChange}
                            className="w-full bg-darker border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary/50 transition-colors"
                        />
                        <p className="text-xs text-gray-500">How long an IP remains blocked</p>
                    </div>

                    <div className="space-y-2">
                        <label className="block text-sm font-medium text-gray-400">Anomaly Threshold</label>
                        <input
                            type="number"
                            name="anomaly_threshold"
                            value={formData.anomaly_threshold || ''}
                            onChange={handleChange}
                            className="w-full bg-darker border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary/50 transition-colors"
                        />
                        <p className="text-xs text-gray-500">Score at which traffic is flagged as suspicious</p>
                    </div>
                </div>

                <div className="md:col-span-2 flex justify-end">
                    <button
                        type="submit"
                        disabled={saving}
                        className="px-6 py-2 bg-primary hover:bg-primary/90 text-white rounded-lg font-medium transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-primary/25"
                    >
                        {saving ? <RefreshCw className="animate-spin w-4 h-4 mr-2" /> : <Save className="w-4 h-4 mr-2" />}
                        Save Configuration
                    </button>
                </div>
            </form>
        </div>
    );
};

export default Rules;
