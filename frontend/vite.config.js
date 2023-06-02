import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import dotenv from 'dotenv';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), dotenv.config()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  base: '/graggle-backend/graggle-frontend/'
  
})

