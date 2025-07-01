import React, { useState } from 'react';
import { User } from '../types';

interface Props {
  user: User;
  isOpen: boolean;
  isCreating: boolean;
  onClose: () => void;
  onSave: (user: User) => void;
  onDelete: () => void;
}

const UserDialog: React.FC<Props> = ({ user, isOpen, isCreating, onClose, onSave, onDelete }) => {
  const [form, setForm] = useState(user);

  if (!isOpen) return null;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(form);
  };

  return (
    <div className="dialog-backdrop">
      <div className="dialog">
        <h2>{isCreating ? 'Neuen Benutzer anlegen' : 'Benutzer bearbeiten'}</h2>
        <form onSubmit={handleSubmit}>
          <input name="full_name" value={form.full_name} onChange={handleChange} placeholder="Name" required />
          <input name="username" value={form.username} onChange={handleChange} placeholder="Benutzername" required />
          <input name="email" value={form.email} onChange={handleChange} placeholder="E-Mail" required />
          <input name="color" value={form.color} onChange={handleChange} placeholder="Farbe (Hex)" required />
          <div className="dialog-actions">
            <button type="submit">Speichern</button>
            {!isCreating && <button type="button" onClick={onDelete}>Löschen</button>}
            <button type="button" onClick={onClose}>Abbrechen</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UserDialog;
