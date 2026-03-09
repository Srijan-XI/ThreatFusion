import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Scans from './pages/Scans'
import Threats from './pages/Threats'
import Reports from './pages/Reports'
import Settings from './pages/Settings'

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Layout />}>
                    <Route index element={<Dashboard />} />
                    <Route path="scans" element={<Scans />} />
                    <Route path="threats" element={<Threats />} />
                    <Route path="reports" element={<Reports />} />
                    <Route path="settings" element={<Settings />} />
                </Route>
            </Routes>
        </Router>
    )
}

export default App
