"use client";
import { PlayerNode } from './PlayerNode';
import React, { useEffect } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  useNodesState, 
  useEdgesState,
  Panel
} from 'reactflow';
import 'reactflow/dist/style.css';
import { COURT_WIDTH, COURT_HEIGHT } from '@/src/lib/constants';
import { useCoAgent } from "@copilotkit/react-core";

const nodeTypes = {
  player: PlayerNode,
};

const BALL_STYLE = { 
  borderRadius: '50%', 
  width: 20, 
  height: 20, 
  display: 'flex', 
  justifyContent: 'center', 
  alignItems: 'center', 
  backgroundColor: '#ff8c00',
  color: '#fff',
  fontSize: '16px',
  zIndex: 1000 
};

export default function BasketballCourt() {

  const { state, setState } = useCoAgent({
    name: "basketball_coach", 
    initialState: {
      players: [],         // מתחילים ריק
      ball_position: null, // אין כדור עדיין
    },
  });

  // מתחילים עם מערך ריק במקום initialNodes
  const [nodes, setNodes, onNodesChange] = useNodesState([]); 
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

useEffect(() => {
    if (state.players) {
      // 👇 התיקון כאן: הוספנו : any[]
      // זה אומר ל-TS: "אל תדאג, זה מערך שאפשר להוסיף לו דברים"
      const gameNodes: any[] = [...state.players]; 

      // 2. אם יש מיקום לכדור, הוסף אותו כ-Node עצמאי
      if (state.ball_position) {
        gameNodes.push({
          id: 'ball',
          type: 'default', 
          data: { label: '🏀' },
          position: state.ball_position,
          draggable: false, 
          style: BALL_STYLE,
        });
      }

      // 3. הוסף אנימציה לכולם ועדכן את הלוח
      setNodes(gameNodes.map((node: any) => ({
        ...node,
        style: {
          ...node.style,
          transition: 'all 1.0s ease-in-out', 
        }
      })));
    }
  }, [state.players, state.ball_position, setNodes]);
  // עדכון ה-AI כשגוררים שחקן ידנית
  const onNodeDragStop = (_: any, node: any) => {
    // אם גררו את הכדור - לא מעדכנים שחקן (אופציונלי: אפשר לממש גרירת כדור)
    if (node.id === 'ball') return;

    setState((prev: any) => ({
      ...prev,
      players: prev.players.map((n: any) => 
        n.id === node.id ? { ...n, position: node.position } : n
      ),
    }));
  };

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
            backgroundSize: '64%',
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