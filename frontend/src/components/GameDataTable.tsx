import React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import type { GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import { Button, Link } from '@mui/material';
import type { BoardGame } from '../types';

interface GameDataTableProps {
  games: BoardGame[];
  onViewImage: (filename: string, title?: string) => void;
}

export const GameDataTable: React.FC<GameDataTableProps> = ({ games, onViewImage }) => {
  // Add a unique ID for DataGrid if one doesn't exist (game_id mostly unique, but maybe duplicates per image? no, single entry per game usually)
  // Actually json has multiple entries for same game if it appears in multiple places? "item" logic in index.html suggests it iterates boxes.
  // We should map rows to include a unique ID.
  const rows = games.map((game, index) => ({
    ...game,
    id: `${game.game_id}-${index}`, // composite key
  }));

  const columns: GridColDef[] = [
    {
      field: 'title',
      headerName: 'Title',
      flex: 1,
      minWidth: 200,
      renderCell: (params: GridRenderCellParams) => (
         <Link href={params.row.url || '#'} target="_blank" rel="noopener noreferrer">
           {params.value}
         </Link>
      ),
    },
    { field: 'score', headerName: 'Score', width: 90, type: 'number' },
    { field: 'min_players', headerName: 'Min P', width: 90, type: 'number' },
    { field: 'max_players', headerName: 'Max P', width: 90, type: 'number' },
    { field: 'min_playtime', headerName: 'Min Time', width: 100, type: 'number' },
    { field: 'max_playtime', headerName: 'Max Time', width: 100, type: 'number' },
    { field: 'weight', headerName: 'Complexity', width: 110, type: 'number' },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      renderCell: (params: GridRenderCellParams) => (
        <Button
          variant="contained"
          size="small"
          onClick={() => onViewImage(params.row.filename, params.row.title)}
        >
          Find on Shelf
        </Button>
      ),
    },
  ];

  return (
    <div style={{ height: 600, width: '100%', backgroundColor: 'white' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        initialState={{
          pagination: { paginationModel: { pageSize: 10 } },
        }}
        pageSizeOptions={[10, 25, 50]}
        disableRowSelectionOnClick
      />
    </div>
  );
};
