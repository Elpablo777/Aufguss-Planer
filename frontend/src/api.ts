// API-Client für die Kommunikation mit dem Django-Backend
// Abhängigkeiten: fetch (Browser), JWT-Token im LocalStorage
// Backend-Endpunkte: /api/token/, /api/token/refresh/, /api/aufguesse/, ...

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/';

export async function login(username: string, password: string) {
  const response = await fetch(API_URL + 'token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  if (!response.ok) {
    let errorMessage = 'Login fehlgeschlagen. Bitte überprüfen Sie Ihre Anmeldedaten.';
    try {
      const errorData = await response.json();
      if (errorData && errorData.detail) {
        errorMessage = errorData.detail;
      } else if (errorData && typeof errorData === 'object' && Object.keys(errorData).length > 0) {
        // Fallback, falls 'detail' nicht existiert, aber andere Fehlerdetails vorhanden sind
        errorMessage = Object.values(errorData).flat().join(' ');
      }
    } catch (e) {
      // JSON-Parsing fehlgeschlagen oder keine JSON-Antwort
      errorMessage = `Login fehlgeschlagen (Status: ${response.status}).`;
    }
    throw new Error(errorMessage);
  }
  const data = await response.json();
  localStorage.setItem('access', data.access);
  localStorage.setItem('refresh', data.refresh);
  return data;
}

export async function fetchAufguesse() {
  const token = localStorage.getItem('access');
  const response = await fetch(API_URL + 'aufguesse/', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error('Fehler beim Laden der Aufgüsse');
  return response.json();
}

export async function createAufguss(aufguss: any) {
  const token = localStorage.getItem('access');
  const response = await fetch(API_URL + 'aufguesse/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(aufguss)
  });
  if (!response.ok) throw new Error('Fehler beim Erstellen des Aufgusses');
  return response.json();
}

export async function updateAufguss(aufguss: any) {
  const token = localStorage.getItem('access');
  const response = await fetch(API_URL + 'aufguesse/' + aufguss.id + '/', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(aufguss)
  });
  if (!response.ok) throw new Error('Fehler beim Aktualisieren des Aufgusses');
  return response.json();
}

export async function deleteAufguss(id: string) {
  const token = localStorage.getItem('access');
  const response = await fetch(API_URL + 'aufguesse/' + id + '/', {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  if (!response.ok) throw new Error('Fehler beim Löschen des Aufgusses');
  return true;
}

export async function fetchUsers() {
  const token = localStorage.getItem('access');
  const response = await fetch(API_URL + 'users/', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error('Fehler beim Laden der Benutzer');
  return response.json();
}

export async function createUser(user: any) {
  const token = localStorage.getItem('access');
  const response = await fetch(API_URL + 'users/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(user)
  });
  if (!response.ok) throw new Error('Fehler beim Erstellen des Benutzers');
  return response.json();
}

export async function updateUser(user: any) {
  const token = localStorage.getItem('access');
  const response = await fetch(API_URL + 'users/' + user.id + '/', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(user)
  });
  if (!response.ok) throw new Error('Fehler beim Aktualisieren des Benutzers');
  return response.json();
}

export async function deleteUser(id: number) {
  const token = localStorage.getItem('access');
  const response = await fetch(API_URL + 'users/' + id + '/', {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  if (!response.ok) throw new Error('Fehler beim Löschen des Benutzers');
  return true;
}

// Weitere API-Methoden folgen analog
