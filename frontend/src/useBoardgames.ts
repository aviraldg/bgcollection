import { useState, useEffect } from 'react';
import type { BoardGame, ImageDescriptions } from './types';

export const useBoardgames = () => {
  const [boardgames, setBoardgames] = useState<BoardGame[]>([]);
  const [imageDescriptions, setImageDescriptions] = useState<ImageDescriptions>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const baseUrl = import.meta.env.BASE_URL;
        const [bgResponse, descResponse] = await Promise.all([
          fetch(`${baseUrl}boardgames.json`),
          fetch(`${baseUrl}image_descriptions.json`)
        ]);

        if (!bgResponse.ok || !descResponse.ok) {
          throw new Error('Failed to fetch data');
        }

        const bgData = await bgResponse.json();
        const descData = await descResponse.json();

        setBoardgames(bgData);
        setImageDescriptions(descData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { boardgames, imageDescriptions, loading, error };
};
