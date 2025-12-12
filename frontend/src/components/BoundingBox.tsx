import React from 'react';
import { Tooltip, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';
import type { BoardGame } from '../types';

interface BoundingBoxProps {
  game: BoardGame;
  scaleX: number;
  scaleY: number;
  alwaysShowInfo: boolean;
}

const StyledBox = styled('div')<{ borderColor: string }>(({ borderColor }) => ({
  position: 'absolute',
  border: `2px solid ${borderColor}`,
  cursor: 'pointer',
  opacity: 0.7,
  '&:hover': {
    borderColor: 'blue',
    opacity: 1,
    zIndex: 10,
  },
}));

const InfoTag = styled('div')(() => ({
  position: 'absolute',
  backgroundColor: 'rgba(0, 0, 0, 0.7)',
  color: 'white',
  padding: '3px 5px',
  borderRadius: '3px',
  fontSize: '12px',
  whiteSpace: 'nowrap',
  pointerEvents: 'none',
  transform: 'translateY(-100%)',
  left: 0,
  top: 0,
  zIndex: 20,
}));

export const BoundingBox: React.FC<BoundingBoxProps> = ({ game, scaleX, scaleY, alwaysShowInfo }) => {
  const [y1, x1, y2, x2] = game.box_2d;

  const style = {
    left: x1 * scaleX,
    top: y1 * scaleY,
    width: (x2 - x1) * scaleX,
    height: (y2 - y1) * scaleY,
  };

  const handleClick = () => {
    const url = game.url || 'https://github.com/aviraldg/bgcollection/blob/master/boardgames.json';
    window.open(url, '_blank');
  };

  const isMissingInfo = !game.score && !game.min_players && !game.min_playtime; // Rough check for "missing info"
  const borderColor = 'red';

  const tooltipContent = (
    <div>
      <Typography variant="subtitle2" style={{ fontWeight: 'bold' }}>{game.title}</Typography>
      <Typography variant="body2" style={{ fontSize: '0.8rem' }}>Location: {game.location}</Typography>
      {!isMissingInfo && (
        <Typography variant="caption" display="block">
          ⭐ {game.score} | 👥 {game.min_players}-{game.max_players} | ⏰ {game.min_playtime}-{game.max_playtime}m | 🧠 {game.weight}
        </Typography>
      )}
      {isMissingInfo && <Typography variant="caption">⚠️ Missing Details</Typography>}
    </div>
  );

  return (
    <Tooltip title={!alwaysShowInfo ? tooltipContent : ''} followCursor>
      <StyledBox style={style} onClick={handleClick} borderColor={borderColor}>
         {alwaysShowInfo && (
           <InfoTag>
             <strong>{game.title}</strong><br />
             {game.location}<br />
             {isMissingInfo ? '⚠️' : `⭐ ${game.score} 👥 ${game.min_players}-${game.max_players} ⏰ ${game.min_playtime}m`}
           </InfoTag>
         )}
      </StyledBox>
    </Tooltip>
  );
};
