import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import AufgussDialog from '../components/AufgussDialog';
import { AufgussSession } from '../types';

const mockOnClose = jest.fn();
const mockOnSave = jest.fn();
const mockOnDelete = jest.fn();

const initialAufguss: AufgussSession = {
  id: '1',
  title: 'Test Aufguss',
  description: 'Eine Beschreibung',
  start_time: '2024-01-01T10:00', // Format für datetime-local
  end_time: '2024-01-01T11:00',
  created_by: 1,
  created_by_username: 'Test User',
  created_by_color: '#FF0000',
};

const emptyAufguss: AufgussSession = {
  id: '',
  title: '',
  description: '',
  start_time: '2024-01-01T12:00', // Default für neue Eingabe
  end_time: '2024-01-01T13:00',
  created_by: 0,
  created_by_username: '',
  created_by_color: '',
};


describe('AufgussDialog Component', () => {
  beforeEach(() => {
    mockOnClose.mockClear();
    mockOnSave.mockClear();
    mockOnDelete.mockClear();
  });

  test('does not render when isOpen is false', () => {
    render(
      <AufgussDialog
        aufguss={initialAufguss}
        isOpen={false}
        isCreating={false}
        onClose={mockOnClose}
        onSave={mockOnSave}
        onDelete={mockOnDelete}
      />
    );
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    // Da der Dialog bei !isOpen null zurückgibt, können wir auch prüfen, ob der Container leer ist.
    // Oder spezifischer, dass der Dialog-Backdrop nicht da ist.
    expect(screen.queryByText('Aufguss bearbeiten')).not.toBeInTheDocument();

  });

  describe('When isOpen is true', () => {
    test('renders in create mode correctly', () => {
      render(
        <AufgussDialog
          aufguss={emptyAufguss}
          isOpen={true}
          isCreating={true}
          onClose={mockOnClose}
          onSave={mockOnSave}
          onDelete={mockOnDelete}
        />
      );
      expect(screen.getByRole('heading', { name: /Neuen Aufguss anlegen/i })).toBeInTheDocument();
      expect(screen.getByPlaceholderText(/Titel/i)).toHaveValue(emptyAufguss.title);
      expect(screen.getByPlaceholderText(/Beschreibung/i)).toHaveValue(emptyAufguss.description);
      expect(screen.getByDisplayValue(emptyAufguss.start_time)).toBeInTheDocument();
      expect(screen.getByDisplayValue(emptyAufguss.end_time)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /Speichern/i })).toBeInTheDocument();
      expect(screen.queryByRole('button', { name: /Löschen/i })).not.toBeInTheDocument();
      expect(screen.getByRole('button', { name: /Abbrechen/i })).toBeInTheDocument();
    });

    test('renders in edit mode correctly with initial data', () => {
      render(
        <AufgussDialog
          aufguss={initialAufguss}
          isOpen={true}
          isCreating={false}
          onClose={mockOnClose}
          onSave={mockOnSave}
          onDelete={mockOnDelete}
        />
      );
      expect(screen.getByRole('heading', { name: /Aufguss bearbeiten/i })).toBeInTheDocument();
      expect(screen.getByPlaceholderText(/Titel/i)).toHaveValue(initialAufguss.title);
      expect(screen.getByPlaceholderText(/Beschreibung/i)).toHaveValue(initialAufguss.description);
      expect(screen.getByDisplayValue(initialAufguss.start_time)).toBeInTheDocument();
      expect(screen.getByDisplayValue(initialAufguss.end_time)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /Speichern/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /Löschen/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /Abbrechen/i })).toBeInTheDocument();
    });

    test('updates form fields on user input', async () => {
      const user = userEvent.setup();
      render(
        <AufgussDialog
          aufguss={emptyAufguss}
          isOpen={true}
          isCreating={true}
          onClose={mockOnClose}
          onSave={mockOnSave}
          onDelete={mockOnDelete}
        />
      );

      const titleInput = screen.getByPlaceholderText(/Titel/i);
      const descriptionInput = screen.getByPlaceholderText(/Beschreibung/i);
      // Für datetime-local ist die Interaktion mit userEvent etwas anders,
      // fireEvent.change ist hier oft einfacher oder man tippt den String direkt.
      const startTimeInput = screen.getByDisplayValue(emptyAufguss.start_time);

      await user.clear(titleInput);
      await user.type(titleInput, 'Neuer Titel');
      expect(titleInput).toHaveValue('Neuer Titel');

      await user.clear(descriptionInput);
      await user.type(descriptionInput, 'Neue Beschreibung');
      expect(descriptionInput).toHaveValue('Neue Beschreibung');

      // Für datetime-local:
      fireEvent.change(startTimeInput, { target: { value: '2024-02-02T14:00' } });
      expect(startTimeInput).toHaveValue('2024-02-02T14:00');
    });

    test('calls onSave with form data on submit', async () => {
      const user = userEvent.setup();
      const aufgussDataForSave = { ...emptyAufguss, title: 'Gespeicherter Titel' };
      render(
        <AufgussDialog
          aufguss={emptyAufguss} // Start mit leeren Daten
          isOpen={true}
          isCreating={true}
          onClose={mockOnClose}
          onSave={mockOnSave}
          onDelete={mockOnDelete}
        />
      );

      const titleInput = screen.getByPlaceholderText(/Titel/i);
      await user.clear(titleInput);
      await user.type(titleInput, aufgussDataForSave.title);
      // Weitere Felder könnten hier auch geändert werden.

      const saveButton = screen.getByRole('button', { name: /Speichern/i });
      await user.click(saveButton);

      expect(mockOnSave).toHaveBeenCalledTimes(1);
      expect(mockOnSave).toHaveBeenCalledWith(
        expect.objectContaining({
          title: aufgussDataForSave.title,
          description: emptyAufguss.description, // Da nicht geändert
          start_time: emptyAufguss.start_time,   // Da nicht geändert
          end_time: emptyAufguss.end_time,     // Da nicht geändert
        })
      );
    });

    test('calls onDelete when delete button is clicked (edit mode)', async () => {
      const user = userEvent.setup();
      render(
        <AufgussDialog
          aufguss={initialAufguss}
          isOpen={true}
          isCreating={false} // Edit mode
          onClose={mockOnClose}
          onSave={mockOnSave}
          onDelete={mockOnDelete}
        />
      );

      const deleteButton = screen.getByRole('button', { name: /Löschen/i });
      await user.click(deleteButton);

      expect(mockOnDelete).toHaveBeenCalledTimes(1);
    });

    test('calls onClose when cancel button is clicked', async () => {
      const user = userEvent.setup();
      render(
        <AufgussDialog
          aufguss={initialAufguss}
          isOpen={true}
          isCreating={false}
          onClose={mockOnClose}
          onSave={mockOnSave}
          onDelete={mockOnDelete}
        />
      );

      const cancelButton = screen.getByRole('button', { name: /Abbrechen/i });
      await user.click(cancelButton);

      expect(mockOnClose).toHaveBeenCalledTimes(1);
    });
  });
});
