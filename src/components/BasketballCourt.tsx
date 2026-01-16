"use client";
import { PlayerNode } from './PlayerNode';
import React, { useCallback } from 'react';
import { useCopilotAction } from "@copilotkit/react-core";
import ReactFlow, { 
  Background, 
  Controls, 
  useNodesState, 
  useEdgesState,
  Panel
} from 'reactflow';
import 'reactflow/dist/style.css';
import { COURT_WIDTH, COURT_HEIGHT, STARTING_POSITIONS_OFFENCE, STARTING_POSITIONS_DEFENCE } from '@/src/lib/constants';
import { useFrontendTool, useCopilotReadable } from "@copilotkit/react-core";

const nodeTypes = {
  player: PlayerNode,
};

const initialNodes = [
  // Ball
  {
    id: 'ball',
    type: 'input',
    data: { label: '🏀' },
    position: { x: COURT_WIDTH / 2 - 20, y: COURT_HEIGHT - 100 },
    draggable: true,
    style: { 
      borderRadius: '50%', 
      width: 20, 
      height: 20, 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      backgroundColor: '#ff8c00',
      color: '#fff',
      fontSize: '16px',
    },
  },

  // TEAM 1 - LAKERS (Purple #552583)
  {
    id: 'team1-pg',
    type: 'player',
    position: STARTING_POSITIONS_OFFENCE.PG,  // { x: 400, y: 420 }
    data: { 
      name: 'D. Russell',
      number: 1,
      position: 'PG',
      team: 'Lakers',
      color: '#552583'  // Lakers purple
    },
  },
  {
    id: 'team1-sg',
    type: 'player',
    position: STARTING_POSITIONS_OFFENCE.SG,  // { x: 150, y: 350 }
    data: { 
      name: 'A. Reaves',
      number: 15,
      position: 'SG',
      team: 'Lakers',
      color: '#552583'
    },
  },
  {
    id: 'team1-sf',
    type: 'player',
    position: STARTING_POSITIONS_OFFENCE.SF,  // { x: 650, y: 350 }
    data: { 
      name: 'LeBron James',
      number: 23,
      position: 'SF',
      team: 'Lakers',
      color: '#552583'
    },
  },
  {
    id: 'team1-pf',
    type: 'player',
    position: STARTING_POSITIONS_OFFENCE.PF,  // { x: 250, y: 150 }
    data: { 
      name: 'R. Hachimura',
      number: 28,
      position: 'PF',
      team: 'Lakers',
      color: '#552583'
    },
  },
  {
    id: 'team1-c',
    type: 'player',
    position: STARTING_POSITIONS_OFFENCE.C,  // { x: 550, y: 150 }
    data: { 
      name: 'A. Davis',
      number: 3,
      position: 'C',
      team: 'Lakers',
      color: '#552583'
    },
  },

  // TEAM 2 - WARRIORS (Blue #1D428A)
  {
    id: 'team2-pg',
    type: 'player',
    position: STARTING_POSITIONS_DEFENCE.PG,  // Opposite end
    data: { 
      name: 'S. Curry',
      number: 30,
      position: 'PG',
      team: 'Warriors',
      color: '#1D428A'
    },
  },
  {
    id: 'team2-sg',
    type: 'player',
    position: STARTING_POSITIONS_DEFENCE.SG,
    data: { 
      name: 'K. Thompson',
      number: 11,
      position: 'SG',
      team: 'Warriors',
      color: '#1D428A'
    },
  },
  {
    id: 'team2-sf',
    type: 'player',
    position: STARTING_POSITIONS_DEFENCE.SF,
    data: { 
      name: 'A. Wiggins',
      number: 22,
      position: 'SF',
      team: 'Warriors',
      color: '#1D428A'
    },
  },
  {
    id: 'team2-pf',
    type: 'player',
    position: STARTING_POSITIONS_DEFENCE.PF,
    data: { 
      name: 'D. Green',
      number: 23,
      position: 'PF',
      team: 'Warriors',
      color: '#1D428A'
    },
  },
  {
    id: 'team2-c',
    type: 'player',
    position: STARTING_POSITIONS_DEFENCE.C,
    data: { 
      name: 'K. Looney',
      number: 5,
      position: 'C',
      team: 'Warriors',
      color: '#1D428A'
    },
  },
];

const initialEdges: any[] = [];

export default function BasketballCourt() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  
  useCopilotReadable({
  description: "The current positions of all players and the ball on the court",
  value: nodes,
});

  useCopilotAction({
  name: "updatePlayerPosition",
  description: "Update the position of a player or the ball on the court",
  parameters: [
    { name: "id", type: "string", description: "The ID of the player to move (e.g., 'p1', 'ball')" },
    { name: "x", type: "number", description: "The new X coordinate (0-800)" },
    { name: "y", type: "number", description: "The new Y coordinate (0-500)" },
  ],
  handler: ({ id, x, y }) => {
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === id) {
          return { ...node, position: { x, y } };
        }
        return node;
      })
    );
  },
});

useFrontendTool({
  name: "updatePlayerPositions",
  description: "Moves players or the ball on the court to new coordinates",
  parameters: [
    {
      name: "movements",
      type: "object[]",
      description: "An array of player movements",
      attributes: [ // בגרסה החדשה לעיתים משתמשים ב-attributes עבור אובייקטים
        { name: "id", type: "string", description: "The ID (p1, p2... ball)" },
        { name: "x", type: "number" },
        { name: "y", type: "number" }
      ],
      required: true,
    },
  ],
  handler: async ({ movements }) => {
    setNodes((nds) =>
      nds.map((node) => {
        const move = movements.find((m: any) => m.id === node.id);
        return move ? { ...node, position: { x: move.x, y: move.y } } : node;
      })
    );
  },
});

  return (
    <div className="relative w-full h-[600px] bg-[#1a1a1a] rounded-xl overflow-hidden border-2 border-zinc-800 shadow-2xl">
      <ReactFlow
      nodes={nodes}
      nodeTypes={nodeTypes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      nodesDraggable={true}
      elementsSelectable={true}
      nodesConnectable={false}
      
      // Prevent all panning and zooming
      panOnDrag={false}
      panOnScroll={false}
      preventScrolling={true}
      zoomOnScroll={false}
      zoomOnPinch={false}
      zoomOnDoubleClick={false}
      
      // Set boundaries
      translateExtent={[[0, 0], [COURT_WIDTH, COURT_HEIGHT]]}
      nodeExtent={[[0, 0], [COURT_WIDTH, COURT_HEIGHT]]}
      
      // Lock viewport position and zoom
      defaultViewport={{ x: 0, y: 0, zoom: 1 }}
      minZoom={1}
      maxZoom={1}
      
      style={{ width: '100%', height: '100%' }}
    >
        {}
        <div 
          className="absolute inset-0 z-0 pointer-events-none opacity-60"
          style={{
            backgroundImage: `url('/basketball-court.svg')`,
            backgroundSize: '90%',
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'center top',
            width: '100%',
            height: '100%',
            filter: 'invert(1) brightness(0.8)', 
            clipPath: 'inset(0 0 0 0)',
          }}
        />

        <Background color="#333" gap={20} />
        <Controls />
        
        {}
        <Panel position="top-right" className="bg-black/60 p-2 rounded border border-white/10 text-xs text-gray-400 backdrop-blur-md">
          Tactical View: Half Court
        </Panel>
      </ReactFlow>
    </div>
  );
}