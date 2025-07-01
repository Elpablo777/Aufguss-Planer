import React from 'react';
import { useAuth } from '../context/AuthContext';

const LogoutButton: React.FC = () => {
  const { logout } = useAuth();
  return (
    <button onClick={logout} className="logout-button">
      Logout
    </button>
  );
};

export default LogoutButton;
