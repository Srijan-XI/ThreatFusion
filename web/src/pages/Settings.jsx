import { useState } from 'react';
import { Settings as SettingsIcon, Shield, Bell, Database, Zap, Save, RefreshCw, Key, Users, Lock } from 'lucide-react';

const Settings = () => {
    const [settings, setSettings] = useState({
        // Scanner Settings
        scanner: {
            enableCppScanner: true,
            enableGoAnalyzer: true,
            enablePythonAnalyzer: true,
            enableMLDetection: true,
            enableNetworkAnalysis: true,
            deepScanEnabled: true,
            entropyThreshold: 7.0,
            autoQuarantine: false,
        },
        // Notification Settings
        notifications: {
            enableEmailAlerts: false,
            enableDiscordWebhook: false,
            enableTelegramBot: false,
            emailAddress: '',
            discordWebhookUrl: '',
            telegramBotToken: '',
            telegramChatId: '',
            alertOnCritical: true,
            alertOnHigh: true,
            alertOnMedium: false,
            alertOnLow: false,
        },
        // API Settings
        api: {
            virusTotalApiKey: '',
            abuseIPDBApiKey: '',
            enableThreatIntel: true,
            apiRateLimit: 100,
        },
        // Database Settings
        database: {
            type: 'sqlite',
            host: 'localhost',
            port: 5432,
            name: 'threatfusion',
            retentionDays: 90,
        },
        // System Settings
        system: {
            maxScanThreads: 4,
            maxMemoryUsage: 2048,
            logLevel: 'info',
            enableAutoUpdates: true,
            darkMode: true,
        },
    });

    const [savedMessage, setSavedMessage] = useState('');

    const handleSave = () => {
        // Save settings logic here
        console.log('Saving settings:', settings);
        setSavedMessage('Settings saved successfully!');
        setTimeout(() => setSavedMessage(''), 3000);
    };

    const handleReset = () => {
        if (confirm('Are you sure you want to reset all settings to default?')) {
            // Reset logic here
            setSavedMessage('Settings reset to default!');
            setTimeout(() => setSavedMessage(''), 3000);
        }
    };

    const updateSetting = (category, key, value) => {
        setSettings({
            ...settings,
            [category]: {
                ...settings[category],
                [key]: value,
            },
        });
    };

    return (
        <div className="p-8 space-y-8">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold mb-2">Settings</h1>
                    <p className="text-slate-400">Configure ThreatFusion platform settings</p>
                </div>

                <div className="flex gap-3">
                    <button
                        onClick={handleReset}
                        className="flex items-center gap-2 px-6 py-3 bg-slate-800 text-slate-300 font-bold rounded-lg hover:bg-slate-700 transition-colors"
                    >
                        <RefreshCw className="w-5 h-5" />
                        Reset to Default
                    </button>
                    <button
                        onClick={handleSave}
                        className="flex items-center gap-2 px-6 py-3 bg-emerald-500 text-slate-950 font-bold rounded-lg hover:bg-emerald-400 transition-colors"
                    >
                        <Save className="w-5 h-5" />
                        Save Changes
                    </button>
                </div>
            </div>

            {/* Save Message */}
            {savedMessage && (
                <div className="glass rounded-xl p-4 border-emerald-500/50 bg-emerald-500/10 animate-in">
                    <p className="text-emerald-400 font-medium text-center">{savedMessage}</p>
                </div>
            )}

            {/* Scanner Settings */}
            <div className="glass rounded-xl p-6">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <Shield className="w-5 h-5 text-emerald-500" />
                    Scanner Configuration
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Left Column */}
                    <div className="space-y-4">
                        <h3 className="text-sm font-semibold text-slate-400 uppercase">Scanner Components</h3>

                        <label className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                            <div>
                                <p className="font-medium text-slate-200">C++ Scanner</p>
                                <p className="text-xs text-slate-500">High-performance file scanning</p>
                            </div>
                            <input
                                type="checkbox"
                                checked={settings.scanner.enableCppScanner}
                                onChange={(e) => updateSetting('scanner', 'enableCppScanner', e.target.checked)}
                                className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                            />
                        </label>

                        <label className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                            <div>
                                <p className="font-medium text-slate-200">Go Network Analyzer</p>
                                <p className="text-xs text-slate-500">Concurrent network analysis</p>
                            </div>
                            <input
                                type="checkbox"
                                checked={settings.scanner.enableGoAnalyzer}
                                onChange={(e) => updateSetting('scanner', 'enableGoAnalyzer', e.target.checked)}
                                className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                            />
                        </label>

                        <label className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                            <div>
                                <p className="font-medium text-slate-200">Python Log Analyzer</p>
                                <p className="text-xs text-slate-500">Heuristic log analysis</p>
                            </div>
                            <input
                                type="checkbox"
                                checked={settings.scanner.enablePythonAnalyzer}
                                onChange={(e) => updateSetting('scanner', 'enablePythonAnalyzer', e.target.checked)}
                                className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                            />
                        </label>

                        <label className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                            <div>
                                <p className="font-medium text-slate-200">ML Detection</p>
                                <p className="text-xs text-slate-500">Machine learning anomaly detection</p>
                            </div>
                            <input
                                type="checkbox"
                                checked={settings.scanner.enableMLDetection}
                                onChange={(e) => updateSetting('scanner', 'enableMLDetection', e.target.checked)}
                                className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                            />
                        </label>
                    </div>

                    {/* Right Column */}
                    <div className="space-y-4">
                        <h3 className="text-sm font-semibold text-slate-400 uppercase">Analysis Options</h3>

                        <label className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                            <div>
                                <p className="font-medium text-slate-200">Network Analysis</p>
                                <p className="text-xs text-slate-500">Analyze network traffic and connections</p>
                            </div>
                            <input
                                type="checkbox"
                                checked={settings.scanner.enableNetworkAnalysis}
                                onChange={(e) => updateSetting('scanner', 'enableNetworkAnalysis', e.target.checked)}
                                className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                            />
                        </label>

                        <label className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                            <div>
                                <p className="font-medium text-slate-200">Deep Scan</p>
                                <p className="text-xs text-slate-500">PE/ELF parsing and entropy analysis</p>
                            </div>
                            <input
                                type="checkbox"
                                checked={settings.scanner.deepScanEnabled}
                                onChange={(e) => updateSetting('scanner', 'deepScanEnabled', e.target.checked)}
                                className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                            />
                        </label>

                        <label className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                            <div>
                                <p className="font-medium text-slate-200">Auto Quarantine</p>
                                <p className="text-xs text-slate-500">Automatically quarantine critical threats</p>
                            </div>
                            <input
                                type="checkbox"
                                checked={settings.scanner.autoQuarantine}
                                onChange={(e) => updateSetting('scanner', 'autoQuarantine', e.target.checked)}
                                className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                            />
                        </label>

                        <div className="p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                            <label className="block mb-2">
                                <p className="font-medium text-slate-200 mb-1">Entropy Threshold</p>
                                <p className="text-xs text-slate-500 mb-2">Minimum entropy for packer detection</p>
                            </label>
                            <input
                                type="number"
                                step="0.1"
                                min="0"
                                max="8"
                                value={settings.scanner.entropyThreshold}
                                onChange={(e) => updateSetting('scanner', 'entropyThreshold', parseFloat(e.target.value))}
                                className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 focus:border-emerald-500 focus:outline-none"
                            />
                        </div>
                    </div>
                </div>
            </div>

            {/* Notification Settings */}
            <div className="glass rounded-xl p-6">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <Bell className="w-5 h-5 text-blue-500" />
                    Notification & Alerts
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Alert Channels */}
                    <div className="space-y-4">
                        <h3 className="text-sm font-semibold text-slate-400 uppercase">Alert Channels</h3>

                        <div className="p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                            <label className="flex items-center justify-between mb-3">
                                <p className="font-medium text-slate-200">Email Alerts</p>
                                <input
                                    type="checkbox"
                                    checked={settings.notifications.enableEmailAlerts}
                                    onChange={(e) => updateSetting('notifications', 'enableEmailAlerts', e.target.checked)}
                                    className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                                />
                            </label>
                            {settings.notifications.enableEmailAlerts && (
                                <input
                                    type="email"
                                    placeholder="your@email.com"
                                    value={settings.notifications.emailAddress}
                                    onChange={(e) => updateSetting('notifications', 'emailAddress', e.target.value)}
                                    className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 placeholder-slate-500 focus:border-emerald-500 focus:outline-none"
                                />
                            )}
                        </div>

                        <div className="p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                            <label className="flex items-center justify-between mb-3">
                                <p className="font-medium text-slate-200">Discord Webhook</p>
                                <input
                                    type="checkbox"
                                    checked={settings.notifications.enableDiscordWebhook}
                                    onChange={(e) => updateSetting('notifications', 'enableDiscordWebhook', e.target.checked)}
                                    className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                                />
                            </label>
                            {settings.notifications.enableDiscordWebhook && (
                                <input
                                    type="text"
                                    placeholder="https://discord.com/api/webhooks/..."
                                    value={settings.notifications.discordWebhookUrl}
                                    onChange={(e) => updateSetting('notifications', 'discordWebhookUrl', e.target.value)}
                                    className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 placeholder-slate-500 focus:border-emerald-500 focus:outline-none"
                                />
                            )}
                        </div>

                        <div className="p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                            <label className="flex items-center justify-between mb-3">
                                <p className="font-medium text-slate-200">Telegram Bot</p>
                                <input
                                    type="checkbox"
                                    checked={settings.notifications.enableTelegramBot}
                                    onChange={(e) => updateSetting('notifications', 'enableTelegramBot', e.target.checked)}
                                    className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                                />
                            </label>
                            {settings.notifications.enableTelegramBot && (
                                <div className="space-y-2">
                                    <input
                                        type="text"
                                        placeholder="Bot Token"
                                        value={settings.notifications.telegramBotToken}
                                        onChange={(e) => updateSetting('notifications', 'telegramBotToken', e.target.value)}
                                        className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 placeholder-slate-500 focus:border-emerald-500 focus:outline-none"
                                    />
                                    <input
                                        type="text"
                                        placeholder="Chat ID"
                                        value={settings.notifications.telegramChatId}
                                        onChange={(e) => updateSetting('notifications', 'telegramChatId', e.target.value)}
                                        className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 placeholder-slate-500 focus:border-emerald-500 focus:outline-none"
                                    />
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Alert Levels */}
                    <div className="space-y-4">
                        <h3 className="text-sm font-semibold text-slate-400 uppercase">Alert Trigger Levels</h3>

                        <label className="flex items-center justify-between p-3 bg-rose-500/10 border border-rose-500/50 rounded-lg">
                            <div>
                                <p className="font-medium text-rose-400">Critical Threats</p>
                                <p className="text-xs text-slate-500">Immediate action required</p>
                            </div>
                            <input
                                type="checkbox"
                                checked={settings.notifications.alertOnCritical}
                                onChange={(e) => updateSetting('notifications', 'alertOnCritical', e.target.checked)}
                                className="w-5 h-5 rounded border-slate-700 text-rose-500 focus:ring-rose-500"
                            />
                        </label>

                        <label className="flex items-center justify-between p-3 bg-amber-500/10 border border-amber-500/50 rounded-lg">
                            <div>
                                <p className="font-medium text-amber-400">High Threats</p>
                                <p className="text-xs text-slate-500">Significant security risk</p>
                            </div>
                            <input
                                type="checkbox"
                                checked={settings.notifications.alertOnHigh}
                                onChange={(e) => updateSetting('notifications', 'alertOnHigh', e.target.checked)}
                                className="w-5 h-5 rounded border-slate-700 text-amber-500 focus:ring-amber-500"
                            />
                        </label>

                        <label className="flex items-center justify-between p-3 bg-blue-500/10 border border-blue-500/50 rounded-lg">
                            <div>
                                <p className="font-medium text-blue-400">Medium Threats</p>
                                <p className="text-xs text-slate-500">Moderate security concern</p>
                            </div>
                            <input
                                type="checkbox"
                                checked={settings.notifications.alertOnMedium}
                                onChange={(e) => updateSetting('notifications', 'alertOnMedium', e.target.checked)}
                                className="w-5 h-5 rounded border-slate-700 text-blue-500 focus:ring-blue-500"
                            />
                        </label>

                        <label className="flex items-center justify-between p-3 bg-emerald-500/10 border border-emerald-500/50 rounded-lg">
                            <div>
                                <p className="font-medium text-emerald-400">Low Threats</p>
                                <p className="text-xs text-slate-500">Minor security issue</p>
                            </div>
                            <input
                                type="checkbox"
                                checked={settings.notifications.alertOnLow}
                                onChange={(e) => updateSetting('notifications', 'alertOnLow', e.target.checked)}
                                className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                            />
                        </label>
                    </div>
                </div>
            </div>

            {/* API Configuration */}
            <div className="glass rounded-xl p-6">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <Key className="w-5 h-5 text-purple-500" />
                    API Configuration
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                        <div className="p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                            <label className="block mb-2">
                                <p className="font-medium text-slate-200 mb-1">VirusTotal API Key</p>
                                <p className="text-xs text-slate-500 mb-2">Optional - for enhanced threat intelligence</p>
                            </label>
                            <input
                                type="password"
                                placeholder="Enter API key..."
                                value={settings.api.virusTotalApiKey}
                                onChange={(e) => updateSetting('api', 'virusTotalApiKey', e.target.value)}
                                className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 placeholder-slate-500 focus:border-emerald-500 focus:outline-none"
                            />
                        </div>

                        <div className="p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                            <label className="block mb-2">
                                <p className="font-medium text-slate-200 mb-1">AbuseIPDB API Key</p>
                                <p className="text-xs text-slate-500 mb-2">Optional - for IP reputation checking</p>
                            </label>
                            <input
                                type="password"
                                placeholder="Enter API key..."
                                value={settings.api.abuseIPDBApiKey}
                                onChange={(e) => updateSetting('api', 'abuseIPDBApiKey', e.target.value)}
                                className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 placeholder-slate-500 focus:border-emerald-500 focus:outline-none"
                            />
                        </div>
                    </div>

                    <div className="space-y-4">
                        <label className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                            <div>
                                <p className="font-medium text-slate-200">Enable Threat Intelligence</p>
                                <p className="text-xs text-slate-500">Query external threat databases</p>
                            </div>
                            <input
                                type="checkbox"
                                checked={settings.api.enableThreatIntel}
                                onChange={(e) => updateSetting('api', 'enableThreatIntel', e.target.checked)}
                                className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                            />
                        </label>

                        <div className="p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                            <label className="block mb-2">
                                <p className="font-medium text-slate-200 mb-1">API Rate Limit</p>
                                <p className="text-xs text-slate-500 mb-2">Maximum requests per hour</p>
                            </label>
                            <input
                                type="number"
                                min="10"
                                max="1000"
                                value={settings.api.apiRateLimit}
                                onChange={(e) => updateSetting('api', 'apiRateLimit', parseInt(e.target.value))}
                                className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 focus:border-emerald-500 focus:outline-none"
                            />
                        </div>
                    </div>
                </div>
            </div>

            {/* System Settings */}
            <div className="glass rounded-xl p-6">
                <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <Zap className="w-5 h-5 text-cyan-500" />
                    System Configuration
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                        <label className="block mb-2">
                            <p className="font-medium text-slate-200 mb-1">Max Scan Threads</p>
                            <p className="text-xs text-slate-500 mb-2">Concurrent scanning processes</p>
                        </label>
                        <input
                            type="number"
                            min="1"
                            max="16"
                            value={settings.system.maxScanThreads}
                            onChange={(e) => updateSetting('system', 'maxScanThreads', parseInt(e.target.value))}
                            className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 focus:border-emerald-500 focus:outline-none"
                        />
                    </div>

                    <div className="p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                        <label className="block mb-2">
                            <p className="font-medium text-slate-200 mb-1">Max Memory (MB)</p>
                            <p className="text-xs text-slate-500 mb-2">Maximum RAM usage</p>
                        </label>
                        <input
                            type="number"
                            min="512"
                            max="8192"
                            step="512"
                            value={settings.system.maxMemoryUsage}
                            onChange={(e) => updateSetting('system', 'maxMemoryUsage', parseInt(e.target.value))}
                            className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 focus:border-emerald-500 focus:outline-none"
                        />
                    </div>

                    <div className="p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                        <label className="block mb-2">
                            <p className="font-medium text-slate-200 mb-1">Log Level</p>
                            <p className="text-xs text-slate-500 mb-2">Logging verbosity</p>
                        </label>
                        <select
                            value={settings.system.logLevel}
                            onChange={(e) => updateSetting('system', 'logLevel', e.target.value)}
                            className="w-full px-4 py-2 bg-slate-900 border border-slate-700 rounded-lg text-slate-200 focus:border-emerald-500 focus:outline-none"
                        >
                            <option value="debug">Debug</option>
                            <option value="info">Info</option>
                            <option value="warning">Warning</option>
                            <option value="error">Error</option>
                        </select>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                    <label className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                        <div>
                            <p className="font-medium text-slate-200">Auto Updates</p>
                            <p className="text-xs text-slate-500">Automatically update signatures and rules</p>
                        </div>
                        <input
                            type="checkbox"
                            checked={settings.system.enableAutoUpdates}
                            onChange={(e) => updateSetting('system', 'enableAutoUpdates', e.target.checked)}
                            className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                        />
                    </label>

                    <label className="flex items-center justify-between p-3 bg-slate-950/50 rounded-lg border border-slate-800">
                        <div>
                            <p className="font-medium text-slate-200">Dark Mode</p>
                            <p className="text-xs text-slate-500">Use dark theme interface</p>
                        </div>
                        <input
                            type="checkbox"
                            checked={settings.system.darkMode}
                            onChange={(e) => updateSetting('system', 'darkMode', e.target.checked)}
                            className="w-5 h-5 rounded border-slate-700 text-emerald-500 focus:ring-emerald-500"
                        />
                    </label>
                </div>
            </div>

            {/* Save/Reset Footer */}
            <div className="flex items-center justify-between glass rounded-xl p-6">
                <p className="text-sm text-slate-400">
                    Changes will be applied immediately after saving
                </p>
                <div className="flex gap-3">
                    <button
                        onClick={handleReset}
                        className="px-6 py-3 bg-slate-800 text-slate-300 font-bold rounded-lg hover:bg-slate-700 transition-colors"
                    >
                        Reset to Default
                    </button>
                    <button
                        onClick={handleSave}
                        className="px-6 py-3 bg-emerald-500 text-slate-950 font-bold rounded-lg hover:bg-emerald-400 transition-colors"
                    >
                        Save All Changes
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Settings;
