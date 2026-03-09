import { useState, useEffect } from 'react';
import { Shield, Activity, AlertTriangle, FileSearch, Terminal, Play, TrendingUp } from 'lucide-react';
import { threatFusionAPI, WebSocketClient } from '../services/api';
import ThreatChart from '../components/ThreatChart';
import StatCard from '../components/StatCard';
import RecentThreats from '../components/RecentThreats';
import ScanProgress from '../components/ScanProgress';

const Dashboard = () => {
    const [statistics, setStatistics] = useState(null);
    const [currentScan, setCurrentScan] = useState(null);
    const [recentThreats, setRecentThreats] = useState([]);
    const [loading, setLoading] = useState(true);
    const [wsClient] = useState(() => new WebSocketClient());

    useEffect(() => {
        // Fetch initial data
        fetchData();

        // Connect WebSocket
        wsClient.connect();

        wsClient.on('scan_started', (data) => {
            console.log('Scan started:', data);
            fetchCurrentScan();
        });

        wsClient.on('scan_progress', (data) => {
            console.log('Scan progress:', data);
            fetchCurrentScan();
        });

        wsClient.on('scan_completed', (data) => {
            console.log('Scan completed:', data);
            fetchData();
        });

        return () => {
            wsClient.disconnect();
        };
    }, []);

    const fetchData = async () => {
        try {
            const [statsRes, threatsRes, scanRes] = await Promise.all([
                threatFusionAPI.getStatistics(),
                threatFusionAPI.getThreats({ limit: 10 }),
                threatFusionAPI.getCurrentScan(),
            ]);

            setStatistics(statsRes.data);
            setRecentThreats(threatsRes.data.threats);
            setCurrentScan(scanRes.data.status !== 'idle' ? scanRes.data : null);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching data:', error);
            setLoading(false);
        }
    };

    const fetchCurrentScan = async () => {
        try {
            const res = await threatFusionAPI.getCurrentScan();
            setCurrentScan(res.data.status !== 'idle' ? res.data : null);
        } catch (error) {
            console.error('Error fetching current scan:', error);
        }
    };

    const startQuickScan = async () => {
        try {
            await threatFusionAPI.startScan({
                target_directory: 'data/samples',
                scan_type: 'quick',
                enable_ml: true,
                enable_network: false,
            });
        } catch (error) {
            console.error('Error starting scan:', error);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <Shield className="w-16 h-16 text-emerald-500 mx-auto mb-4 animate-pulse" />
                    <p className="text-slate-400">Loading dashboard...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="p-8 space-y-8">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold mb-2">Security Dashboard</h1>
                    <p className="text-slate-400">Real-time threat monitoring and analysis</p>
                </div>

                <button
                    onClick={startQuickScan}
                    disabled={currentScan && currentScan.status === 'running'}
                    className="flex items-center gap-2 px-6 py-3 bg-emerald-500 text-slate-950 font-bold rounded-lg hover:bg-emerald-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    <Play className="w-5 h-5" />
                    Start Quick Scan
                </button>
            </div>

            {/* Active Scan Progress */}
            {currentScan && currentScan.status === 'running' && (
                <ScanProgress scan={currentScan} />
            )}

            {/* Statistics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    icon={<FileSearch className="w-6 h-6" />}
                    label="Total Scans"
                    value={statistics?.total_scans || 0}
                    change="+12%"
                    trend="up"
                    color="blue"
                />
                <StatCard
                    icon={<Activity className="w-6 h-6" />}
                    label="Files Scanned"
                    value={statistics?.total_files_scanned || 0}
                    change="+28%"
                    trend="up"
                    color="green"
                />
                <StatCard
                    icon={<AlertTriangle className="w-6 h-6" />}
                    label="Threats Detected"
                    value={statistics?.total_threats_detected || 0}
                    change="+5%"
                    trend="up"
                    color="red"
                />
                <StatCard
                    icon={<TrendingUp className="w-6 h-6" />}
                    label="Success Rate"
                    value={`${((statistics?.scan_success_rate || 0) * 100).toFixed(1)}%`}
                    change="+2%"
                    trend="up"
                    color="emerald"
                />
            </div>

            {/* Charts and Recent Activity */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Threat Distribution Chart */}
                <div className="glass rounded-xl p-6">
                    <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                        <Shield className="w-5 h-5 text-emerald-500" />
                        Threat Distribution
                    </h2>
                    <ThreatChart data={statistics?.threats_by_level} />
                </div>

                {/* Recent Threats */}
                <div className="glass rounded-xl p-6">
                    <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                        <AlertTriangle className="w-5 h-5 text-amber-500" />
                        Recent Threats
                    </h2>
                    <RecentThreats threats={recentThreats} />
                </div>
            </div>

            {/* System Status */}
            <div className="glass rounded-xl p-6">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <Terminal className="w-5 h-5 text-cyan-500" />
                    System Status
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <StatusItem label="C++ Scanner" status="operational" />
                    <StatusItem label="Go Network Analyzer" status="operational" />
                    <StatusItem label="Python ML Engine" status="operational" />
                </div>
            </div>
        </div>
    );
};

const StatusItem = ({ label, status }) => (
    <div className="flex items-center justify-between p-4 bg-slate-950/50 rounded-lg border border-slate-800">
        <span className="text-slate-300 font-medium">{label}</span>
        <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${status === 'operational' ? 'bg-emerald-500' : 'bg-rose-500'} animate-pulse`}></div>
            <span className={`text-sm font-medium ${status === 'operational' ? 'text-emerald-400' : 'text-rose-400'}`}>
                {status === 'operational' ? 'Online' : 'Offline'}
            </span>
        </div>
    </div>
);

export default Dashboard;
