export interface PuzzleMatrix {
  id: number;
  value: number;
  open: boolean;
  matched: boolean;
  hint: boolean;
}

export interface GameHistory {
  name: string;
  email: string;
  score: number;
  difficulty: string;
  matrixSize: number;
  limitTime: number;
  overTime: number;
}