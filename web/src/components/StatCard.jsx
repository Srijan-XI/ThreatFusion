import { TrendingUp, TrendingDown } from 'lucide-react';

const StatCard = ({ icon, label, value, change, trend, color = 'emerald' }) => {
    const colorClasses = {
        blue: 'from-blue-500/10 to-blue-900/10 border-blue-500/50',
        green: 'from-green-500/10 to-green-900/10 border-green-500/50',
        red: 'from-rose-500/10 to-rose-900/10 border-rose-500/50',
        emerald: 'from-emerald-500/10 to-emerald-900/10 border-emerald-500/50',
    };

    const iconColorClasses = {
        blue: 'text-blue-400',
        green: 'text-green-400',
        red: 'text-rose-400',
        emerald: 'text-emerald-400',
    };

    return (
        <div className={`glass glass-hover rounded-xl p-6 bg-gradient-to-br ${colorClasses[color]} transition-all duration-300`}>
            <div className="flex items-center justify-between mb-4">
                <div className={`p-3 rounded-lg bg-slate-950/50 ${iconColorClasses[color]}`}>
                    {icon}
                </div>
                {change && (
                    <div className={`flex items-center gap-1 text-sm font-medium ${trend === 'up' ? 'text-emerald-400' : 'text-rose-400'}`}>
                        {trend === 'up' ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                        {change}
                    </div>
                )}
            </div>
            <p className="text-slate-400 text-sm mb-1">{label}</p>
            <p className="text-3xl font-bold text-white">{value.toLocaleString()}</p>
        </div>
    );
};

export default StatCard;
