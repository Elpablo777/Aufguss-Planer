import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Login from '../components/Login';
import { AuthProvider, useAuth } from '../context/AuthContext'; // Importiere AuthProvider für den Kontext

// Mocken des AuthContext
const mockLogin = jest.fn();
const mockUseAuth = useAuth as jest.Mock;

jest.mock('../context/AuthContext', () => {
  const originalModule = jest.requireActual('../context/AuthContext');
  return {
    ...originalModule,
    useAuth: jest.fn(),
  };
});

// Hilfsfunktion zum Rendern der Komponente mit dem Provider
const renderLoginComponent = () => {
  return render(
    <AuthProvider> {/* Login benötigt den AuthProvider */}
      <Login />
    </AuthProvider>
  );
};


describe('Login Component', () => {
  beforeEach(() => {
    // Setze den Mock für jeden Test zurück und konfiguriere ihn neu
    mockLogin.mockReset();
    mockUseAuth.mockImplementation(() => ({
      login: mockLogin,
      isAuthenticated: false, // Standardmäßig nicht authentifiziert
      logout: jest.fn(),
    }));
  });

  test('renders login form elements correctly', () => {
    renderLoginComponent();
    expect(screen.getByPlaceholderText(/Benutzername/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Passwort/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Login/i })).toBeInTheDocument();
  });

  test('allows user to type in username and password fields', async () => {
    const user = userEvent.setup();
    renderLoginComponent();

    const usernameInput = screen.getByPlaceholderText(/Benutzername/i);
    const passwordInput = screen.getByPlaceholderText(/Passwort/i);

    await user.type(usernameInput, 'testuser');
    await user.type(passwordInput, 'password123');

    expect(usernameInput).toHaveValue('testuser');
    expect(passwordInput).toHaveValue('password123');
  });

  test('calls login function with username and password on submit', async () => {
    const user = userEvent.setup();
    renderLoginComponent();

    const usernameInput = screen.getByPlaceholderText(/Benutzername/i);
    const passwordInput = screen.getByPlaceholderText(/Passwort/i);
    const loginButton = screen.getByRole('button', { name: /Login/i });

    await user.type(usernameInput, 'testuser');
    await user.type(passwordInput, 'password123');
    await user.click(loginButton);

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledTimes(1);
      expect(mockLogin).toHaveBeenCalledWith('testuser', 'password123');
    });
  });

  test('displays error message if login fails', async () => {
    const user = userEvent.setup();
    // Simuliere einen Fehler beim Login
    mockLogin.mockRejectedValueOnce(new Error('Login failed'));

    renderLoginComponent();

    const usernameInput = screen.getByPlaceholderText(/Benutzername/i);
    const passwordInput = screen.getByPlaceholderText(/Passwort/i);
    const loginButton = screen.getByRole('button', { name: /Login/i });

    await user.type(usernameInput, 'testuser');
    await user.type(passwordInput, 'password123');
    await user.click(loginButton);

    await waitFor(() => {
      expect(screen.getByText(/Login fehlgeschlagen/i)).toBeInTheDocument();
    });
  });

  test('does not display error message if login succeeds', async () => {
    const user = userEvent.setup();
    // Simuliere erfolgreichen Login
    mockLogin.mockResolvedValueOnce(undefined);

    renderLoginComponent();

    const usernameInput = screen.getByPlaceholderText(/Benutzername/i);
    const passwordInput = screen.getByPlaceholderText(/Passwort/i);
    const loginButton = screen.getByRole('button', { name: /Login/i });

    await user.type(usernameInput, 'testuser');
    await user.type(passwordInput, 'password123');
    await user.click(loginButton);

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledTimes(1);
    });
    expect(screen.queryByText(/Login fehlgeschlagen/i)).not.toBeInTheDocument();
  });
});
