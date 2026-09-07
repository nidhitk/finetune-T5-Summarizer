import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, ".", "");
  const port = Number(env.VITE_DEV_PORT);

  return {
    plugins: [react()],
    server: {
      ...(Number.isFinite(port) && port > 0 ? { port } : {}),
    },
  };
});
