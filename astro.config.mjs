import { defineConfig } from 'astro/config';
import react from "@astrojs/react";
import netlify from "@astrojs/netlify";

import partytown from "@astrojs/partytown";

export default defineConfig({
  integrations: [
    react(), 
    partytown(
      {
        config: {
          forward: ["dataLayer.push"],
        },
      }
    )],

  output: "server",
  adapter: netlify()
});