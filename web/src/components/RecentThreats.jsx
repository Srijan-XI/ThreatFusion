import { AlertTriangle, Clock } from 'lucide-react';

const RecentThreats = ({ threats }) => {
    const getThreatColor = (level) => {
        const colors = {
            CRITICAL: 'text-rose-400 bg-rose-500/10 border-rose-500/50',
            HIGH: 'text-amber-400 bg-amber-500/10 border-amber-500/50',
            MEDIUM: 'text-blue-400 bg-blue-500/10 border-blue-500/50',
            LOW: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/50',
        };
        return colors[level] || colors.LOW;
    };

    if (!threats || threats.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center h-48 text-slate-500">
                <AlertTriangle className="w-12 h-12 mb-2 opacity-50" />
                <p>No threats detected</p>
            </div>
        );
    }

    return (
        <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
            {threats.map((threat, index) => (
                <div
                    key={threat.id || index}
                    className="p-4 bg-slate-950/50 rounded-lg border border-slate-800 hover:border-emerald-500/30 transition-colors"
                >
                    <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                            <h4 className="font-medium text-slate-200 mb-1">{threat.filename}</h4>
                            <p className="text-sm text-slate-400">{threat.threat_type}</p>
                        </div>
                        <span className={`px-2 py-1 rounded text-xs font-medium border ${getThreatColor(threat.threat_level)}`}>
                            {threat.threat_level}
                        </span>
                    </div>

                    {threat.details && threat.details.suspicious_strings && (
                        <div className="mt-2 text-xs text-slate-500">
                            Suspicious: {threat.details.suspicious_strings.join(', ')}
                        </div>
                    )}

                    <div className="flex items-center gap-2 mt-2 text-xs text-slate-500">
                        <Clock className="w-3 h-3" />
                        {new Date(threat.detection_time).toLocaleString()}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default RecentThreats;
