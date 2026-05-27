import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  
  const apiUrl = env.VITE_API_URL;
  if (!apiUrl) {
    console.warn('WARNING: VITE_API_URL is not set. API proxying may fail.');
  }

  return {
    plugins: [react()],
    server: {
      host: true, // Need this for Docker
      port: 5173,
      watch: {
        usePolling: true,
      },
      proxy: apiUrl ? {
        '/api': {
          target: apiUrl,
          changeOrigin: true
        }
      } : {}
    }
  }
})