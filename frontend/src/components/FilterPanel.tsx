import React from 'react';
import { Box, Typography, TextField, Slider, Button, Paper } from '@mui/material';

export interface FilterState {
  title: string;
  score: [number, number];
  players: [number, number];
  playtime: [number, number];
  complexity: [number, number];
}

export const INITIAL_FILTERS: FilterState = {
  title: '',
  score: [0, 10],
  players: [0, 10], // Assuming realistic max
  playtime: [0, 240], // Minutes
  complexity: [0, 5],
};

interface FilterPanelProps {
  filters: FilterState;
  onFilterChange: (newFilters: FilterState) => void;
}

export const FilterPanel: React.FC<FilterPanelProps> = ({ filters, onFilterChange }) => {
  const handleChange = (key: keyof FilterState, value: any) => {
    onFilterChange({ ...filters, [key]: value });
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
      <Typography variant="h6" gutterBottom>Filters</Typography>
      
      <Box mb={2}>
        <TextField
          label="Search Title"
          fullWidth
          variant="outlined"
          value={filters.title}
          onChange={(e) => handleChange('title', e.target.value)}
        />
      </Box>

      <Box mb={2}>
        <Typography gutterBottom>Score ({filters.score[0]} - {filters.score[1]})</Typography>
        <Slider
          value={filters.score}
          onChange={(_, val) => handleChange('score', val)}
          valueLabelDisplay="auto"
          min={0}
          max={10}
          step={0.1}
        />
      </Box>

      <Box mb={2}>
        <Typography gutterBottom>Players ({filters.players[0]} - {filters.players[1]}+)</Typography>
        <Slider
          value={filters.players}
          onChange={(_, val) => handleChange('players', val)}
          valueLabelDisplay="auto"
          min={0}
          max={20}
        />
      </Box>

      <Box mb={2}>
        <Typography gutterBottom>Playtime ({filters.playtime[0]}m - {filters.playtime[1]}m)</Typography>
        <Slider
          value={filters.playtime}
          onChange={(_, val) => handleChange('playtime', val)}
          valueLabelDisplay="auto"
          min={0}
          max={300}
          step={15}
        />
      </Box>

       <Box mb={2}>
        <Typography gutterBottom>Complexity ({filters.complexity[0]} - {filters.complexity[1]})</Typography>
        <Slider
          value={filters.complexity}
          onChange={(_, val) => handleChange('complexity', val)}
          valueLabelDisplay="auto"
          min={0}
          max={5}
          step={0.1}
        />
      </Box>

      <Button variant="outlined" onClick={() => onFilterChange(INITIAL_FILTERS)}>Reset Filters</Button>
    </Paper>
  );
};
