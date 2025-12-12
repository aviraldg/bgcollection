import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { FilterPanel, INITIAL_FILTERS } from './FilterPanel';
import type { FilterState } from './FilterPanel';

describe('FilterPanel', () => {
  it('renders all filter inputs', () => {
    render(<FilterPanel filters={INITIAL_FILTERS} onFilterChange={() => {}} />);
    
    expect(screen.getByLabelText('Search Title')).toBeInTheDocument();
    expect(screen.getByText(/Score/)).toBeInTheDocument();
    expect(screen.getByText(/Players/)).toBeInTheDocument();
    expect(screen.getByText(/Playtime/)).toBeInTheDocument();
    expect(screen.getByText(/Complexity/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Reset Filters' })).toBeInTheDocument();
  });

  it('calls onFilterChange when title changes', () => {
    const handleChange = vi.fn();
    render(<FilterPanel filters={INITIAL_FILTERS} onFilterChange={handleChange} />);
    
    const input = screen.getByLabelText('Search Title');
    fireEvent.change(input, { target: { value: 'Catan' } });
    
    expect(handleChange).toHaveBeenCalledWith({
      ...INITIAL_FILTERS,
      title: 'Catan'
    });
  });

  it('calls onFilterChange when reset is clicked', () => {
     const handleChange = vi.fn();
     const modifiedFilters: FilterState = { ...INITIAL_FILTERS, title: 'Modified' };
     render(<FilterPanel filters={modifiedFilters} onFilterChange={handleChange} />);
     
     const button = screen.getByRole('button', { name: 'Reset Filters' });
     fireEvent.click(button);
     
     expect(handleChange).toHaveBeenCalledWith(INITIAL_FILTERS);
  });

  it('calls onFilterChange when sliders change', () => {
    const handleChange = vi.fn();
    render(<FilterPanel filters={INITIAL_FILTERS} onFilterChange={handleChange} />);
    
    // Sliders are tricky to test directly with fireEvent.change on the input[type=range].
    // MUI Sliders render hidden inputs.
    
    // Score Slider
    const scoreInputs = screen.getAllByRole('slider');
    // We have 4 sliders * 2 handles each (range) = 8 handles? 
    // Or maybe just inputs.
    // Let's target by name if possible? No name prop.
    // We can target by looking at the structure or simple inputs.
    
    // MUI Slider hidden input: <input type="range" ... value="0" ... >
    // We can filter by max value or something?
    
    // Let's try to just fire change on the first slider input found for Score (0-10)
    // Actually, getting by role 'slider' returns the thumb usually.
    
    // Let's use fireEvent.change on the hidden input.
    // Score is the first one.
    // But there are two thumbs (min/max).
    
    // Let's just assume we can find them.
    // Using a more robust approach:
    // We know the order: Score, Players, Playtime, Complexity.
    
    const sliders = screen.getAllByRole('slider');
    // Each range slider has 2 thumbs. So 0,1 are Score. 2,3 are Players. etc.
    
    // Change Score Max (index 1)
    fireEvent.change(sliders[1], { target: { value: 8 } });
    expect(handleChange).toHaveBeenCalled();
    
    // Change Player Min (index 2)
    fireEvent.change(sliders[2], { target: { value: 2 } });
    expect(handleChange).toHaveBeenCalled();
    
    // Change Playtime Max (index 5) (Playtime range 0-240)
    // 0,1 Score; 2,3 Players; 4,5 Playtime; 6,7 Complexity
    fireEvent.change(sliders[5], { target: { value: 60 } });
    expect(handleChange).toHaveBeenCalled();
    
    // Change Complexity Max (index 7) (0-5)
    fireEvent.change(sliders[7], { target: { value: 4 } });
    expect(handleChange).toHaveBeenCalled();
  });
});
