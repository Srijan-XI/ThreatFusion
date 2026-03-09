import { useState, useEffect } from 'react';
import { Scan, Play, Pause, Clock, CheckCircle, XCircle, Settings as SettingsIcon, FolderOpen, Upload } from 'lucide-react';
import { threatFusionAPI } from '../services/api';

const Scans = () => {
    const [scanHistory, setScanHistory] = useState([]);
    const [currentScan, setCurrentScan] = useState(null);
    const [loading, setLoading] = useState(true);
    const [showNewScan, setShowNewScan] = useState(false);
    const [scanConfig, setScanConfig] = useState({
        target_directory: 'data/samples',
        scan_type: 'full',
        enable_ml: true,
        enable_network: true,
    });
    const [selectedFiles, setSelectedFiles] = useState([]);

    useEffect(() => {
        fetchScans();
    }, []);

    const fetchScans = async () => {
        try {
            const [historyRes, currentRes] = await Promise.all([
                threatFusionAPI.getScanHistory(),
                threatFusionAPI.getCurrentScan(),
            ]);
            setScanHistory(historyRes.data.scans || []);
            setCurrentScan(currentRes.data.status !== 'idle' ? currentRes.data : null);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching scans:', error);
            setLoading(false);
        }
    };

    const handleStartScan = async () => {
        try {
            await threatFusionAPI.startScan(scanConfig);
            setShowNewScan(false);
            setTimeout(fetchScans, 1000);
        } catch (error) {
            console.error('Error starting scan:', error);
        }
    };

    const handleFileSelect = (event) => {
        const files = Array.from(event.target.files);
        setSelectedFiles(files);
    };

    const getScanStatusColor = (status) => {
        const colors = {
            completed: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/50',
            running: 'text-blue-400 bg-blue-500/10 border-blue-500/50 animate-pulse',
            failed: 'text-rose-400 bg-rose-500/10 border-rose-500/50',
            idle: 'text-slate-400 bg-slate-500/10 border-slate-500/50',
        };
        return colors[status] || colors.idle;
    };

    const getScanIcon = (status) => {
        const icons = {
            completed: <CheckCircle className="w-5 h-5" />,
            running: <Play className="w-5 h-5" />,
            failed: <XCircle className="w-5 h-5" />,
        };
        return icons[status] || <Clock className="w-5 h-5" />;
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <Scan className="w-16 h-16 text-emerald-500 animate-pulse" />
            </div>
        );
    }

    return (
        <div className="p-8 space-y-8">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold mb-2">Scan Management</h1>
                    <p className="text-slate-400">Configure and manage security scans</p>
                </div>

                <button
                    onClick={() => setShowNewScan(!showNewScan)}
                    disabled={currentScan && currentScan.status === 'running'}
                    className="flex items-center gap-2 px-6 py-3 bg-emerald-500 text-slate-950 font-bold rounded-lg hover:bg-emerald-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    <Play className="w-5 h-5" />
                    New Scan
                </button>
            </div>

            {/* New Scan Configuration */}
            {showNewScan && (
                <div className="glass rounded-xl p-6 border-emerald-500/30 animate-in">
                    <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                        <SettingsIcon className="w-5 h-5 text-emerald-500" />
                        Scan Configuration
                    </h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Left Column */}
                        <div className="space-y-4">
                            {/* Scan Type */}
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                    Scan Type
                                </label>
                                <select
                                    value={scanConfig.scan_type}
                                    onChange={(e) => setScanConfig({ ...scanConfig, scan_type: e.target.value })}
                                    className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-slate-200 focus:border-emerald-500 focus:outline-none"
                                >
                                    <option value="quick">Quick Scan</option>
                                    <option value="full">Full Scan</option>
                                    <option value="custom">Custom Scan</option>
                                </select>
                            </div>

                            {/* Target Directory */}
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                    Target Directory
                                </label>
                                <div className="flex gap-2">
                                    <input
                                        type="text"
                                        value={scanConfig.target_directory}
                                        onChange={(e) => setScanConfig({ ...scanConfig, target_directory: e.target.value })}
                                        className="flex-1 px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-slate-200 focus:border-emerald-500 focus:outline-none"
                                        placeholder="data/samples"
                                    />
                                    <button className="px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg hover:border-emerald-500 transition-colors">
                                        <FolderOpen className="w-5 h-5 text-slate-400" />
                                    </button>
                                </div>
                            </div>

                            {/* File Upload */}
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                    Upload Files (Optional)
                                </label>
                                <div className="border-2 border-dashed border-slate-700 rounded-lg p-6 text-center hover:border-emerald-500 transition-colors cursor-pointer">
                                    <input
                                        type="file"
                                        multiple
                                        onChange={handleFileSelect}
                                        className="hidden"
                                        id="file-upload"
                                    />
                                    <label htmlFor="file-upload" className="cursor-pointer">
                                        <Upload className="w-8 h-8 text-slate-500 mx-auto mb-2" />
                                        <p className="text-sm text-slate-400">
                                            Click to upload or drag and drop
                                        </p>
                                        <p className="text-xs text-slate-600 mt-1">
                                            Executable files, scripts, archives
                                        </p>
                                    </label>
                                    {selectedFiles.length > 0 && (
                                        <div className="mt-4 text-left">
                                            <p className="text-sm text-emerald-400 mb-2">
                                                {selectedFiles.length} file(s) selected:
                                            </p>
                                            <div className="space-y-1 max-h-32 overflow-y-auto">
                                                {selectedFiles.map((file, idx) => (
                                                    <p key={idx} className="text-xs text-slate-500">
                                                        • {file.name} ({(file.size / 1024).toFixed(1)} KB)
                                                    </p>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* Right Column */}
                        <div className="space-y-4">
                            {/* Scan Options */}
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-3">
                                    Scan Options
                                </label>
                                <div className="space-y-3">
                                    <label className="flex items-center gap-3 p-3 bg-slate-950/50 rounded-lg border border-slate-800 hover:border-emerald-500/30 transition-colors cursor-pointer">
                                        <input
                                            type="checkbox"
                                            checked={scanConfig.enable_ml}
                                            onChange={(e) => setScanConfig({ ...scanConfig, enable_ml: e.target.checked })}
                                            className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                                        />
                                        <div className="flex-1">
                                            <p className="font-medium text-slate-200">Machine Learning Analysis</p>
                                            <p className="text-xs text-slate-500">Use ML models for anomaly detection</p>
                                        </div>
                                    </label>

                                    <label className="flex items-center gap-3 p-3 bg-slate-950/50 rounded-lg border border-slate-800 hover:border-emerald-500/30 transition-colors cursor-pointer">
                                        <input
                                            type="checkbox"
                                            checked={scanConfig.enable_network}
                                            onChange={(e) => setScanConfig({ ...scanConfig, enable_network: e.target.checked })}
                                            className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                                        />
                                        <div className="flex-1">
                                            <p className="font-medium text-slate-200">Network Analysis</p>
                                            <p className="text-xs text-slate-500">Scan for network threats and connections</p>
                                        </div>
                                    </label>

                                    <label className="flex items-center gap-3 p-3 bg-slate-950/50 rounded-lg border border-slate-800 hover:border-emerald-500/30 transition-colors cursor-pointer">
                                        <input
                                            type="checkbox"
                                            defaultChecked
                                            className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                                        />
                                        <div className="flex-1">
                                            <p className="font-medium text-slate-200">Deep File Analysis</p>
                                            <p className="text-xs text-slate-500">PE/ELF parsing and entropy analysis</p>
                                        </div>
                                    </label>

                                    <label className="flex items-center gap-3 p-3 bg-slate-950/50 rounded-lg border border-slate-800 hover:border-emerald-500/30 transition-colors cursor-pointer">
                                        <input
                                            type="checkbox"
                                            defaultChecked
                                            className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                                        />
                                        <div className="flex-1">
                                            <p className="font-medium text-slate-200">Generate Reports</p>
                                            <p className="text-xs text-slate-500">Create HTML, PDF, and Excel reports</p>
                                        </div>
                                    </label>
                                </div>
                            </div>

                            {/* Action Buttons */}
                            <div className="flex gap-3 pt-4">
                                <button
                                    onClick={handleStartScan}
                                    className="flex-1 px-6 py-3 bg-emerald-500 text-slate-950 font-bold rounded-lg hover:bg-emerald-400 transition-colors"
                                >
                                    Start Scan
                                </button>
                                <button
                                    onClick={() => setShowNewScan(false)}
                                    className="flex-1 px-6 py-3 bg-slate-800 text-slate-300 font-bold rounded-lg hover:bg-slate-700 transition-colors"
                                >
                                    Cancel
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Current Scan */}
            {currentScan && currentScan.status === 'running' && (
                <div className="glass rounded-xl p-6 border-2 border-emerald-500/30 animate-glow">
                    <div className="flex items-center justify-between mb-4">
                        <h2 className="text-xl font-bold flex items-center gap-2">
                            <Play className="w-5 h-5 text-emerald-500 animate-pulse" />
                            Active Scan
                        </h2>
                        <span className={`px-3 py-1 rounded-lg text-sm font-medium border ${getScanStatusColor(currentScan.status)}`}>
                            {currentScan.status.toUpperCase()}
                        </span>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                        <div className="p-4 bg-slate-950/50 rounded-lg">
                            <p className="text-sm text-slate-500 mb-1">Scan ID</p>
                            <p className="font-mono text-sm text-slate-300">{currentScan.scan_id}</p>
                        </div>
                        <div className="p-4 bg-slate-950/50 rounded-lg">
                            <p className="text-sm text-slate-500 mb-1">Files Scanned</p>
                            <p className="text-2xl font-bold text-emerald-400">{currentScan.files_scanned}</p>
                        </div>
                        <div className="p-4 bg-slate-950/50 rounded-lg">
                            <p className="text-sm text-slate-500 mb-1">Threats Detected</p>
                            <p className="text-2xl font-bold text-amber-400">{currentScan.threats_detected}</p>
                        </div>
                    </div>

                    {/* Progress Bar */}
                    <div className="relative w-full h-3 bg-slate-900 rounded-full overflow-hidden">
                        <div
                            className="absolute top-0 left-0 h-full bg-gradient-to-r from-emerald-500 to-cyan-500 transition-all duration-500"
                            style={{ width: `${((currentScan.files_scanned / 100) * 100)}%` }}
                        >
                            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse"></div>
                        </div>
                    </div>

                    <p className="text-sm text-slate-500 mt-2">
                        Started: {new Date(currentScan.start_time).toLocaleString()}
                    </p>
                </div>
            )}

            {/* Scan History */}
            <div className="glass rounded-xl p-6">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <Clock className="w-5 h-5 text-blue-500" />
                    Scan History
                </h2>

                {scanHistory.length === 0 ? (
                    <div className="text-center py-12 text-slate-500">
                        <Scan className="w-16 h-16 mx-auto mb-4 opacity-50" />
                        <p>No scans performed yet</p>
                    </div>
                ) : (
                    <div className="space-y-3">
                        {scanHistory.map((scan, idx) => (
                            <div
                                key={idx}
                                className="p-4 bg-slate-950/50 rounded-lg border border-slate-800 hover:border-emerald-500/30 transition-colors"
                            >
                                <div className="flex items-center justify-between mb-3">
                                    <div className="flex items-center gap-3">
                                        {getScanIcon(scan.status)}
                                        <div>
                                            <p className="font-medium text-slate-200">{scan.scan_id}</p>
                                            <p className="text-xs text-slate-500">
                                                {new Date(scan.start_time).toLocaleString()}
                                            </p>
                                        </div>
                                    </div>
                                    <span className={`px-3 py-1 rounded-lg text-xs font-medium border ${getScanStatusColor(scan.status)}`}>
                                        {scan.status.toUpperCase()}
                                    </span>
                                </div>

                                <div className="grid grid-cols-3 gap-4 text-sm">
                                    <div>
                                        <p className="text-slate-500">Files Scanned</p>
                                        <p className="font-bold text-slate-200">{scan.files_scanned}</p>
                                    </div>
                                    <div>
                                        <p className="text-slate-500">Threats Found</p>
                                        <p className="font-bold text-amber-400">{scan.threats_detected}</p>
                                    </div>
                                    <div>
                                        <p className="text-slate-500">Duration</p>
                                        <p className="font-bold text-slate-200">
                                            {scan.end_time
                                                ? `${((new Date(scan.end_time) - new Date(scan.start_time)) / 1000).toFixed(0)}s`
                                                : 'In progress'}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Scans;
