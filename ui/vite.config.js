import { defineConfig } from 'vite'
import Vue from '@vitejs/plugin-vue'
import ElementPlus from 'unplugin-element-plus/vite'

export default defineConfig({
  plugins: [Vue(), ElementPlus()],
  base: './',
})
