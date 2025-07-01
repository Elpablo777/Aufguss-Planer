import React, { useEffect, useState } from 'react';
import { fetchUsers, createUser, updateUser, deleteUser } from '../api';
import { User } from '../types';
import UserDialog from './UserDialog';

const AdminPanel: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
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

  const handleCreateUser = () => {
    setIsCreating(true);
    setSelectedUser({
      id: 0,
      username: '',
      email: '',
      full_name: '',
      color: '#000000',
      is_active: true,
      is_staff: false,
      is_permanent_admin: false
    });
    setIsDialogOpen(true);
  };

  const handleEditUser = (user: User) => {
    setIsCreating(false);
    setSelectedUser(user);
    setIsDialogOpen(true);
  };

  const handleSaveUser = async (user: User) => {
    try {
      if (isCreating) {
        await createUser(user);
      } else {
        await updateUser(user);
      }
      setIsDialogOpen(false);
      loadUsers();
    } catch (err) {
      setError('Fehler beim Speichern des Benutzers');
    }
  };

  const handleDeleteUser = async () => {
    if (selectedUser && !selectedUser.is_permanent_admin) {
      try {
        await deleteUser(selectedUser.id);
        setIsDialogOpen(false);
        loadUsers();
      } catch (err) {
        setError('Fehler beim Löschen des Benutzers');
      }
    } else {
      alert('Permanente Administratoren können nicht gelöscht werden.');
    }
  };

  return (
    <div className="admin-panel">
      <h2>Admin-Panel</h2>
      {error && <div className="error">{error}</div>}
      <button onClick={handleCreateUser} className="add-user-button">Neuen Benutzer hinzufügen</button>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Benutzername</th>
            <th>E-Mail</th>
            <th>Farbe</th>
            <th>Status</th>
            <th>Admin</th>
            <th>Aktionen</th>
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
              <td>
                <button onClick={() => handleEditUser(user)} className="edit-button">Bearbeiten</button>
                {!user.is_permanent_admin && (
                  <button onClick={handleDeleteUser} className="delete-button">Löschen</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {isDialogOpen && selectedUser && (
        <UserDialog
          user={selectedUser}
          isOpen={isDialogOpen}
          isCreating={isCreating}
          onClose={() => setIsDialogOpen(false)}
          onSave={handleSaveUser}
          onDelete={handleDeleteUser}
        />
      )}
    </div>
  );
};

export default AdminPanel;
