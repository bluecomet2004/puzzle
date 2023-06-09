export interface User {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface UserDashbaord {
  success: boolean;
  total: number;
  current_page: number;
  last_page: number;
  list: User[];
}

export interface editUser {
  id: string;
  name: string;
}

export interface Message {
  success: boolean;
  message: string;
}
