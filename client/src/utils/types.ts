export interface PuzzleMatrix {
  id: number;
  value: number;
  open: boolean;
  matched: boolean;
  hint: boolean;
}