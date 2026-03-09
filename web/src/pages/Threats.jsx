import { useState, useEffect } from 'react';
import { FileWarning, AlertTriangle, Search, Filter, Download, Eye, X, Shield } from 'lucide-react';
import { threatFusionAPI } from '../services/api';

const Threats = () => {
    const [threats, setThreats] = useState([]);
    const [filteredThreats, setFilteredThreats] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedLevel, setSelectedLevel] = useState('all');
    const [selectedThreat, setSelectedThreat] = useState(null);
    const [showDetails, setShowDetails] = useState(false);

    useEffect(() => {
        fetchThreats();
    }, []);

    useEffect(() => {
        filterThreats();
    }, [searchTerm, selectedLevel, threats]);

    const fetchThreats = async () => {
        try {
            const res = await threatFusionAPI.getThreats({ limit: 100 });
            setThreats(res.data.threats || []);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching threats:', error);
            setLoading(false);
        }
    };

    const filterThreats = () => {
        let filtered = threats;

        // Filter by level
        if (selectedLevel !== 'all') {
            filtered = filtered.filter(t => t.threat_level === selectedLevel);
        }

        // Filter by search term
        if (searchTerm) {
            filtered = filtered.filter(t =>
                t.filename.toLowerCase().includes(searchTerm.toLowerCase()) ||
                t.threat_type.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }

        setFilteredThreats(filtered);
    };

    const getThreatColor = (level) => {
        const colors = {
            CRITICAL: 'text-rose-400 bg-rose-500/10 border-rose-500/50',
            HIGH: 'text-amber-400 bg-amber-500/10 border-amber-500/50',
            MEDIUM: 'text-blue-400 bg-blue-500/10 border-blue-500/50',
            LOW: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/50',
        };
        return colors[level] || colors.LOW;
    };

    const getThreatIcon = (level) => {
        if (level === 'CRITICAL' || level === 'HIGH') {
            return <AlertTriangle className="w-5 h-5" />;
        }
        return <Shield className="w-5 h-5" />;
    };

    const viewThreatDetails = async (threat) => {
        setSelectedThreat(threat);
        setShowDetails(true);
    };

    const exportThreats = () => {
        const csv = [
            ['Filename', 'Threat Level', 'Threat Type', 'Detection Time'].join(','),
            ...filteredThreats.map(t =>
                [t.filename, t.threat_level, t.threat_type, t.detection_time].join(',')
            )
        ].join('\n');

        const blob = new Blob([csv], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `threats_${new Date().toISOString()}.csv`;
        a.click();
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <FileWarning className="w-16 h-16 text-amber-500 animate-pulse" />
            </div>
        );
    }

    return (
        <div className="p-8 space-y-8">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold mb-2">Threat Analysis</h1>
                    <p className="text-slate-400">Detected security threats and vulnerabilities</p>
                </div>

                <button
                    onClick={exportThreats}
                    className="flex items-center gap-2 px-6 py-3 bg-blue-500 text-white font-bold rounded-lg hover:bg-blue-400 transition-colors"
                >
                    <Download className="w-5 h-5" />
                    Export CSV
                </button>
            </div>

            {/* Statistics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                {['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].map((level) => {
                    const count = threats.filter(t => t.threat_level === level).length;
                    return (
                        <div
                            key={level}
                            className={`glass glass-hover rounded-xl p-6 cursor-pointer ${getThreatColor(level)}`}
                            onClick={() => setSelectedLevel(selectedLevel === level ? 'all' : level)}
                        >
                            <div className="flex items-center justify-between mb-2">
                                {getThreatIcon(level)}
                                <p className="text-3xl font-bold">{count}</p>
                            </div>
                            <p className="text-sm font-medium">{level} Threats</p>
                            {selectedLevel === level && (
                                <p className="text-xs mt-2 opacity-75">Click to clear filter</p>
                            )}
                        </div>
                    );
                })}
            </div>

            {/* Filters */}
            <div className="glass rounded-xl p-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Search */}
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                        <input
                            type="text"
                            placeholder="Search by filename or threat type..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="w-full pl-12 pr-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-slate-200 placeholder-slate-500 focus:border-emerald-500 focus:outline-none"
                        />
                    </div>

                    {/* Level Filter */}
                    <div className="relative">
                        <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
                        <select
                            value={selectedLevel}
                            onChange={(e) => setSelectedLevel(e.target.value)}
                            className="w-full pl-12 pr-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-slate-200 focus:border-emerald-500 focus:outline-none appearance-none"
                        >
                            <option value="all">All Threat Levels</option>
                            <option value="CRITICAL">Critical</option>
                            <option value="HIGH">High</option>
                            <option value="MEDIUM">Medium</option>
                            <option value="LOW">Low</option>
                        </select>
                    </div>
                </div>

                <div className="mt-4 flex items-center justify-between">
                    <p className="text-sm text-slate-400">
                        Showing {filteredThreats.length} of {threats.length} threats
                    </p>
                    {(searchTerm || selectedLevel !== 'all') && (
                        <button
                            onClick={() => {
                                setSearchTerm('');
                                setSelectedLevel('all');
                            }}
                            className="text-sm text-emerald-400 hover:text-emerald-300"
                        >
                            Clear filters
                        </button>
                    )}
                </div>
            </div>

            {/* Threats List */}
            <div className="glass rounded-xl p-6">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <FileWarning className="w-5 h-5 text-amber-500" />
                    Detected Threats
                </h2>

                {filteredThreats.length === 0 ? (
                    <div className="text-center py-12 text-slate-500">
                        <Shield className="w-16 h-16 mx-auto mb-4 opacity-50" />
                        <p>No threats found matching your criteria</p>
                    </div>
                ) : (
                    <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
                        {filteredThreats.map((threat) => (
                            <div
                                key={threat.id}
                                className="p-4 bg-slate-950/50 rounded-lg border border-slate-800 hover:border-emerald-500/30 transition-colors"
                            >
                                <div className="flex items-start justify-between mb-3">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-3 mb-2">
                                            {getThreatIcon(threat.threat_level)}
                                            <h3 className="font-medium text-slate-200">{threat.filename}</h3>
                                        </div>
                                        <p className="text-sm text-slate-400 mb-2">{threat.threat_type}</p>

                                        {threat.details && (
                                            <div className="space-y-1">
                                                {threat.details.entropy && (
                                                    <p className="text-xs text-slate-500">
                                                        Entropy: <span className="text-amber-400 font-mono">{threat.details.entropy}</span>
                                                    </p>
                                                )}
                                                {threat.details.packed && (
                                                    <p className="text-xs text-rose-400">⚠️ Packed executable detected</p>
                                                )}
                                                {threat.details.suspicious_strings && threat.details.suspicious_strings.length > 0 && (
                                                    <div className="mt-2">
                                                        <p className="text-xs text-slate-500 mb-1">Suspicious strings:</p>
                                                        <div className="flex flex-wrap gap-1">
                                                            {threat.details.suspicious_strings.slice(0, 3).map((str, idx) => (
                                                                <span
                                                                    key={idx}
                                                                    className="px-2 py-1 bg-slate-900 text-amber-400 rounded text-xs font-mono"
                                                                >
                                                                    {str}
                                                                </span>
                                                            ))}
                                                            {threat.details.suspicious_strings.length > 3 && (
                                                                <span className="px-2 py-1 text-slate-500 text-xs">
                                                                    +{threat.details.suspicious_strings.length - 3} more
                                                                </span>
                                                            )}
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                        )}

                                        <p className="text-xs text-slate-600 mt-2">
                                            Detected: {new Date(threat.detection_time).toLocaleString()}
                                        </p>
                                    </div>

                                    <div className="flex gap-2 ml-4">
                                        <span className={`px-3 py-1 rounded-lg text-sm font-medium border ${getThreatColor(threat.threat_level)}`}>
                                            {threat.threat_level}
                                        </span>
                                        <button
                                            onClick={() => viewThreatDetails(threat)}
                                            className="p-2 bg-slate-800 border border-slate-700 rounded-lg hover:border-emerald-500 transition-colors"
                                        >
                                            <Eye className="w-5 h-5 text-slate-400" />
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Threat Details Modal */}
            {showDetails && selectedThreat && (
                <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
                    <div className="glass rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6">
                        <div className="flex items-center justify-between mb-6">
                            <h2 className="text-2xl font-bold flex items-center gap-3">
                                {getThreatIcon(selectedThreat.threat_level)}
                                Threat Details
                            </h2>
                            <button
                                onClick={() => setShowDetails(false)}
                                className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
                            >
                                <X className="w-6 h-6" />
                            </button>
                        </div>

                        <div className="space-y-6">
                            {/* Basic Info */}
                            <div>
                                <h3 className="text-sm font-semibold text-slate-400 uppercase mb-3">Basic Information</h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="p-4 bg-slate-950/50 rounded-lg">
                                        <p className="text-xs text-slate-500 mb-1">Filename</p>
                                        <p className="font-medium text-slate-200">{selectedThreat.filename}</p>
                                    </div>
                                    <div className="p-4 bg-slate-950/50 rounded-lg">
                                        <p className="text-xs text-slate-500 mb-1">Threat Level</p>
                                        <span className={`inline-block px-3 py-1 rounded-lg text-sm font-medium border ${getThreatColor(selectedThreat.threat_level)}`}>
                                            {selectedThreat.threat_level}
                                        </span>
                                    </div>
                                    <div className="p-4 bg-slate-950/50 rounded-lg col-span-2">
                                        <p className="text-xs text-slate-500 mb-1">Threat Type</p>
                                        <p className="font-medium text-slate-200">{selectedThreat.threat_type}</p>
                                    </div>
                                    <div className="p-4 bg-slate-950/50 rounded-lg col-span-2">
                                        <p className="text-xs text-slate-500 mb-1">Detection Time</p>
                                        <p className="font-medium text-slate-200">
                                            {new Date(selectedThreat.detection_time).toLocaleString()}
                                        </p>
                                    </div>
                                </div>
                            </div>

                            {/* Technical Details */}
                            {selectedThreat.details && (
                                <div>
                                    <h3 className="text-sm font-semibold text-slate-400 uppercase mb-3">Technical Analysis</h3>
                                    <div className="space-y-3">
                                        {selectedThreat.details.entropy && (
                                            <div className="p-4 bg-slate-950/50 rounded-lg">
                                                <p className="text-xs text-slate-500 mb-1">Entropy Score</p>
                                                <p className="font-mono text-lg text-amber-400">{selectedThreat.details.entropy}</p>
                                                <p className="text-xs text-slate-600 mt-1">
                                                    {selectedThreat.details.entropy > 7.0 ? 'High entropy detected (possibly packed/encrypted)' : 'Normal entropy range'}
                                                </p>
                                            </div>
                                        )}

                                        {selectedThreat.details.packed !== undefined && (
                                            <div className="p-4 bg-slate-950/50 rounded-lg">
                                                <p className="text-xs text-slate-500 mb-1">Packer Detection</p>
                                                <p className={selectedThreat.details.packed ? 'text-rose-400' : 'text-emerald-400'}>
                                                    {selectedThreat.details.packed ? '⚠️ Packed executable detected' : '✓ No packer detected'}
                                                </p>
                                            </div>
                                        )}

                                        {selectedThreat.details.suspicious_strings && selectedThreat.details.suspicious_strings.length > 0 && (
                                            <div className="p-4 bg-slate-950/50 rounded-lg">
                                                <p className="text-xs text-slate-500 mb-2">Suspicious API Calls / Strings</p>
                                                <div className="flex flex-wrap gap-2">
                                                    {selectedThreat.details.suspicious_strings.map((str, idx) => (
                                                        <span
                                                            key={idx}
                                                            className="px-3 py-1 bg-slate-900 text-amber-400 rounded text-sm font-mono"
                                                        >
                                                            {str}
                                                        </span>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}

                            {/* Recommendations */}
                            <div>
                                <h3 className="text-sm font-semibold text-slate-400 uppercase mb-3">Recommendations</h3>
                                <div className="p-4 bg-amber-500/10 border border-amber-500/50 rounded-lg">
                                    <ul className="space-y-2 text-sm text-slate-300">
                                        <li className="flex items-start gap-2">
                                            <span className="text-amber-400">•</span>
                                            <span>Quarantine this file immediately</span>
                                        </li>
                                        <li className="flex items-start gap-2">
                                            <span className="text-amber-400">•</span>
                                            <span>Run additional scans with updated signatures</span>
                                        </li>
                                        <li className="flex items-start gap-2">
                                            <span className="text-amber-400">•</span>
                                            <span>Review system logs for suspicious activity</span>
                                        </li>
                                        <li className="flex items-start gap-2">
                                            <span className="text-amber-400">•</span>
                                            <span>Consider submitting to VirusTotal for analysis</span>
                                        </li>
                                    </ul>
                                </div>
                            </div>

                            {/* Actions */}
                            <div className="flex gap-3">
                                <button className="flex-1 px-6 py-3 bg-rose-500 text-white font-bold rounded-lg hover:bg-rose-400 transition-colors">
                                    Quarantine File
                                </button>
                                <button className="flex-1 px-6 py-3 bg-slate-800 text-slate-300 font-bold rounded-lg hover:bg-slate-700 transition-colors">
                                    Generate Report
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Threats;
