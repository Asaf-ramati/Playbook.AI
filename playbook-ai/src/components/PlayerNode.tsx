import React from 'react';
import { Handle, Position } from 'reactflow';

export function PlayerNode({ data }: any) {
  return (
    <div 
      className="relative group h-fit" 
      
      style={{ 
        transition: 'transform 1.5s ease-in-out', 
      }}
    >
      {/* עיגול השחקן */}
      <div 
        className="w-12 h-12 rounded-full border-2 border-white flex items-center justify-center shadow-2xl transition-transform duration-200 group-hover:scale-110 active:scale-95 cursor-grab"
        style={{ 
          backgroundColor: data.color || '#1d428a',
          boxShadow: `0 1px 3px rgba(0,0,0,0.3)`
        }}
      >
       <div className="text-center px-1">
          <span className="text-white font-bold text-[9px] leading-tight select-none block">
            {data.name}
          </span>
        </div>
      </div>

      <Handle type="target" position={Position.Top} className="opacity-0" />
      <Handle type="source" position={Position.Bottom} className="opacity-0" />
    </div>
  );
}