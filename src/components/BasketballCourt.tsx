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
import { COURT_WIDTH, COURT_HEIGHT, STARTING_POSITIONS } from '@/src/lib/constants';
import { useFrontendTool, useCopilotReadable } from "@copilotkit/react-core";

const nodeTypes = {
  player: PlayerNode,
};

const initialNodes = [
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
  {
    id: 'player-1',
    type: 'player',
    position: { x: 200, y: 200 },
    data: { 
      name: 'LeBron James', 
      number: 23, 
      color: '#552583' 
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
        zoomOnPinch={false}
        elementsSelectable={true}
        nodesConnectable={false}
        panOnDrag={false}   
        zoomOnScroll={false}
        translateExtent={[[0, 0], [COURT_WIDTH, COURT_HEIGHT]]}
        nodeExtent={[[0, 0], [COURT_WIDTH, COURT_HEIGHT]]}
        fitView
        
        style={{ width: '100%', height: '100%' }}
      >
        {}
        <div 
          className="absolute inset-0 z-0 pointer-events-none opacity-60"
          style={{
            backgroundImage: `url('/basketball-court.svg')`,
            backgroundSize: 'contain',
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'center top',
            width: '100%',
            height: '100%',
            filter: 'invert(1) brightness(0.8)', 
            transform: 'rotate(0deg)',
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