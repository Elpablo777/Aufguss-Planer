// Typdefinitionen für die wichtigsten Datenstrukturen

export interface AufgussSession {
  id: string;
  title: string;
  description?: string;
  start_time: string;
  end_time: string;
  created_by: number;
  created_by_username: string;
  created_by_color: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string;
  color: string;
  is_active: boolean;
  is_staff: boolean;
  is_permanent_admin: boolean;
}
