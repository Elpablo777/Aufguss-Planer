import React from "react";
import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App', () => {
  it('rendert ohne Crash', () => {
    render(<App />);
    expect(screen.getByText(/Aufguss/i)).toBeInTheDocument();
  });
});
