import React, { useEffect, useState } from 'react';
import { fetchUsers } from '../api';
import { User } from '../types';

const UserList: React.FC = () => {
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
    <div className="user-list">
      <h2>Benutzer</h2>
      {error && <div className="error">{error}</div>}
      <ul>
        {users.map(user => (
          <li key={user.id}>
            <span style={{ background: user.color, display: 'inline-block', width: 16, height: 16, borderRadius: '50%', marginRight: 8 }} />
            {user.full_name} ({user.username}) {user.is_permanent_admin && <b>Admin</b>}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UserList;
