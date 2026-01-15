import React from 'react';
import { Handle, Position } from 'reactflow';

export function PlayerNode({ data }: any) {
  return (
    <div className="flex flex-col items-center group h-fit">
      {}
      <div 
        className="w-5 h-5 rounded-full border-2 border-white flex items-center justify-center shadow-2xl transition-transform duration-200 group-hover:scale-110 active:scale-95 cursor-grab"
        style={{ 
          backgroundColor: data.color || '#1d428a',
          boxShadow: `0 1px 3px rgba(0,0,0,0.3)`
        }}
      >
        {}
        <span className="text-white font-black text-[8px] select-none leading-none">
          {data.number}
        </span>
      </div>
      
      {}
      <div className="mt-0.5 leading-none">
        <span className="bg-[#0f172a]/90 text-white text-[5px] font-bold px-1 py-[1px] rounded-[2px] border border-white/10 whitespace-nowrap shadow-sm select-none block">
          {data.name}
        </span>
      </div>

      {}
      <Handle type="target" position={Position.Top} className="opacity-0" />
      <Handle type="source" position={Position.Bottom} className="opacity-0" />
    </div>
  );
}