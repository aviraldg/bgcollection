import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import App from './App';
import * as useBoardgamesModule from './useBoardgames';

// Mock the hook
vi.mock('./useBoardgames', () => ({
  useBoardgames: vi.fn(),
}));

const mockGames = [
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
    box_2d: [10, 10, 100, 100],
    filename: 'image1.jpg',
    location: 'shelf'
  }
];
const mockDesc = { 'image1.jpg': 'Shelf 1' };

describe('App Integration', () => {
  it('renders loading state', () => {
    (useBoardgamesModule.useBoardgames as any).mockReturnValue({
      loading: true,
      boardgames: [],
      imageDescriptions: {},
      error: null
    });

    render(<App />);
    expect(screen.getByText('Loading collection...')).toBeInTheDocument();
  });

  it('renders error state', () => {
    (useBoardgamesModule.useBoardgames as any).mockReturnValue({
      loading: false,
      boardgames: [],
      imageDescriptions: {},
      error: 'Something went wrong'
    });

    render(<App />);
    expect(screen.getByText('Error: Something went wrong')).toBeInTheDocument();
  });

  it('renders main content and handles interaction', async () => {
    (useBoardgamesModule.useBoardgames as any).mockReturnValue({
      loading: false,
      boardgames: mockGames,
      imageDescriptions: mockDesc,
      error: null
    });

    render(<App />);
    
    expect(screen.getByRole('heading', { name: 'Board Game Collection' })).toBeInTheDocument();
    
    // Select image
    const select = screen.getByRole('combobox', { name: 'Select Shelf Image' });
    fireEvent.mouseDown(select);
    fireEvent.click(screen.getByText('Shelf 1'));
    
    expect(screen.getByAltText('Board Game Shelf')).toBeInTheDocument();
    
    // Switch to Global Mode
    const switchControl = screen.getByLabelText('Global Mode (Table View)');
    fireEvent.click(switchControl);
    
    expect(screen.getByRole('grid')).toBeInTheDocument();
    
    // Filter interaction via FilterPanel
    const searchInput = screen.getByLabelText('Search Title');
    fireEvent.change(searchInput, { target: { value: 'Cat' } });
    
    // Check if table filtered? (Table logic is tested in filterGames, but integration check is good)
    expect(screen.getByText('Catan')).toBeInTheDocument();
  });
});
