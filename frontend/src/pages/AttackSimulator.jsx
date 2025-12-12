import React, { useState } from 'react';
import client from '../api/client';
import { Skull, Zap, ShieldAlert, Activity, Play, CheckCircle } from 'lucide-react';
import { clsx } from 'clsx';

const AttackConsole = () => {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    // High Traffic State
    const [trafficCount, setTrafficCount] = useState(1000);
    const [trafficIP, setTrafficIP] = useState('random');

    // DDoS State
    const [ddosIPs, setDdosIPs] = useState(50);
    const [ddosReqs, setDdosReqs] = useState(200);

    const runHighTraffic = async () => {
        setLoading(true);
        setResult(null);
        try {
            const res = await client.get(`/simulate/high-traffic?count=${trafficCount}&ip=${trafficIP}`);
            if (res.data.success) {
                setResult({
                    type: 'success',
                    title: 'Traffic Simulation Complete',
                    data: res.data
                });
            }
        } catch (err) {
            setResult({
                type: 'error',
                title: 'Simulation Failed',
                message: err.message
            });
        } finally {
            setLoading(false);
        }
    };

    const runDDoS = async () => {
        setLoading(true);
        setResult(null);
        try {
            // Warning: This can take time
            const res = await client.get(`/simulate/ddos-attack?target_ips=${ddosIPs}&requests_per_ip=${ddosReqs}`);
            if (res.data.success) {
                setResult({
                    type: 'warning',
                    title: 'DDoS Simulation Report',
                    data: res.data
                });
            }
        } catch (err) {
            setResult({
                type: 'error',
                title: 'Simulation Failed',
                message: err.message
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-5xl mx-auto space-y-8">
            <div>
                <h2 className="text-2xl font-bold text-white flex items-center">
                    <Skull className="w-8 h-8 mr-3 text-danger" />
                    Attack Simulator
                </h2>
                <p className="text-gray-400 text-sm mt-1">
                    Test your defenses by simulating traffic and attacks.
                    <span className="text-warning ml-2 font-medium">Warning: This generates real load on the backend.</span>
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* High Traffic Simulation */}
                <div className="bg-surface/50 backdrop-blur-xl border border-white/5 p-6 rounded-2xl relative overflow-hidden group">
                    <div className="absolute top-0 right-0 p-4 opacity-10 text-primary">
                        <Activity size={100} />
                    </div>

                    <h3 className="text-xl font-bold text-white mb-6 flex items-center relative z-10">
                        <Zap className="w-5 h-5 mr-2 text-primary" />
                        Request Flood
                    </h3>

                    <div className="space-y-4 relative z-10">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-400">Request Count</label>
                            <input
                                type="number"
                                value={trafficCount}
                                onChange={(e) => setTrafficCount(parseInt(e.target.value))}
                                className="w-full bg-darker border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary/50"
                                min="1" max="10000"
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-400">Source IP</label>
                            <select
                                value={trafficIP}
                                onChange={(e) => setTrafficIP(e.target.value)}
                                className="w-full bg-darker border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-primary/50"
                            >
                                <option value="random">Random IPs (Distributed)</option>
                                <option value="auto">Single IP (DoS)</option>
                            </select>
                        </div>

                        <button
                            onClick={runHighTraffic}
                            disabled={loading}
                            className="w-full py-3 bg-primary hover:bg-primary/90 text-white rounded-xl font-bold transition-all shadow-lg hover:shadow-primary/25 disabled:opacity-50 flex items-center justify-center mt-4"
                        >
                            {loading ? <Activity className="w-5 h-5 animate-spin mr-2" /> : <Play className="w-5 h-5 mr-2 fill-current" />}
                            Launch Flood
                        </button>
                    </div>
                </div>

                {/* DDoS Simulation */}
                <div className="bg-surface/50 backdrop-blur-xl border border-white/5 p-6 rounded-2xl relative overflow-hidden group">
                    <div className="absolute top-0 right-0 p-4 opacity-10 text-danger">
                        <ShieldAlert size={100} />
                    </div>

                    <h3 className="text-xl font-bold text-white mb-6 flex items-center relative z-10">
                        <Skull className="w-5 h-5 mr-2 text-danger" />
                        Botnet Attack
                    </h3>

                    <div className="space-y-4 relative z-10">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-400">Bot Count (Unique IPs)</label>
                            <input
                                type="number"
                                value={ddosIPs}
                                onChange={(e) => setDdosIPs(parseInt(e.target.value))}
                                className="w-full bg-darker border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-danger/50"
                                min="1" max="1000"
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-400">Requests Per Bot</label>
                            <input
                                type="number"
                                value={ddosReqs}
                                onChange={(e) => setDdosReqs(parseInt(e.target.value))}
                                className="w-full bg-darker border border-white/10 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-danger/50"
                                min="1" max="10000"
                            />
                        </div>

                        <button
                            onClick={runDDoS}
                            disabled={loading}
                            className="w-full py-3 bg-danger hover:bg-danger/90 text-white rounded-xl font-bold transition-all shadow-lg hover:shadow-danger/25 disabled:opacity-50 flex items-center justify-center mt-4"
                        >
                            {loading ? <ShieldAlert className="w-5 h-5 animate-pulse mr-2" /> : <Play className="w-5 h-5 mr-2 fill-current" />}
                            Launch Attack
                        </button>
                    </div>
                </div>
            </div>

            {/* Results Console */}
            {result && (
                <div className={clsx(
                    "w-full rounded-2xl border p-6 animate-fade-in relative overflow-hidden",
                    result.type === 'success' ? "bg-primary/5 border-primary/20" :
                        result.type === 'warning' ? "bg-danger/5 border-danger/20" :
                            "bg-red-500/10 border-red-500/30"
                )}>
                    <div className="flex items-start justify-between mb-4">
                        <div className="flex items-center">
                            {result.type === 'success' ? <CheckCircle className="text-primary mr-3" /> :
                                result.type === 'warning' ? <ShieldAlert className="text-danger mr-3" /> :
                                    <Skull className="text-red-500 mr-3" />}
                            <h4 className="text-lg font-bold text-white">{result.title}</h4>
                        </div>
                        <button onClick={() => setResult(null)} className="text-gray-400 hover:text-white">Close</button>
                    </div>

                    <div className="bg-darker/50 rounded-xl p-4 font-mono text-sm overflow-x-auto border border-white/5">
                        <pre className="text-gray-300">
                            {JSON.stringify(result.data || result.message, null, 2)}
                        </pre>
                    </div>

                    {result.type === 'warning' && (
                        <div className="mt-4 flex gap-4">
                            <div className="px-4 py-2 bg-danger/10 text-danger rounded-lg text-sm font-bold flex flex-col items-center">
                                <span className="text-xs font-normal opacity-70">Blocked IPs</span>
                                {result.data.blocked_count}
                            </div>
                            <div className="px-4 py-2 bg-primary/10 text-primary rounded-lg text-sm font-bold flex flex-col items-center">
                                <span className="text-xs font-normal opacity-70">Total Reqs</span>
                                {result.data.total_requests}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default AttackConsole;
