"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import BasketballCourt from '@/src/components/BasketballCourt';

export default function Home() {
  return (
    <CopilotKit 
      runtimeUrl="/api/copilot"
      agent="basketball_coach"
    >
      {}
      <CopilotSidebar
        defaultOpen={true}
        clickOutsideToClose={false} 
        hitEscapeToClose={false}
        onSetOpen={(open) => {
          if (!open) return;
        }}
        instructions="You are a basketball tactical assistant. Help the coach manage players and plays on the court."
        labels={{
          title: "Playbook AI Assistant",
          initial: "שלום קואוץ'! המגרש מוכן. איזה תרגיל נבנה היום?",
        }}
      >
        <main className="min-h-screen bg-black text-white p-8">
          <div className="max-w-6xl mx-auto">
            <header className="mb-8 flex justify-between items-center">
              <div>
                <h1 className="text-4xl font-bold tracking-tighter text-orange-500">PLAYBOOK.AI</h1>
                <p className="text-gray-400">Advanced Tactical Basketball Strategy</p>
              </div>
            </header>

            <div className="grid grid-cols-1 gap-8">
              {}
              <BasketballCourt />
            </div>
          </div>
        </main>
      </CopilotSidebar>
    </CopilotKit>
  );
}