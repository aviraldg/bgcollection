import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { ImageViewer } from './ImageViewer';

describe('ImageViewer', () => {
    const mockGames = [{
        title: 'Test Game',
        game_id: 1,
        min_players: 1,
        max_players: 4,
        min_playtime: 30,
        max_playtime: 60,
        score: 8.5,
        rank: 10,
        weight: 2.5,
        box_2d: [100, 100, 200, 200],
        filename: 'img.jpg',
        location: 'shelf'
    }];

    it('renders loading state initially', () => {
        render(<ImageViewer imageSrc="img.jpg" games={[]} alwaysShowInfo={false} />);
        expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });

    it('renders image and boxes', () => {
        render(<ImageViewer imageSrc="img.jpg" games={mockGames} alwaysShowInfo={true} />);
        
        const img = screen.getByAltText('Board Game Shelf');
        expect(img).toBeInTheDocument();
        
        // Trigger load
        fireEvent.load(img);
        
        // Should show boxes now? 
        // Logic requires dimensions.
        // ImageViewer uses offsetWidth/Height.
        // In JSDOM, these are 0 by default. we need to mock them.
        
        // We can define properties on the element.
        Object.defineProperty(img, 'offsetWidth', { configurable: true, value: 1024 });
        Object.defineProperty(img, 'offsetHeight', { configurable: true, value: 1024 });
        
        fireEvent.load(img);
        
        // This might not trigger the React onLoad handler if we just called fireEvent.load without the element update? 
        // The component has onLoad={handleLoad}.
        
        // We need to re-render or wait?
        // Actually, firing load event is enough.
        
        expect(screen.getByText('Test Game')).toBeInTheDocument();
    });
});
