import React, { useState, useEffect, useRef } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import { AufgussSession } from '../types';
import { fetchAufguesse, createAufguss, updateAufguss, deleteAufguss } from '../api';
import AufgussDialog from './AufgussDialog';
import { useAuth } from '../context/AuthContext';

const Calendar: React.FC = () => {
  const [aufguesse, setAufguesse] = useState<AufgussSession[]>([]);
  const [selectedAufguss, setSelectedAufguss] = useState<AufgussSession | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState<string | null>(null); // Zustand für Fehlermeldungen
  const wsAufguss = useRef<WebSocket | null>(null);

  useEffect(() => {
    loadAufguesse();

    // WebSocket für Live-Updates
    const token = localStorage.getItem('access');
    if (token) {
      // Token wird jetzt im Sec-WebSocket-Protocol Header gesendet
      wsAufguss.current = new WebSocket('ws://' + window.location.host + '/ws/aufguss/', [token]);
      wsAufguss.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'aufguss_update') {
          loadAufguesse();
        }
      };
    }
    return () => { wsAufguss.current?.close(); };
  }, []);

  const loadAufguesse = async () => {
    try {
      const data = await fetchAufguesse();
      setAufguesse(data);
      setError(null); // Fehler zurücksetzen bei Erfolg
    } catch (error) {
      console.error("Fehler beim Laden der Aufgüsse:", error);
      setError('Fehler beim Laden der Aufgüsse. Bitte versuchen Sie es später erneut.');
    }
  };

  const handleDateSelect = (selectInfo: any) => {
    setIsCreating(true);
    setSelectedAufguss({
      id: '',
      title: '',
      description: '',
      start_time: selectInfo.startStr,
      end_time: selectInfo.endStr,
      created_by: 0,
      created_by_username: '',
      created_by_color: ''
    });
    setIsDialogOpen(true);
  };

  const handleEventClick = (clickInfo: any) => {
    const aufguss = aufguesse.find(a => a.id === clickInfo.event.id);
    if (aufguss) {
      setIsCreating(false);
      setSelectedAufguss(aufguss);
      setIsDialogOpen(true);
    }
  };

  const handleSaveAufguss = async (aufguss: AufgussSession) => {
    try {
      if (isCreating) {
        await createAufguss(aufguss);
      } else {
        await updateAufguss(aufguss);
      }
      setIsDialogOpen(false);
      setError(null);
      loadAufguesse();
    } catch (error) {
      console.error("Fehler beim Speichern des Aufgusses:", error);
      setError('Fehler beim Speichern des Aufgusses.');
    }
  };

  const handleDeleteAufguss = async () => {
    if (selectedAufguss) {
      try {
        await deleteAufguss(selectedAufguss.id);
        setIsDialogOpen(false);
        setError(null);
        loadAufguesse();
      } catch (error) {
        console.error("Fehler beim Löschen des Aufgusses:", error);
        setError('Fehler beim Löschen des Aufgusses.');
      }
    }
  };

  const events = aufguesse.map(aufguss => ({
    id: aufguss.id,
    title: aufguss.title,
    start: aufguss.start_time,
    end: aufguss.end_time,
    backgroundColor: aufguss.created_by_color,
    borderColor: aufguss.created_by_color,
    extendedProps: {
      description: aufguss.description,
      createdBy: aufguss.created_by_username
    }
  }));

  return (
    <div className="calendar-container">
      {error && (
        <div style={{ color: 'red', padding: '10px', border: '1px solid red', marginBottom: '10px' }}>
          {error}
          <button onClick={() => setError(null)} style={{ marginLeft: '10px' }}>
            Schließen
          </button>
        </div>
      )}
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="timeGridWeek"
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        }}
        editable={true}
        selectable={true}
        dayMaxEvents={true}
        weekends={true}
        events={events}
        select={handleDateSelect}
        eventClick={handleEventClick}
        locale="de"
        firstDay={1}
        slotMinTime="06:00:00"
        slotMaxTime="23:00:00"
      />
      {isDialogOpen && selectedAufguss && (
        <AufgussDialog
          aufguss={selectedAufguss}
          isOpen={isDialogOpen}
          isCreating={isCreating}
          onClose={() => setIsDialogOpen(false)}
          onSave={handleSaveAufguss}
          onDelete={handleDeleteAufguss}
        />
      )}
    </div>
  );
};

export default Calendar;
