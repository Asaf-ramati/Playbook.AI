
export const COURT_WIDTH = 800;
export const COURT_HEIGHT = 500;


export const STARTING_POSITIONS_OFFENCE = {
  PG: { x: 405, y: 250 }, 
  SG: { x: 475, y: 210 },
  SF: { x: 335, y: 210 },
  PF: { x: 370, y: 150 }, 
  C: { x: 435, y: 150 }, 
};

export const STARTING_POSITIONS_DEFENCE = {
  PG: { x: 405, y: 230 },   
  SG: { x: 475, y: 190 },   
  SF: { x: 335, y: 190 },   
  PF: { x: 370, y: 130 },   
  C: { x: 435, y: 130 },    
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