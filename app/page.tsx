import BasketballCourt from '@/src/components/BasketballCourt';

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white p-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold tracking-tighter text-orange-500">PLAYBOOK.AI</h1>
            <p className="text-gray-400">Advanced Tactical Basketball Strategy</p>
          </div>
        </header>

        <div className="grid grid-cols-1 gap-8">
          <BasketballCourt />
        </div>
      </div>
    </main>
  );
}