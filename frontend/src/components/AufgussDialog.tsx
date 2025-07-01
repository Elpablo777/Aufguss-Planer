import React, { useState } from 'react';
import { AufgussSession } from '../types';

interface Props {
  aufguss: AufgussSession;
  isOpen: boolean;
  isCreating: boolean;
  onClose: () => void;
  onSave: (aufguss: AufgussSession) => void;
  onDelete: () => void;
}

const AufgussDialog: React.FC<Props> = ({ aufguss, isOpen, isCreating, onClose, onSave, onDelete }) => {
  const [form, setForm] = useState(aufguss);

  if (!isOpen) return null;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(form);
  };

  return (
    <div className="dialog-backdrop">
      <div className="dialog">
        <h2>{isCreating ? 'Neuen Aufguss anlegen' : 'Aufguss bearbeiten'}</h2>
        <form onSubmit={handleSubmit}>
          <input name="title" value={form.title} onChange={handleChange} placeholder="Titel" required />
          <textarea name="description" value={form.description} onChange={handleChange} placeholder="Beschreibung" />
          <input name="start_time" value={form.start_time} onChange={handleChange} type="datetime-local" required />
          <input name="end_time" value={form.end_time} onChange={handleChange} type="datetime-local" required />
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

export default AufgussDialog;
