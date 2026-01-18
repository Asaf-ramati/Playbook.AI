import React from 'react';

// הגדרת המבנה של הנתונים שאנחנו מצפים לקבל
interface PlayerStats {
  mp: number;
  pts: number;
  ast: number;
  trb: number;
  stl?: number;
  blk?: number;
}

interface PlayerNode {
  id: string;
  data: {
    name: string;
    position: string;
    side: 'ATTACK' | 'DEFENSE'; // כדי שנוכל להבדיל או לסנן
    stats?: PlayerStats; // הסטטיסטיקה מגיעה מה-CSV
    color?: string;
  };
}

interface StatsTableProps {
  players: PlayerNode[];
}

export const StatsTable: React.FC<StatsTableProps> = ({ players }) => {
  // סינון: נציג רק את שחקני ההתקפה בטבלה הראשית (אפשר לשנות להציג את כולם)
  // כרגע נציג את כולם אבל נמיין לפי קבוצה (התקפה קודם)
  const sortedPlayers = [...players].sort((a, b) => 
    a.data.side === 'ATTACK' ? -1 : 1
  );

  if (!players || players.length === 0) {
    return <div style={{ color: '#888', textAlign: 'center', marginTop: 20 }}>Waiting for teams...</div>;
  }

  return (
    <div style={styles.container}>
      <h3 style={styles.header}>Live Roster Stats</h3>
      <div style={styles.tableWrapper}>
        <table style={styles.table}>
          <thead>
            <tr style={styles.theadRow}>
              <th style={{ ...styles.th, textAlign: 'left' }}>PLAYER</th>
              <th style={styles.th}>TEAM</th>
              <th style={styles.th}>POS</th>
              <th style={styles.th}>PTS</th>
              <th style={styles.th}>AST</th>
              <th style={styles.th}>REB</th>
            </tr>
          </thead>
          <tbody>
            {sortedPlayers.map((player) => {
              const stats = player.data.stats || { pts: 0, ast: 0, trb: 0 };
              const isAttack = player.data.side === 'ATTACK';
              
              return (
                <tr key={player.id} style={styles.tbodyRow}>
                  <td style={{ ...styles.td, textAlign: 'left', fontWeight: 'bold', color: isAttack ? '#4ade80' : '#f87171' }}>
                    {player.data.name}
                  </td>
                  <td style={styles.td}>
                    <span style={{ 
                      padding: '2px 6px', 
                      borderRadius: '4px', 
                      backgroundColor: isAttack ? 'rgba(74, 222, 128, 0.1)' : 'rgba(248, 113, 113, 0.1)',
                      fontSize: '0.8rem'
                    }}>
                      {player.data.side === 'ATTACK' ? 'OFF' : 'DEF'}
                    </span>
                  </td>
                  <td style={styles.td}>{player.data.position}</td>
                  <td style={styles.td}>{stats.pts}</td>
                  <td style={styles.td}>{stats.ast}</td>
                  <td style={styles.td}>{stats.trb}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// עיצוב בסגנון Inline (כדי שלא תצטרך קבצי CSS נפרדים כרגע)
const styles: Record<string, React.CSSProperties> = {
  container: {
    width: '100%',
    backgroundColor: '#111',
    borderRadius: '12px',
    padding: '16px',
    marginTop: '20px',
    border: '1px solid #333',
    boxShadow: '0 4px 6px rgba(0,0,0,0.3)',
  },
  header: {
    color: '#fff',
    margin: '0 0 12px 0',
    fontSize: '1.2rem',
    borderBottom: '1px solid #333',
    paddingBottom: '8px',
  },
  tableWrapper: {
    overflowX: 'auto',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    fontSize: '0.9rem',
    color: '#ccc',
  },
  theadRow: {
    borderBottom: '2px solid #444',
  },
  th: {
    padding: '10px',
    textAlign: 'center',
    fontWeight: '600',
    color: '#888',
    textTransform: 'uppercase',
    fontSize: '0.75rem',
  },
  tbodyRow: {
    borderBottom: '1px solid #222',
  },
  td: {
    padding: '10px',
    textAlign: 'center',
  },
};