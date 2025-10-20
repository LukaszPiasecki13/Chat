export interface Profile {
  role: 'PLAYER' | 'OFFICIAL';
}

export interface User {
  id: number;
  username: string;
  profile: Profile;
}

export interface Message {
  id?: number;
  sender?: number | string;
  receiver?: number | string;
  content: string;
  timestamp?: string;
  isError?: boolean;
}