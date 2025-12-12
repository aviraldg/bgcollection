import { renderHook, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { useBoardgames } from './useBoardgames';

global.fetch = vi.fn();

describe('useBoardgames', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('fetches data successfully', async () => {
    const mockGames = [{ title: 'Game 1' }];
    const mockDesc = { 'img1.jpg': 'Shelf 1' };

    (global.fetch as any)
      .mockResolvedValueOnce({ ok: true, json: async () => mockGames })
      .mockResolvedValueOnce({ ok: true, json: async () => mockDesc });

    const { result } = renderHook(() => useBoardgames());

    expect(result.current.loading).toBe(true);
    
    await waitFor(() => expect(result.current.loading).toBe(false));

    expect(result.current.boardgames).toEqual(mockGames);
    expect(result.current.imageDescriptions).toEqual(mockDesc);
    expect(result.current.error).toBeNull();
  });

  it('handles fetch error', async () => {
    (global.fetch as any).mockRejectedValue(new Error('Network error'));

    const { result } = renderHook(() => useBoardgames());

    await waitFor(() => expect(result.current.loading).toBe(false));

    expect(result.current.error).toBe('Network error');
  });
  
  it('handles HTTP error', async () => {
     (global.fetch as any).mockResolvedValue({ ok: false });
     
    const { result } = renderHook(() => useBoardgames());
    
    await waitFor(() => expect(result.current.loading).toBe(false));
    
    expect(result.current.error).toBe('Failed to fetch data');
  });
});
