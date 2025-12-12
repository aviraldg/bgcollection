/// <reference types="vitest" />
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  base: './', // For GitHub Pages
  plugins: [react()],
  test: {
    environment: 'jsdom',
    exclude: ['node_modules', 'tests/**'],
    setupFiles: ['./src/setupTests.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: ['src/**/*.ts', 'src/**/*.tsx'],
      exclude: ['src/main.tsx', 'src/types.ts', 'src/vite-env.d.ts'],
      // @ts-expect-error: 'all' is valid but types might be outdated or strict
      all: true,
    },
    server: {
      deps: {
        inline: ['@mui/x-data-grid'],
      },
    },
  },
})
