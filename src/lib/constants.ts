
export const COURT_WIDTH = 800;
export const COURT_HEIGHT = 500;


export const STARTING_POSITIONS = {
  PG: { x: 400, y: 420 }, 
  SG: { x: 150, y: 350 },
  SF: { x: 650, y: 350 },
  PF: { x: 250, y: 150 }, 
  C: { x: 550, y: 150 }, 
};

export const COURT_ZONES = {
  LEFT_CORNER: { x: 50, y: 50 },
  RIGHT_CORNER: { x: 750, y: 50 },
  PAINT: { x: 400, y: 120 },
  TOP_OF_KEY: { x: 400, y: 420 },
  LEFT_WING: { x: 150, y: 350 },
  RIGHT_WING: { x: 650, y: 350 },
};

export type TeamSide = 'ATTACK' | 'DEFENSE';