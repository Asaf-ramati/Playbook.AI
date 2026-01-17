"use client";

import { CopilotKit, useCoAgent } from "@copilotkit/react-core"; // 👈 הוספנו useCoAgent
import { CopilotSidebar } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import BasketballCourt from '@/src/components/BasketballCourt';
import { StatsTable } from '@/src/components/StatsTable'; // 👈 הייבוא של הטבלה החדשה

// הגדרת טיפוס המידע שמגיע מהסוכן (אפשר גם בקובץ נפרד types.ts)
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

// קומפוננטה פנימית כדי להשתמש ב-Hook בתוך ה-Provider
const DashboardContent = () => {
  // 👇 כאן אנחנו מושכים את המידע מהסוכן
  const { state } = useCoAgent<AgentState>({
    name: "basketball_coach",
    initialState: {
      players: [],
    },
  });

  return (
    <main className="min-h-screen bg-black text-white p-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold tracking-tighter text-orange-500">PLAYBOOK.AI</h1>
            <p className="text-gray-400">Advanced Tactical Basketball Strategy</p>
          </div>
        </header>

        <div className="grid grid-cols-1 gap-6">
          {/* המגרש מקבל את השחקנים כ-Prop */}
          <div className="border border-gray-800 rounded-lg overflow-hidden">
             <BasketballCourt 
                players={state.players || []} 
                ballPosition={state.ball_position || null}
              />
          </div>

          {/* הטבלה מקבלת את אותם שחקנים בדיוק */}
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
          initial: "שלום קואוץ'! המגרש מוכן. איזה תרגיל נבנה היום?",
        }}
      >
        <DashboardContent />
      </CopilotSidebar>
    </CopilotKit>
  );
}