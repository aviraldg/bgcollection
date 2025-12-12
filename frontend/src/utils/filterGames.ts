import type { BoardGame } from '../types';
import type { FilterState } from '../components/FilterPanel';

export const filterGames = (games: BoardGame[], filters: FilterState, globalSearchItem?: string): BoardGame[] => {
  return games.filter(game => {
    // Image Check (only if not global search - handled by caller usually, but if globalSearchItem provided, we filter by it)
    if (globalSearchItem && game.filename !== globalSearchItem) return false;

    // Filter Checks
    if (game.score < filters.score[0] || game.score > filters.score[1]) return false;
    
    if (filters.players[0] > 0 && game.min_players < filters.players[0]) return false; // Min constraint
    if (filters.players[1] > 0 && game.max_players > filters.players[1]) return false; // Max constraint

    if (filters.playtime[0] > 0 && game.min_playtime < filters.playtime[0]) return false;
    if (filters.playtime[1] > 0 && game.max_playtime > filters.playtime[1]) return false;

    if (game.weight < filters.complexity[0] || game.weight > filters.complexity[1]) return false;

    if (filters.title && !game.title.toLowerCase().includes(filters.title.toLowerCase())) return false;

    return true;
  });
};
