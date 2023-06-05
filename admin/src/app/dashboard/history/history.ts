export interface History {
  id: string;
  name: string;
  email: string;
  score: number;
  difficulty: string;
  matrixSize: number;
  limitTime: number;
  overTime: number;
  finishedAt: Date;
}

export interface HistoryDashboard {
  success: boolean;
  total: number;
  current_page: number;
  last_page: number;
  list: History[];
}

export interface HistoryMessage {
  success: boolean;
  message: string;
}