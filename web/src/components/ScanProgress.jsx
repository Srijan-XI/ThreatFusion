import { Activity, FileSearch } from 'lucide-react';

const ScanProgress = ({ scan }) => {
    const progress = scan ? ((scan.files_scanned / 100) * 100).toFixed(0) : 0;

    return (
        <div className="glass rounded-xl p-6 border-2 border-emerald-500/30 animate-glow">
            <div className="flex items-center justify-between mb-4">
                <div>
                    <h3 className="text-lg font-bold flex items-center gap-2">
                        <Activity className="w-5 h-5 text-emerald-500 animate-pulse" />
                        Scan In Progress
                    </h3>
                    <p className="text-sm text-slate-400 mt-1">Scan ID: {scan?.scan_id}</p>
                </div>
                <div className="flex items-center gap-4">
                    <div className="text-right">
                        <p className="text-2xl font-bold text-emerald-400">{scan?.files_scanned || 0}</p>
                        <p className="text-xs text-slate-500">Files Scanned</p>
                    </div>
                    <div className="text-right">
                        <p className="text-2xl font-bold text-amber-400">{scan?.threats_detected || 0}</p>
                        <p className="text-xs text-slate-500">Threats Found</p>
                    </div>
                </div>
            </div>

            {/* Progress Bar */}
            <div className="relative w-full h-3 bg-slate-900 rounded-full overflow-hidden">
                <div
                    className="absolute top-0 left-0 h-full bg-gradient-to-r from-emerald-500 to-cyan-500 transition-all duration-500 rounded-full"
                    style={{ width: `${progress}%` }}
                >
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse"></div>
                </div>
            </div>

            <div className="flex items-center justify-between mt-2 text-sm text-slate-400">
                <span>Progress: {progress}%</span>
                <span>Started: {scan ? new Date(scan.start_time).toLocaleTimeString() : 'N/A'}</span>
            </div>
        </div>
    );
};

export default ScanProgress;
