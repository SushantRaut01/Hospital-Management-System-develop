import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import AssistantDashboard from './Pages/Assistant/AssistantDashboard';
import DoctorDashboard from './Pages/Doctor/DoctorDashboard';
import DoctorAnalytics from './Pages/Doctor/DoctorAnalytics';
import PrintPrescription from './Pages/Doctor/components/print_prescription';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/assistant" element={<AssistantDashboard />} />
        <Route path="/doctor" element={<DoctorDashboard/>} />
        <Route path="/doctor/analytics" element={<DoctorAnalytics />} />
        <Route path="/print" element={<PrintPrescription />} />

      </Routes>
    </Router>
  );
}

export default App;
