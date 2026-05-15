# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a monorepo for English learning tools and content, containing multiple projects managed via Yarn workspaces:

- **enjoy/** - Electron desktop app for English learning (TypeScript, React, Electron Forge)
- **1000-hours/** - VitePress documentation site for the "1000 hours" English learning method  
- **1000h-portal/** - Nuxt 3 static site for portal/marketing content
- **learning-notes/** - Personal English learning materials (Markdown, built with MkDocs Material)
- **book/** - Original "人人都能用英语" book content
- **scripts/** - Python scripts for processing vocabulary and subtitle data

## Common Development Commands

### Root Workspace Commands
```bash
# Install dependencies (runs from root)
yarn install

# Enjoy app development
yarn enjoy:dev              # Development mode with hot reload
yarn enjoy:start           # Start production build
yarn enjoy:test            # Run all E2E tests
yarn enjoy:test:main       # Run main process tests
yarn enjoy:test:renderer   # Run renderer process tests
yarn enjoy:package         # Package the app
yarn enjoy:make           # Build distributables
yarn enjoy:lint           # Run ESLint

# Documentation sites
yarn docs:dev             # Run 1000-hours VitePress dev server
yarn docs:build           # Build 1000-hours for production
yarn docs:preview         # Preview built 1000-hours site

# Portal site
yarn portal:generate      # Generate static Nuxt site
```

### Learning Notes Documentation
```bash
# Local preview of learning-notes (MkDocs Material)
pip install -r requirements-docs.txt
mkdocs serve

# Build for GitHub Pages
mkdocs build
```

## Architecture

### Enjoy App (Electron)
- **Main Process** (`enjoy/src/main/`): Node.js backend, database operations, API integrations
- **Renderer Process** (`enjoy/src/renderer/`): React frontend with TypeScript
- **Build System**: Electron Forge with Vite plugin
- **Testing**: Playwright E2E tests in `enjoy/e2e/`
- **UI**: Tailwind CSS with Radix UI components
- **Database**: SQLite with Sequelize ORM

### 1000-hours (VitePress)
- Vue 3 + VitePress static site generator
- Markdown content in `1000-hours/` subdirectories
- Mermaid diagrams support
- Deployed to Cloudflare Workers

### 1000h-portal (Nuxt 3)
- Nuxt 3 static site generation
- Tailwind CSS for styling
- SEO optimization with @nuxtjs/seo

### Learning Notes (MkDocs)
- MkDocs Material theme with Chinese language support
- **Custom Python hooks** (`mkdocs_hooks.py`) convert Obsidian-style wikilinks to regular Markdown links
- Content organized in `learning-notes/` with hierarchical structure
- Built and deployed via GitHub Actions to GitHub Pages

## Code Conventions

### TypeScript Configuration
- Target: ESNext with React JSX
- Path aliases: `@/*`, `@renderer/*`, `@main/*`, `@commands`
- Strict mode enabled
- Decorators enabled for Sequelize

### File Naming
- Use `kebab-case` for all new files and directories
- English file names with Chinese content where appropriate
- Consistent with existing patterns in each workspace

### Obsidian Wikilinks in Learning Notes
- Use full paths from vault root: `[[learning-notes/path/to/file|Display Name]]`
- Custom hooks convert these to relative links during MkDocs build
- Maintain bidirectional links between related notes

### English Learning Content
When working with learning materials, use the custom Cursor skills:
- **english-learning-markdown-docs**: For creating bilingual learning materials
- **subtitle-vocabulary-tables**: For generating vocabulary tables from subtitles

## Testing

### Enjoy App E2E Tests
- Playwright configuration in `enjoy/playwright.config.ts`
- Test files in `enjoy/e2e/`
- Multi-platform testing (macOS, Windows, Linux) via GitHub Actions
- Run tests locally: `yarn enjoy:test`

### CI/CD Pipeline
- **Test workflow**: `.github/workflows/test-enjoy-app.yml`
- **Release workflow**: `.github/workflows/release-enjoy-app.yml`
- **Docs deployment**: `.github/workflows/github-pages.yml`
- **Portal deployment**: Multiple workflows for different environments

## Python Scripts

Scripts in `scripts/` process vocabulary and subtitle data:
- `peppa_*` scripts for Peppa Pig vocabulary processing
- Use Python 3.x with dependencies as needed
- Often used with OCR output and subtitle files

## Development Notes

### Yarn Workspaces
- Root `package.json` defines workspace configuration
- Shared dependencies managed at root level
- Workspace-specific dependencies in respective `package.json` files

### Node Version
- Requires Node.js >= 20.0.0
- Uses Yarn 4.6.0 as package manager

### Build Artifacts
- Electron builds in `enjoy/out/`
- VitePress builds in `1000-hours/.vitepress/dist/`
- MkDocs builds in `site/`
- Nuxt builds in `1000h-portal/.output/`

### Git Workflow
- Main branch: `master`
- Feature branches should follow conventional naming
- Use descriptive commit messages following existing patterns

## Important Files

- `package.json` - Root workspace configuration
- `mkdocs.yml` - MkDocs configuration for learning-notes
- `mkdocs_hooks.py` - Custom hooks for Obsidian wikilink conversion
- `enjoy/forge.config.js` - Electron Forge configuration
- `enjoy/tsconfig.json` - TypeScript configuration with path aliases
- `.cursor/skills/` - Custom Cursor skills for English learning content
