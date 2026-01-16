
export const COURT_WIDTH = 370;
export const COURT_HEIGHT = 580;


export const STARTING_POSITIONS_OFFENCE = {
  PG: { x: 160, y: 200 }, 
  SG: { x: 70, y: 150 },
  SF: { x: 250, y: 150 },
  PF: { x: 85, y: 30 }, 
  C: { x: 235, y: 30 }, 
};

export const STARTING_POSITIONS_DEFENCE = {
  PG: { x: 160, y: 180 },   
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