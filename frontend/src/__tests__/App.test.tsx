import React from "react";
import { render, screen } from '@testing-library/react';
import App from '../App';

// Browser-APIs mocken
beforeAll(() => {
  window.alert = jest.fn();
  window.HTMLElement.prototype.scrollIntoView = jest.fn();
});

// Hilfsfunktion: Authentifizierten Zustand mocken
jest.mock('../context/AuthContext', () => {
  const actual = jest.requireActual('../context/AuthContext');
  return {
    ...actual,
    useAuth: () => ({ isAuthenticated: true, login: jest.fn(), logout: jest.fn() })
  };
});

describe('App', () => {
  it('rendert ohne Crash und zeigt Titel', () => {
    render(<App />);
    expect(screen.getByText(/Sauna-Aufguss-Planer/i)).toBeInTheDocument();
  });
});
