import React from 'react';
import Calendar from './components/Calendar';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './components/Login';
import UserList from './components/UserList';
import Chat from './components/Chat';
import LogoutButton from './components/LogoutButton';
import AdminPanel from './components/AdminPanel';

import './styles.css'; // Importiere die globale CSS-Datei

const Main: React.FC = () => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? (
    <div className="app-container">
      <header className="app-header">
        <h1>Sauna-Aufguss-Planer</h1>
        <LogoutButton />
      </header>
      <main className="app-main-authenticated">
        <section className="app-main-content">
          <Calendar />
        </section>
        <aside className="app-sidebar">
          <UserList />
          <Chat />
          <AdminPanel />
        </aside>
      </main>
    </div>
  ) : (
    <div className="login-form-container"> {/* Wrapper für Zentrierung */}
      <Login />
    </div>
  );
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Main />
    </AuthProvider>
  );
};

export default App;
