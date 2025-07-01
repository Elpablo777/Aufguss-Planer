import React, { useEffect, useState } from 'react';
import { fetchUsers } from '../api';
import { User } from '../types';

const AdminPanel: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      const data = await fetchUsers();
      setUsers(data);
    } catch (err) {
      setError('Fehler beim Laden der Benutzer');
    }
  };

  return (
    <div className="admin-panel">
      <h2>Admin-Panel</h2>
      {error && <div className="error">{error}</div>}
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Benutzername</th>
            <th>E-Mail</th>
            <th>Farbe</th>
            <th>Status</th>
            <th>Admin</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.full_name}</td>
              <td>{user.username}</td>
              <td>{user.email}</td>
              <td><span style={{ background: user.color, display: 'inline-block', width: 16, height: 16, borderRadius: '50%' }} /></td>
              <td>{user.is_active ? 'Aktiv' : 'Inaktiv'}</td>
              <td>{user.is_permanent_admin ? 'Ja' : 'Nein'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminPanel;
