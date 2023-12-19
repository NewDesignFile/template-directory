import { defineConfig } from 'astro/config';
import netlify from "@astrojs/netlify/functions";
import react from "@astrojs/react";

import cloudflare from "@astrojs/cloudflare";

// https://astro.build/config
export default defineConfig({
  output: "server",
  adapter: cloudflare(),
  integrations: [react()]
});