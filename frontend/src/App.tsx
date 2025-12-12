import { useState, useEffect, useMemo } from 'react';
import {
  Container, CssBaseline, Box, Typography,
  FormControl, InputLabel, Select, MenuItem,
  FormControlLabel, Switch
} from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useBoardgames } from './useBoardgames';
import { FilterPanel, INITIAL_FILTERS } from './components/FilterPanel';
import type { FilterState } from './components/FilterPanel';
import { filterGames } from './utils/filterGames';
import { GameDataTable } from './components/GameDataTable';
import { ImageViewer } from './components/ImageViewer';

const theme = createTheme({
  palette: {
    primary: { main: '#1976d2' },
    secondary: { main: '#dc004e' },
    background: { default: '#f4f4f4' },
  },
});

function App() {
  const { boardgames, imageDescriptions, loading, error } = useBoardgames();

  // State
  const [selectedImage, setSelectedImage] = useState<string>('');
  const [filters, setFilters] = useState<FilterState>(INITIAL_FILTERS);
  const [globalSearch, setGlobalSearch] = useState<boolean>(false);
  const [alwaysDisplayInfo, setAlwaysDisplayInfo] = useState<boolean>(true);

  // Load state from localStorage on mount
  useEffect(() => {
    const savedImage = localStorage.getItem('selectedImage');
    if (savedImage) setSelectedImage(savedImage);

    const savedFilters = localStorage.getItem('filters');
    if (savedFilters) {
      try {
        setFilters(JSON.parse(savedFilters));
      } catch (e) {
        console.error('Failed to parse saved filters', e);
      }
    }

    const savedGlobalSearch = localStorage.getItem('globalSearchChecked');
    if (savedGlobalSearch) setGlobalSearch(savedGlobalSearch === 'true');

    const savedDisplayInfo = localStorage.getItem('alwaysDisplayInfo');
    if (savedDisplayInfo) setAlwaysDisplayInfo(savedDisplayInfo === 'true');
  }, []);

  // Save state to localStorage on change
  useEffect(() => { localStorage.setItem('selectedImage', selectedImage); }, [selectedImage]);
  useEffect(() => { localStorage.setItem('filters', JSON.stringify(filters)); }, [filters]);
  useEffect(() => { localStorage.setItem('globalSearchChecked', String(globalSearch)); }, [globalSearch]);
  useEffect(() => { localStorage.setItem('alwaysDisplayInfo', String(alwaysDisplayInfo)); }, [alwaysDisplayInfo]);

  // Derived Data
  const uniqueImages = useMemo(() => {
    return Array.from(new Set(boardgames.map(bg => bg.filename))).sort();
  }, [boardgames]);

  const filteredGames = useMemo(() => {
    return filterGames(boardgames, filters, globalSearch ? undefined : selectedImage);
  }, [boardgames, selectedImage, filters, globalSearch]);

  const handleImageSelect = (event: any) => {
    setSelectedImage(event.target.value as string);
  };

  const handleViewImageFromTable = (filename: string, title?: string) => {
    setGlobalSearch(false);
    setSelectedImage(filename);
    if (title) {
        setFilters(prev => ({ ...prev, title: title }));
    }
  };

  if (loading) return <Box p={4} display="flex" justifyContent="center"><Typography>Loading collection...</Typography></Box>;
  if (error) return <Box p={4} display="flex" justifyContent="center" color="error.main"><Typography>Error: {error}</Typography></Box>;

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Typography variant="h3" component="h1" align="center" gutterBottom>
          Board Game Collection
        </Typography>

        <Box display="flex" flexWrap="wrap" gap={3}>
          {/* Controls Area */}
          <Box width={{ xs: '100%', md: '25%' }} minWidth="250px" sx={{ flexShrink: 0 }}>
             <Box mb={2}>
               <FormControlLabel
                 control={<Switch checked={globalSearch} onChange={(e) => setGlobalSearch(e.target.checked)} />}
                 label="Global Mode (Table View)"
               />
             </Box>
             
             <Box mb={2}>
                <FormControl fullWidth disabled={globalSearch}>
                  <InputLabel id="image-select-label">Select Shelf Image</InputLabel>
                  <Select
                    labelId="image-select-label"
                    value={selectedImage}
                    label="Select Shelf Image"
                    onChange={handleImageSelect}
                  >
                    <MenuItem value=""><em>None</em></MenuItem>
                    {uniqueImages.map(filename => (
                      <MenuItem key={filename} value={filename}>
                        {imageDescriptions[filename] || filename}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
             </Box>

             <Box mb={2}>
               <FormControlLabel
                 disabled={globalSearch}
                 control={<Switch checked={alwaysDisplayInfo} onChange={(e) => setAlwaysDisplayInfo(e.target.checked)} />}
                 label="Always Display Info Tags"
               />
             </Box>

             <FilterPanel filters={filters} onFilterChange={setFilters} />
          </Box>

          {/* Main Display Area */}
          <Box flexGrow={1} minWidth={0} width={{ xs: '100%', md: '70%' }}>
            {globalSearch ? (
              <GameDataTable games={filteredGames} onViewImage={handleViewImageFromTable} />
            ) : (
              selectedImage ? (
                <ImageViewer
                  imageSrc={selectedImage}
                  games={filteredGames}
                  alwaysShowInfo={alwaysDisplayInfo}
                />
              ) : (
                <Box display="flex" justifyContent="center" alignItems="center" height="400px" border="1px dashed #ccc">
                  <Typography variant="h6" color="textSecondary">Select an image to view shelves</Typography>
                </Box>
              )
            )}
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
