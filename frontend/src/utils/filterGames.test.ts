import { describe, it, expect } from 'vitest';
import { filterGames } from './filterGames';
import { INITIAL_FILTERS } from '../components/FilterPanel';
import type { BoardGame } from '../types';

const mockGames: BoardGame[] = [
  {
    title: 'Gloomhaven',
    game_id: 1,
    min_players: 1,
    max_players: 4,
    min_playtime: 60,
    max_playtime: 120,
    score: 8.5,
    rank: 1,
    weight: 4.0,
    box_2d: [0,0,0,0],
    filename: 'image1.jpg',
    location: 'shelf'
  },
  {
    title: 'Catan',
    game_id: 2,
    min_players: 3,
    max_players: 4,
    min_playtime: 60,
    max_playtime: 90,
    score: 7.0,
    rank: 100,
    weight: 2.3,
    box_2d: [0,0,0,0],
    filename: 'image2.jpg',
    location: 'shelf'
  }
];

describe('filterGames', () => {
  it('should return all games with default filters', () => {
    const result = filterGames(mockGames, INITIAL_FILTERS);
    expect(result).toHaveLength(2);
  });

  it('should filter by title', () => {
    const filters = { ...INITIAL_FILTERS, title: 'gloom' };
    const result = filterGames(mockGames, filters);
    expect(result).toHaveLength(1);
    expect(result[0].title).toBe('Gloomhaven');
  });

  it('should filter by score', () => {
    const filters = { ...INITIAL_FILTERS, score: [8, 10] as [number, number] };
    const result = filterGames(mockGames, filters);
    expect(result).toHaveLength(1);
    expect(result[0].title).toBe('Gloomhaven');
  });

  it('should filter by complexity', () => {
    const filters = { ...INITIAL_FILTERS, complexity: [0, 3] as [number, number] };
    const result = filterGames(mockGames, filters);
    expect(result).toHaveLength(1);
    expect(result[0].title).toBe('Catan');
  });

  it('should filter by player count', () => {
    const filters = { ...INITIAL_FILTERS, players: [2, 10] as [number, number] };
    // Gloomhaven: min 1. Filters min 2. 1 < 2 so Gloomhaven passes?
    // Logic: if (playersMin > 0 && item.min_players < playersMin) return false;
    // item.min_players(1) < playersMin(2) => true, so it returns false (filtered out).
    // Wait, my logic in `filterGames` is `if (filters.players[0] > 0 && game.min_players < filters.players[0]) return false;`
    // So if game.min_players(1) < 2, it is excluded.
    // So Gloomhaven (min 1) should be excluded if I want games that support at least 2 players?
    // No, usually "Min Players" filter means "I have N players, can I play it?".
    // If I have 2 players, I can play Gloomhaven (1-4).
    // But the legacy logic `if (playersMin > 0 && item.min_players < playersMin)` excludes games where min_players < filter.
    // If filter is 2, and game is 1-4. 1 < 2? Yes. So excluded.
    // This implies the legacy filter meant "Minimum players THIS game supports must be at least X".
    // e.g. "I want a game that requires at least 3 players".
    // If that's the legacy logic, I should preserve it, or improve it. Request was "refactor ... maintain functionality".
    // So I will stick to legacy logic in my test expectation.
    // Gloomhaven (min 1) < 2 -> Excluded.
    // Catan (min 3) < 2 -> False (Included).
    
    // Wait, checked legacy logic:
    // `if (playersMin > 0 && item.min_players < playersMin) return false;`
    // item.min_players < playersMin.
    // If I set filter=2. Gloomhaven=1. 1 < 2 is True. Returns false. Excluded.
    // This seems to filter out games that *can* be played with fewer people.
    // It selects games that *require* at least X players.
    
    // Let's verify expectation.
    const result = filterGames(mockGames, filters);
    expect(result).toHaveLength(1);
    expect(result[0].title).toBe('Catan');
  });
});
