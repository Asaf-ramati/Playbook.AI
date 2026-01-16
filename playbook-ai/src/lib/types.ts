export interface PlayerMovement {
  id: string;
  x: number;
  y: number;
}

export interface TacticalPlay {
  name: string;
  description: string;
  steps: PlayerMovement[][]; // מערך של שלבים, בכל שלב רשימת תנועות של שחקנים
}

// זה ה-State של ה-LangGraph שלנו
export interface AgentState {
  playerPositions: any[];   // מה המצב כרגע במגרש
  userQuery: string;        // מה המשתמש ביקש
  selectedPlay?: TacticalPlay; // איזה תרגיל נבחר
  currentStep: number;      // באיזה שלב של התרגיל אנחנו (למהלכים רב-שלביים)
  analysis?: string;        // התובנות של ה-Analyzer
}