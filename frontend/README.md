# Frontend 🎨

This directory contains the Vue 3 application that talks to the Paperhub API. Vite handles the build process while Bun manages dependencies.

## Tech stack

- **Vue 3** 🖖
- **Vite** ⚡
- **PrimeVue** UI components 🌟
- **Pinia** for state management 🍍
- **Bun** as runtime and package manager 🍞

## Installation

1. `cd frontend`
2. Install dependencies:
   ```bash
   bun install
   ```
3. Copy `.env.example` to `.env` and set the API URL and Firebase credentials.

## Development

Run the dev server:
```bash
bun dev
```

## Production build

```bash
bun run build
```

Lint the project with:
```bash
bun lint
```
