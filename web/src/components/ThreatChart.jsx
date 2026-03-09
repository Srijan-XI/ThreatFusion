import { useEffect, useRef } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

const ThreatChart = ({ data }) => {
    const chartData = {
        labels: ['Critical', 'High', 'Medium', 'Low'],
        datasets: [
            {
                label: 'Threats',
                data: data ? [
                    data.CRITICAL || 0,
                    data.HIGH || 0,
                    data.MEDIUM || 0,
                    data.LOW || 0,
                ] : [0, 0, 0, 0],
                backgroundColor: [
                    'rgba(239, 68, 68, 0.8)',   // red
                    'rgba(251, 191, 36, 0.8)',  // amber
                    'rgba(59, 130, 246, 0.8)',  // blue
                    'rgba(16, 185, 129, 0.8)',  // emerald
                ],
                borderColor: [
                    'rgba(239, 68, 68, 1)',
                    'rgba(251, 191, 36, 1)',
                    'rgba(59, 130, 246, 1)',
                    'rgba(16, 185, 129, 1)',
                ],
                borderWidth: 2,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    color: '#94a3b8',
                    font: {
                        size: 12,
                    },
                    padding: 15,
                },
            },
            tooltip: {
                backgroundColor: '#0f172a',
                titleColor: '#f1f5f9',
                bodyColor: '#cbd5e1',
                borderColor: '#334155',
                borderWidth: 1,
                padding: 12,
                displayColors: true,
            },
        },
    };

    return (
        <div className="h-64">
            <Doughnut data={chartData} options={options} />
        </div>
    );
};

export default ThreatChart;
