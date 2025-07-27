// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import UserManagementPage from './pages/user/UserManagementPage';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import SchoolManagementPage from './pages/SchoolManagementPage'; // Import new page
import ClassManagementPage from './pages/ClassManagementPage'; // Import new page
import { AnimatePresence } from 'framer-motion';

function AppRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/login" element={<LoginPage />} />
        
        <Route 
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/schools" element={<SchoolManagementPage />} />
          <Route path="/classes" element={<ClassManagementPage />} />
          <Route path="/users" element={<UserManagementPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </AnimatePresence>
  );
}

function App() {
  return (
    <Router>
      <AppRoutes />
    </Router>
  );
}

export default App;