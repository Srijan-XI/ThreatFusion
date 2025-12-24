import axios from 'axios';

const API_BASE_URL = '/api';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// API methods
export const threatFusionAPI = {
    // System status
    getStatus: () => api.get('/status'),
    getStatistics: () => api.get('/statistics'),

    // Scan operations
    startScan: (scanRequest) => api.post('/scan/start', scanRequest),
    getCurrentScan: () => api.get('/scan/current'),
    getScanHistory: () => api.get('/scan/history'),

    // Threats
    getThreats: (params) => api.get('/threats', { params }),
    getThreatDetails: (threatId) => api.get(`/threats/${threatId}`),

    // Reports
    listReports: () => api.get('/reports'),
};

// WebSocket connection
export class WebSocketClient {
    constructor(url = 'ws://localhost:8000/ws') {
        this.url = url;
        this.ws = null;
        this.listeners = new Map();
        this.reconnectDelay = 3000;
    }

    connect() {
        try {
            this.ws = new WebSocket(this.url);

            this.ws.onopen = () => {
                console.log('WebSocket connected');
                this.emit('connected');
            };

            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.emit(data.type, data);
                    this.emit('message', data);
                } catch (error) {
                    console.error('WebSocket message parse error:', error);
                }
            };

            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.emit('error', error);
            };

            this.ws.onclose = () => {
                console.log('WebSocket disconnected');
                this.emit('disconnected');
                // Auto-reconnect
                setTimeout(() => this.connect(), this.reconnectDelay);
            };
        } catch (error) {
            console.error('WebSocket connection error:', error);
        }
    }

    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(callback);
    }

    off(event, callback) {
        if (this.listeners.has(event)) {
            const callbacks = this.listeners.get(event);
            const index = callbacks.indexOf(callback);
            if (index > -1) {
                callbacks.splice(index, 1);
            }
        }
    }

    emit(event, data) {
        if (this.listeners.has(event)) {
            this.listeners.get(event).forEach(callback => callback(data));
        }
    }

    send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        }
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

export default api;
