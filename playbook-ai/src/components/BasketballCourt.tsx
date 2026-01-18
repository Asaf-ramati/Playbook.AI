"use client";

import { PlayerNode } from './PlayerNode';
import React, { useEffect } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  useNodesState, 
  useEdgesState,
  Panel,
  Node,
  OnNodesChange,
  OnEdgesChange
} from 'reactflow';
import 'reactflow/dist/style.css';
import { COURT_WIDTH, COURT_HEIGHT } from '@/src/lib/constants';

// --- הגדרת ה-Props שהרכיב מקבל ---
interface BasketballCourtProps {
  players: any[];         // רשימת השחקנים שמגיעה מ-page.tsx
  ballPosition?: { x: number; y: number } | null; // מיקום הכדור
}

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

// 👇 הרכיב מקבל את הנתונים כ-Props
export default function BasketballCourt({ players, ballPosition }: BasketballCourtProps) {

  // ניהול ה-Nodes הפנימי של ReactFlow (לצורך אנימציות ורינדור)
  const [nodes, setNodes, onNodesChange] = useNodesState([]); 
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  useEffect(() => {
    // בודקים אם קיבלנו מערך שחקנים תקין
    if (players && Array.isArray(players)) {
      
      const gameNodes: any[] = [...players]; 

      // 2. אם יש מיקום לכדור, הוסף אותו כ-Node עצמאי
      if (ballPosition) {
        gameNodes.push({
          id: 'ball',
          type: 'default', 
          data: { label: '🏀' },
          position: ballPosition,
          draggable: false, 
          style: BALL_STYLE,
        });
      }

      // 3. הוסף אנימציה לכולם ועדכן את הלוח
      setNodes(gameNodes.map((node: any) => ({
        ...node,
        style: {
          ...node.style,
          transition: 'all 1.0s ease-in-out', // האנימציה החלקה
        }
      })));
    }
  }, [players, ballPosition, setNodes]); // 👈 מאזינים לשינויים ב-Props

  // הערה: כרגע ביטלתי את עדכון ה-State בגרירה כי ה-State נמצא למעלה.
  // אם תרצה להחזיר גרירה שמעדכנת את ה-AI, נצטרך להעביר פונקציה onPlayerMove מהאבא.
  
  return (
    <div className="relative w-full h-[600px] bg-[#1a1a1a] rounded-xl overflow-hidden border-2 border-zinc-800 shadow-2xl">
      <ReactFlow
        nodes={nodes}
        nodeTypes={nodeTypes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodesDraggable={true} // אפשר לגרור ויזואלית, אבל זה יתאפס בעדכון הבא
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
        <div 
          className="absolute inset-0 z-0 pointer-events-none opacity-60"
          style={{
            backgroundImage: `url('/basketball-court.svg')`,
            backgroundSize: '64%',
            backgroundRepeat: 'no-repeat',
            backgroundPosition: 'center top',
            width: '100%',
            height: '100%',
            filter: 'none', 
            clipPath: 'inset(0 0 0 0)',
          }}
        />

        <Background color="#333" gap={20} />
        <Controls />
        
        <Panel position="top-right" className="bg-black/60 p-2 rounded border border-white/10 text-xs text-gray-400 backdrop-blur-md">
          Tactical View: Half Court
        </Panel>
      </ReactFlow>
    </div>
  );
}