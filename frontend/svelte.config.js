import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter({
      pages: 'dist',
      assets: 'dist',
      fallback: 'index.html',
      precompress: false,
      strict: true
    }),
    alias: {
      $lib: 'src/lib',
      $components: 'src/lib/components'
    },
    prerender: {
      handleHttpError: ({ path, referrer, message }) => {
        // Ignore missing favicon and other static assets
        if (path === '/favicon.png' || path === '/favicon.ico') {
          return;
        }
        throw new Error(message);
      }
    }
  }
};

export default config;
