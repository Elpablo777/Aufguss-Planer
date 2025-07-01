import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import Calendar from '../components/Calendar';
import * as api from '../api'; // Importiere alles aus api, um es mocken zu können
import { AuthProvider } from '../context/AuthContext'; // Benötigt für useAuth innerhalb von Calendar

// Mocken des gesamten api Moduls
jest.mock('../api');

// Mocken von WebSocket
const mockWebSocket = {
  onmessage: jest.fn(),
  close: jest.fn(),
};
global.WebSocket = jest.fn(() => mockWebSocket) as any;


// Mocken des AuthContext, falls Calendar ihn direkt oder indirekt für Token verwendet
// In diesem Fall wird localStorage.getItem('access') direkt verwendet,
// daher ist ein AuthContext-Mock hier nicht primär für den Token, aber gut für Vollständigkeit.
jest.mock('../context/AuthContext', () => {
  const originalModule = jest.requireActual('../context/AuthContext');
  return {
    ...originalModule,
    useAuth: () => ({
      isAuthenticated: true, // Annahme: Kalender wird nur für authentifizierte Benutzer angezeigt
      // Weitere gemockte Auth-Funktionen hier, falls benötigt
    }),
  };
});

describe('Calendar Component', () => {
  const mockFetchAufguesse = api.fetchAufguesse as jest.Mock;
  // const mockCreateAufguss = api.createAufguss as jest.Mock;
  // const mockUpdateAufguss = api.updateAufguss as jest.Mock;
  // const mockDeleteAufguss = api.deleteAufguss as jest.Mock;

  beforeEach(() => {
    mockFetchAufguesse.mockReset();
    // mockCreateAufguss.mockReset();
    // mockUpdateAufguss.mockReset();
    // mockDeleteAufguss.mockReset();

    // Standard-Mock-Implementierung für fetchAufguesse
    mockFetchAufguesse.mockResolvedValue([]); // Leeres Array als Standardantwort

    // localStorage Mock für den Token
    Storage.prototype.getItem = jest.fn((key) => {
      if (key === 'access') return 'fake-access-token';
      return null;
    });
  });

  test('renders FullCalendar and fetches aufguesse on mount', async () => {
    render(
      <AuthProvider>
        <Calendar />
      </AuthProvider>
    );

    // Überprüfen, ob fetchAufguesse aufgerufen wurde
    await waitFor(() => {
      expect(mockFetchAufguesse).toHaveBeenCalledTimes(1);
    });

    // Da FullCalendar selbst gemockt ist (siehe jest.config.js),
    // können wir nicht direkt nach FullCalendar-spezifischen Elementen suchen,
    // es sei denn, der Mock rendert etwas Eindeutiges.
    // Fürs Erste prüfen wir, ob der Container der Komponente gerendert wird.
    expect(screen.getByRole('application', { name: 'Kalender' })).toBeInTheDocument();
    // Der Mock für FullCalendar in __mocks__/fullcalendar-react.js muss ein passendes Role-Attribut haben.
    // Oder wir suchen nach einem allgemeineren Element, das vom Calendar-Wrapper gerendert wird.
    // z.B. wenn Calendar.tsx ein div mit einer bestimmten Klasse hätte.
    // Aktuell: <div className="calendar-container">
    expect(screen.getByText((content, element) => element?.tagName.toLowerCase() === 'div' && element.classList.contains('calendar-container'))).toBeInTheDocument();

  });

  test('displays error message if fetching aufguesse fails', async () => {
    mockFetchAufguesse.mockRejectedValueOnce(new Error('API Error'));
    render(
      <AuthProvider>
        <Calendar />
      </AuthProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Fehler beim Laden der Aufgüsse. Bitte versuchen Sie es später erneut.')).toBeInTheDocument();
    });
  });

  // TODO: Weitere Tests für:
  // - handleDateSelect (Öffnen des Dialogs im Create-Modus)
  // - handleEventClick (Öffnen des Dialogs im Edit-Modus)
  // - handleSaveAufguss (create und update)
  // - handleDeleteAufguss
  // - WebSocket-Nachrichtenverarbeitung (loadAufguesse Aufruf)
});
