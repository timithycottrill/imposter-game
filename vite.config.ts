import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
export default defineConfig({
  base: './',
  plugins: [react(), VitePWA({
    registerType: 'prompt', injectRegister: 'script',
    manifest: false,
    workbox: { globPatterns: ['**/*.{js,css,html,png,webmanifest}'], navigateFallback: 'index.html', cleanupOutdatedCaches: true, clientsClaim: true, skipWaiting: false },
  })],
});
