// __mocks__/fullcalendar-react.js
import React from 'react';

// Mock-Implementierung für FullCalendar
// Gibt ein einfaches div zurück, das für Tests identifiziert werden kann.
// Die Props (plugins, initialView, etc.) werden hier ignoriert, könnten aber
// bei Bedarf an das div weitergegeben oder für komplexere Mock-Logik verwendet werden.
const MockFullCalendar = React.forwardRef((props, ref) => {
  // Man könnte hier props.events oder andere props auswerten, um den Mock dynamischer zu gestalten
  // console.log('MockFullCalendar props:', props);
  return (
    <div role="application" aria-label="Kalender" data-testid="fullcalendar-mock">
      {/* Man könnte hier auch eine vereinfachte Darstellung von Events rendern, wenn nötig */}
      <p>FullCalendar Mock</p>
      {props.events && props.events.length > 0 && (
        <div data-testid="mock-event-list">
          {props.events.map(event => (
            <div key={event.id || event.title}>{event.title}</div>
          ))}
        </div>
      )}
    </div>
  );
});

export default MockFullCalendar;
