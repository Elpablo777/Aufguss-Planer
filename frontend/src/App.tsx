import React from 'react';
import Calendar from './components/Calendar';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './components/Login';
import UserList from './components/UserList';
import Chat from './components/Chat';

const Main: React.FC = () => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? (
    <div>
      <h1>Sauna-Aufguss-Planer</h1>
      <Calendar />
      <UserList />
      <Chat />
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
