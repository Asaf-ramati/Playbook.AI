
export const COURT_WIDTH = 660;
export const COURT_HEIGHT = 550;


export const STARTING_POSITIONS_OFFENCE = {
  PG: { x: 300, y: 400 }, 
  SG: { x: 160, y: 320 },
  SF: { x: 440, y: 320 },
  PF: { x: 180, y: 50 }, 
  C: { x: 400, y: 50 }, 
};

export const STARTING_POSITIONS_DEFENCE = {
  PG: { x: 300, y: 380 },   
  SG: { x: 160, y: 300 },   
  SF: { x: 440, y: 300 },   
  PF: { x: 180, y: 30 },   
  C: { x: 400, y: 30 },    
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