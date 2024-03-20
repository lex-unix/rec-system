import { preprocessMeltUI, sequence } from '@melt-ui/pp';
import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
/** @type {import('@sveltejs/kit').Config}*/
const config = {
  preprocess: sequence([vitePreprocess(), preprocessMeltUI()]),
  kit: {
    adapter: adapter(),
    alias: {
      $components: './ui/src/lib/components',
      $transitions: './ui/src/lib/transitions'
    },
    files: {
      assets: './ui/static',
      lib: './ui/src/lib',
      routes: './ui/src/routes',
      appTemplate: './ui/src/app.html',
      errorTemplate: './ui/src/error.html'
    }
  }
};
export default config;
