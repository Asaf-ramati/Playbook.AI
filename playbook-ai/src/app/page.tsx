"use client";

import { CopilotKit, useCoAgent, useCopilotChat } from "@copilotkit/react-core"; // 1. הוספנו את useCopilotChat
import { CopilotSidebar } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import BasketballCourt from '@/src/components/BasketballCourt';
import { StatsTable } from '@/src/components/StatsTable';

interface PlayerData {
  id: string;
  position: { x: number; y: number };
  data: {
    name: string;
    position: string;
    side: 'ATTACK' | 'DEFENSE';
    stats?: { mp: number; pts: number; ast: number; trb: number; };
    color?: string;
  };
}

interface AgentState {
  players: PlayerData[];
  ball_position?: { x: number; y: number } | null;
}

const DashboardContent = () => {
  const { state } = useCoAgent<AgentState>({
    name: "basketball_coach",
    initialState: {
      players: [],
    },
  });

  // 2. שימוש ב-Hook כדי לדעת אם ה-AI חושב כרגע
  const { isLoading } = useCopilotChat();

  return (
    <main className="min-h-screen bg-black text-white p-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold tracking-tighter text-orange-500">PLAYBOOK.AI</h1>
            <p className="text-gray-400">Advanced Tactical Basketball Strategy</p>
          </div>

          {/* 3. אינדיקציה ויזואלית שמופיעה כשה-AI חושב */}
          {isLoading && (
            <div className="flex items-center gap-2 px-4 py-2 bg-gray-800 rounded-full border border-orange-500/50 animate-pulse">
              <div className="w-2 h-2 bg-orange-500 rounded-full animate-bounce" />
              <div className="w-2 h-2 bg-orange-500 rounded-full animate-bounce delay-75" />
              <div className="w-2 h-2 bg-orange-500 rounded-full animate-bounce delay-150" />
              <span className="text-sm font-medium text-orange-400 ml-2">Coach is thinking...</span>
            </div>
          )}
        </header>

        <div className="grid grid-cols-1 gap-6">
          <div className={`border border-gray-800 rounded-lg overflow-hidden transition-opacity duration-300 ${isLoading ? 'opacity-80' : 'opacity-100'}`}>
             <BasketballCourt 
                players={state.players || []} 
                ballPosition={state.ball_position || null}
              />
          </div>

          <StatsTable players={state.players || []} />
        </div>
      </div>
    </main>
  );
};

export default function Home() {
  return (
    <CopilotKit runtimeUrl="/api/copilot" agent="basketball_coach">
      <CopilotSidebar
        defaultOpen={true}
        clickOutsideToClose={false}
        hitEscapeToClose={false}
        instructions="You are a basketball tactical assistant. Help the coach manage players and plays on the court."
        labels={{
          title: "Playbook AI Assistant",
          initial: "Hello Coach! The court is ready. What play should we run today?",
        }}
      >
        <DashboardContent />
      </CopilotSidebar>
    </CopilotKit>
  );
}