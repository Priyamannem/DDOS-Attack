import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import LiveLogs from './pages/LiveLogs';
import Rules from './pages/Rules';
import IPManager from './pages/IPManager';
import AttackSimulator from './pages/AttackSimulator';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/logs" element={<LiveLogs />} />
          <Route path="/rules" element={<Rules />} />
          <Route path="/ip-manager" element={<IPManager />} />
          <Route path="/attack-simulator" element={<AttackSimulator />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
