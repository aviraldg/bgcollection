export interface BoardGame {
  title: string;
  game_id: number;
  min_players: number;
  max_players: number;
  min_playtime: number;
  max_playtime: number;
  score: number;
  rank: number | string;
  weight: number;
  box_2d: [number, number, number, number]; // [y1, x1, y2, x2] based on index.html usage
  filename: string;
  location: string;
  url?: string;
}

export interface ImageDescriptions {
  [filename: string]: string;
}
