// frontend/src/components/__mocks__/AufgussDialog.tsx
import React from 'react';

// Mock-Props-Typ, basierend auf dem Original, aber vereinfacht für den Mock
interface MockAufgussDialogProps {
  isOpen: boolean;
  isCreating: boolean;
  aufguss: any; // Vereinfacht für den Mock
  onClose: () => void;
  onSave: (aufguss: any) => void;
  onDelete: () => void;
}

const MockAufgussDialog: React.FC<MockAufgussDialogProps> = ({
  isOpen,
  isCreating,
  aufguss,
  onClose,
  onSave,
  onDelete,
}) => {
  if (!isOpen) {
    return null;
  }

  return (
    <div data-testid="aufguss-dialog-mock">
      <h3>{isCreating ? 'Neuer Aufguss Mock' : `Aufguss Bearbeiten Mock: ${aufguss?.title}`}</h3>
      <button onClick={onClose}>Schließen</button>
      <button onClick={() => onSave(aufguss)}>Speichern</button>
      {!isCreating && <button onClick={onDelete}>Löschen</button>}
    </div>
  );
};

export default MockAufgussDialog;
