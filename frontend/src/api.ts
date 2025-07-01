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
  if (!response.ok) throw new Error('Login fehlgeschlagen');
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

// Weitere API-Methoden (createAufguss, updateAufguss, deleteAufguss, fetchUsers, etc.) folgen analog
