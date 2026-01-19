export interface PlayerMovement {
  id: string;
  x: number;
  y: number;
}

export interface TacticalPlay {
  name: string;
  description: string;
  steps: PlayerMovement[][]; // Array of steps, each step contains a list of player movements
}

// This is our LangGraph State
export interface AgentState {
  playerPositions: any[];   // Current state on the court
  userQuery: string;        // What the user requested
  selectedPlay?: TacticalPlay; // Which drill was selected
  currentStep: number;      // Which step of the drill we're at (for multi-step movements)
  analysis?: string;        // Insights from the Analyzer
}