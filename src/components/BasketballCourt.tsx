"use client";

import React, { useCallback } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  useNodesState, 
  useEdgesState,
  Panel
} from 'reactflow';
import 'reactflow/dist/style.css';

import { COURT_WIDTH, COURT_HEIGHT, STARTING_POSITIONS } from '@/src/lib/constants';

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
];

const initialEdges: any[] = [];

export default function BasketballCourt() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  return (
    <div className="relative w-full h-[600px] bg-[#1a1a1a] rounded-xl overflow-hidden border-2 border-zinc-800 shadow-2xl">
      <ReactFlow
        nodes={nodes}
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