import React, { useState, useRef, useEffect } from 'react';
import { Box, CircularProgress } from '@mui/material';
import type { BoardGame } from '../types';
import { BoundingBox } from './BoundingBox';

interface ImageViewerProps {
  imageSrc: string;
  games: BoardGame[];
  alwaysShowInfo: boolean;
}

export const ImageViewer: React.FC<ImageViewerProps> = ({ imageSrc, games, alwaysShowInfo }) => {
  const [loaded, setLoaded] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);
  const [dimensions, setDimensions] = useState<{ width: number; height: number } | null>(null);

  useEffect(() => {
    setLoaded(false);
    setDimensions(null);
  }, [imageSrc]);

  const handleLoad = () => {
    setLoaded(true);
  };

  useEffect(() => {
    if (loaded && imgRef.current) {
        setDimensions({
          width: imgRef.current.offsetWidth,
          height: imgRef.current.offsetHeight,
        });
    }
  }, [loaded]);

  // Recalculate dimensions on resize
  useEffect(() => {
    const handleResize = () => {
      if (imgRef.current) {
        setDimensions({
          width: imgRef.current.offsetWidth,
          height: imgRef.current.offsetHeight,
        });
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Assuming original image size is 1024x1024 as per legacy code comments
  // "actualImageScaleX = displayWidth / 1024"
  const scaleX = dimensions ? dimensions.width / 1024 : 1;
  const scaleY = dimensions ? dimensions.height / 1024 : 1;

  return (
    <Box position="relative" width="100%" maxWidth="1200px" margin="0 auto" boxShadow={3} bgcolor="white">
      {!loaded && (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="500px">
          <CircularProgress />
        </Box>
      )}
      <img
        ref={imgRef}
        src={imageSrc}
        alt="Board Game Shelf"
        style={{ width: '100%', height: 'auto', display: loaded ? 'block' : 'none' }}
        onLoad={handleLoad}
      />
      {loaded && dimensions && games.map(game => (
        <BoundingBox
          key={`${game.game_id}-${game.filename}-${game.box_2d.join(',')}`}
          game={game}
          scaleX={scaleX}
          scaleY={scaleY}
          alwaysShowInfo={alwaysShowInfo}
        />
      ))}
    </Box>
  );
};
