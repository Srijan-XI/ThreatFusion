import { useState, useEffect } from 'react';
import { FileText, Download, Eye, FileJson, FileSpreadsheet, File, Calendar, HardDrive, RefreshCw } from 'lucide-react';
import { threatFusionAPI } from '../services/api';

const Reports = () => {
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filterType, setFilterType] = useState('all');

    useEffect(() => {
        fetchReports();
    }, []);

    const fetchReports = async () => {
        try {
            const res = await threatFusionAPI.listReports();
            setReports(res.data.reports || []);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching reports:', error);
            setLoading(false);
        }
    };

    const getReportIcon = (type) => {
        const icons = {
            html: <FileText className="w-6 h-6 text-orange-400" />,
            pdf: <File className="w-6 h-6 text-rose-400" />,
            xlsx: <FileSpreadsheet className="w-6 h-6 text-emerald-400" />,
            csv: <FileJson className="w-6 h-6 text-blue-400" />,
            json: <FileJson className="w-6 h-6 text-purple-400" />,
        };
        return icons[type] || <FileText className="w-6 h-6 text-slate-400" />;
    };

    const getReportColor = (type) => {
        const colors = {
            html: 'border-orange-500/50 bg-orange-500/10',
            pdf: 'border-rose-500/50 bg-rose-500/10',
            xlsx: 'border-emerald-500/50 bg-emerald-500/10',
            csv: 'border-blue-500/50 bg-blue-500/10',
            json: 'border-purple-500/50 bg-purple-500/10',
        };
        return colors[type] || 'border-slate-500/50 bg-slate-500/10';
    };

    const formatFileSize = (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
    };

    const filteredReports = filterType === 'all'
        ? reports
        : reports.filter(r => r.type === filterType);

    const reportTypes = [...new Set(reports.map(r => r.type))];
    const totalSize = reports.reduce((sum, r) => sum + r.size, 0);

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <FileText className="w-16 h-16 text-blue-500 animate-pulse" />
            </div>
        );
    }

    return (
        <div className="p-8 space-y-8">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold mb-2">Reports</h1>
                    <p className="text-slate-400">Generated security analysis reports</p>
                </div>

                <button
                    onClick={fetchReports}
                    className="flex items-center gap-2 px-6 py-3 bg-blue-500 text-white font-bold rounded-lg hover:bg-blue-400 transition-colors"
                >
                    <RefreshCw className="w-5 h-5" />
                    Refresh
                </button>
            </div>

            {/* Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="glass glass-hover rounded-xl p-6 border-blue-500/30">
                    <div className="flex items-center justify-between mb-2">
                        <FileText className="w-6 h-6 text-blue-400" />
                        <p className="text-3xl font-bold text-blue-400">{reports.length}</p>
                    </div>
                    <p className="text-sm font-medium text-slate-300">Total Reports</p>
                </div>

                <div className="glass glass-hover rounded-xl p-6 border-emerald-500/30">
                    <div className="flex items-center justify-between mb-2">
                        <HardDrive className="w-6 h-6 text-emerald-400" />
                        <p className="text-3xl font-bold text-emerald-400">{formatFileSize(totalSize)}</p>
                    </div>
                    <p className="text-sm font-medium text-slate-300">Total Size</p>
                </div>

                <div className="glass glass-hover rounded-xl p-6 border-purple-500/30">
                    <div className="flex items-center justify-between mb-2">
                        <FileJson className="w-6 h-6 text-purple-400" />
                        <p className="text-3xl font-bold text-purple-400">{reportTypes.length}</p>
                    </div>
                    <p className="text-sm font-medium text-slate-300">Report Types</p>
                </div>

                <div className="glass glass-hover rounded-xl p-6 border-amber-500/30">
                    <div className="flex items-center justify-between mb-2">
                        <Calendar className="w-6 h-6 text-amber-400" />
                        <p className="text-3xl font-bold text-amber-400">
                            {reports.length > 0 ? new Date(reports[0].created).toLocaleDateString() : 'N/A'}
                        </p>
                    </div>
                    <p className="text-sm font-medium text-slate-300">Latest Report</p>
                </div>
            </div>

            {/* Filters */}
            <div className="glass rounded-xl p-6">
                <div className="flex items-center gap-4">
                    <p className="text-sm font-medium text-slate-400">Filter by type:</p>
                    <div className="flex gap-2 flex-wrap">
                        <button
                            onClick={() => setFilterType('all')}
                            className={`px-4 py-2 rounded-lg font-medium text-sm transition-all ${filterType === 'all'
                                    ? 'bg-emerald-500 text-slate-950'
                                    : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                                }`}
                        >
                            All ({reports.length})
                        </button>
                        {reportTypes.map((type) => (
                            <button
                                key={type}
                                onClick={() => setFilterType(type)}
                                className={`px-4 py-2 rounded-lg font-medium text-sm transition-all uppercase ${filterType === type
                                        ? 'bg-emerald-500 text-slate-950'
                                        : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                                    }`}
                            >
                                {type} ({reports.filter(r => r.type === type).length})
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            {/* Reports Grid */}
            <div className="glass rounded-xl p-6">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <FileText className="w-5 h-5 text-blue-500" />
                    Available Reports
                </h2>

                {filteredReports.length === 0 ? (
                    <div className="text-center py-12 text-slate-500">
                        <FileText className="w-16 h-16 mx-auto mb-4 opacity-50" />
                        <p>No reports generated yet</p>
                        <p className="text-sm mt-2">Run a scan to generate reports</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {filteredReports.map((report, idx) => (
                            <div
                                key={idx}
                                className={`p-6 rounded-xl border-2 ${getReportColor(report.type)} hover:shadow-lg transition-all`}
                            >
                                {/* Report Icon & Type */}
                                <div className="flex items-center justify-between mb-4">
                                    {getReportIcon(report.type)}
                                    <span className="px-3 py-1 bg-slate-950/50 rounded-lg text-xs font-mono uppercase text-slate-300">
                                        {report.type}
                                    </span>
                                </div>

                                {/* Report Name */}
                                <h3 className="font-medium text-slate-200 mb-2 truncate" title={report.filename}>
                                    {report.filename}
                                </h3>

                                {/* Report Details */}
                                <div className="space-y-2 mb-4">
                                    <div className="flex items-center justify-between text-xs">
                                        <span className="text-slate-500">Size:</span>
                                        <span className="text-slate-300 font-medium">{formatFileSize(report.size)}</span>
                                    </div>
                                    <div className="flex items-center justify-between text-xs">
                                        <span className="text-slate-500">Created:</span>
                                        <span className="text-slate-300 font-medium">
                                            {new Date(report.created).toLocaleDateString()}
                                        </span>
                                    </div>
                                    <div className="flex items-center justify-between text-xs">
                                        <span className="text-slate-500">Time:</span>
                                        <span className="text-slate-300 font-medium">
                                            {new Date(report.created).toLocaleTimeString()}
                                        </span>
                                    </div>
                                </div>

                                {/* Actions */}
                                <div className="flex gap-2">
                                    {report.type === 'html' && (
                                        <button className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-slate-950/50 border border-slate-700 rounded-lg hover:border-emerald-500 transition-colors text-sm font-medium">
                                            <Eye className="w-4 h-4" />
                                            Preview
                                        </button>
                                    )}
                                    <button className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-emerald-500 text-slate-950 rounded-lg hover:bg-emerald-400 transition-colors text-sm font-medium">
                                        <Download className="w-4 h-4" />
                                        Download
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Report Generation Options */}
            <div className="glass rounded-xl p-6">
                <h2 className="text-xl font-bold mb-4">Generate New Report</h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Report Type Selection */}
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-3">
                            Report Format
                        </label>
                        <div className="space-y-2">
                            {[
                                { type: 'html', name: 'HTML Dashboard', desc: 'Interactive web-based report' },
                                { type: 'pdf', name: 'PDF Report', desc: 'Executive summary for management' },
                                { type: 'xlsx', name: 'Excel Workbook', desc: 'Detailed data analysis' },
                                { type: 'csv', name: 'CSV Export', desc: 'Simple threat list' },
                            ].map((format) => (
                                <label
                                    key={format.type}
                                    className="flex items-center gap-3 p-3 bg-slate-950/50 rounded-lg border border-slate-800 hover:border-emerald-500/30 transition-colors cursor-pointer"
                                >
                                    <input
                                        type="radio"
                                        name="report-format"
                                        className="w-4 h-4 text-emerald-500 focus:ring-emerald-500"
                                    />
                                    <div className="flex-1">
                                        <p className="font-medium text-slate-200">{format.name}</p>
                                        <p className="text-xs text-slate-500">{format.desc}</p>
                                    </div>
                                    {getReportIcon(format.type)}
                                </label>
                            ))}
                        </div>
                    </div>

                    {/* Report Options */}
                    <div>
                        <label className="block text-sm font-medium text-slate-300 mb-3">
                            Report Options
                        </label>
                        <div className="space-y-3">
                            <label className="flex items-center gap-3 p-3 bg-slate-950/50 rounded-lg border border-slate-800 hover:border-emerald-500/30 transition-colors cursor-pointer">
                                <input
                                    type="checkbox"
                                    defaultChecked
                                    className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                                />
                                <div className="flex-1">
                                    <p className="font-medium text-slate-200">Include Executive Summary</p>
                                    <p className="text-xs text-slate-500">High-level overview for management</p>
                                </div>
                            </label>

                            <label className="flex items-center gap-3 p-3 bg-slate-950/50 rounded-lg border border-slate-800 hover:border-emerald-500/30 transition-colors cursor-pointer">
                                <input
                                    type="checkbox"
                                    defaultChecked
                                    className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                                />
                                <div className="flex-1">
                                    <p className="font-medium text-slate-200">Include Detailed Findings</p>
                                    <p className="text-xs text-slate-500">Complete threat analysis</p>
                                </div>
                            </label>

                            <label className="flex items-center gap-3 p-3 bg-slate-950/50 rounded-lg border border-slate-800 hover:border-emerald-500/30 transition-colors cursor-pointer">
                                <input
                                    type="checkbox"
                                    className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                                />
                                <div className="flex-1">
                                    <p className="font-medium text-slate-200">Include Charts & Visualizations</p>
                                    <p className="text-xs text-slate-500">Graphs and statistics</p>
                                </div>
                            </label>

                            <label className="flex items-center gap-3 p-3 bg-slate-950/50 rounded-lg border border-slate-800 hover:border-emerald-500/30 transition-colors cursor-pointer">
                                <input
                                    type="checkbox"
                                    className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                                />
                                <div className="flex-1">
                                    <p className="font-medium text-slate-200">Include Recommendations</p>
                                    <p className="text-xs text-slate-500">Security improvement suggestions</p>
                                </div>
                            </label>
                        </div>

                        <button className="w-full mt-6 px-6 py-3 bg-emerald-500 text-slate-950 font-bold rounded-lg hover:bg-emerald-400 transition-colors">
                            Generate Report
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Reports;
