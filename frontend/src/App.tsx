import React from 'react';
import Calendar from './components/Calendar';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './components/Login';
import UserList from './components/UserList';
import Chat from './components/Chat';
import LogoutButton from './components/LogoutButton';
import AdminPanel from './components/AdminPanel';

const Main: React.FC = () => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? (
    <div>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '1rem 2rem', background: '#e3e3e3' }}>
        <h1>Sauna-Aufguss-Planer</h1>
        <LogoutButton />
      </header>
      <main style={{ maxWidth: 1200, margin: '2rem auto', display: 'flex', gap: '2rem' }}>
        <section style={{ flex: 2 }}>
          <Calendar />
        </section>
        <aside style={{ flex: 1 }}>
          <UserList />
          <Chat />
          <AdminPanel />
        </aside>
      </main>
    </div>
  ) : (
    <Login />
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
