# ThreatFusion Web Interface

Modern web interface for the ThreatFusion cybersecurity analysis platform.

## 🚀 Features

- **Real-time Dashboard** - Live threat monitoring with WebSocket updates
- **Scan Management** - Start, monitor, and manage security scans
- **Threat Analysis** - Detailed threat information and statistics
- **Interactive Charts** - Visual representation of threat data using Chart.js
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark Theme** - Professional glassmorphism design

## 🏗️ Tech Stack

### Frontend
- **React 18** - Modern UI framework
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Chart.js** - Data visualization
- **React Router** - Client-side routing
- **Lucide Icons** - Beautiful icon library
- **Axios** - HTTP client

### Backend
- **FastAPI** - Python web framework
- **WebSocket** - Real-time communication
- **Uvicorn** - ASGI server

## 📦 Installation

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+

### Setup

1. **Install frontend dependencies:**
   ```bash
   cd web
   npm install
   ```

2. **Install backend dependencies:**
   ```bash
   cd web/api
   pip install -r requirements.txt
   ```

## 🎯 Usage

### Development Mode

1. **Start the FastAPI backend:**
   ```bash
   cd web/api
   uvicorn main:app --reload --port 8000
   ```
   API will be available at: http://localhost:8000

2. **Start the React frontend:**
   ```bash
   cd web
   npm run dev
   ```
   Frontend will be available at: http://localhost:3000

### Production Build

```bash
cd web
npm run build
npm run preview
```

## 📁 Project Structure

```
web/
├── api/                    # FastAPI backend
│   ├── main.py            # Main API application
│   └── requirements.txt   # Python dependencies
│
├── src/                   # React frontend source
│   ├── components/        # Reusable components
│   │   ├── Layout.jsx
│   │   ├── StatCard.jsx
│   │   ├── ThreatChart.jsx
│   │   ├── RecentThreats.jsx
│   │   └── ScanProgress.jsx
│   │
│   ├── pages/            # Page components
│   │   ├── Dashboard.jsx
│   │   ├── Scans.jsx
│   │   ├── Threats.jsx
│   │   ├── Reports.jsx
│   │   └── Settings.jsx
│   │
│   ├── services/         # API services
│   │   └── api.js        # API client & WebSocket
│   │
│   ├── App.jsx           # Main app component
│   ├── main.jsx          # Entry point
│   └── index.css         # Global styles
│
├── index.html            # HTML entry point
├── package.json          # Dependencies
├── vite.config.js        # Vite configuration
└── tailwind.config.js    # Tailwind configuration
```

## 🔌 API Endpoints

### Status & Statistics
- `GET /api/status` - Get system status
- `GET /api/statistics` - Get overall statistics

### Scan Operations
- `POST /api/scan/start` - Start a new scan
- `GET /api/scan/current` - Get current scan status
- `GET /api/scan/history` - Get scan history

### Threats
- `GET /api/threats` - List detected threats
- `GET /api/threats/{id}` - Get threat details

### Reports
- `GET /api/reports` - List available reports

### Real-time
- `WS /ws` - WebSocket for live updates

## 🎨 Design Features

- **Glassmorphism** - Modern glass-effect UI elements
- **Dark Theme** - Professional dark color scheme
- **Responsive** - Mobile-first responsive design
- **Animations** - Smooth transitions and micro-interactions
- **Color-coded** - Threat levels with visual indicators
- **Real-time Updates** - Live data via WebSocket

## 🔧 Configuration

### API Proxy
The Vite dev server proxies `/api` requests to `http://localhost:8000`.
Configure in `vite.config.js`:

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

### WebSocket URL
Default: `ws://localhost:8000/ws`
Configure in `src/services/api.js`

## 🚧 Roadmap

### Phase 1: ✅ Complete
- [x] FastAPI backend setup
- [x] React frontend setup
- [x] WebSocket integration
- [x] Dashboard with statistics
- [x] Real-time scan progress
- [x] Threat visualization

### Phase 2: In Progress
- [ ] Complete scan management
- [ ] Detailed threat analysis page
- [ ] Report viewer
- [ ] Settings interface
- [ ] Authentication (JWT)

### Phase 3: Planned
- [ ] User management & RBAC
- [ ] Advanced filtering & search
- [ ] Export functionality
- [ ] Real-time notifications
- [ ] Historical data charts
- [ ] System health monitoring

## 🧪 Testing

```bash
# Run frontend tests (when added)
npm test

# Run backend tests (when added)
cd api
pytest
```

## 📝 License

Part of the ThreatFusion project. See main project README for details.

## 🤝 Contributing

Contributions welcome! This web interface integrates with the core ThreatFusion platform.

---

**Built with ❤️ for cybersecurity professionals**
