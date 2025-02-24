# Frontend
A modern, responsive frontend built with Next.js, TypeScript, ShadCN and Tailwind CSS for an AI-powered programming education platform that generates coding problems, evaluates submissions, and provides intelligent assistance. This application provides an interactive coding environment where users can practice coding challenges, view problem descriptions, and receive real-time code assistance through a chat interface.


## Overview

The Frontend is designed to work seamlessly with the backend API. It:
- **Displays Coding Challenges:** Shows problem details and test cases.
- **Provides an Interactive Code Editor:** Powered by Monaco Editor for live code editing.
- **Offers a Chat Assistant:** For on-demand coding guidance.
- **Integrates with Submission and Problem Generation APIs:** To fetch challenges and submit code for evaluation.
- **Utilizes Tailwind CSS and ShadCN UI:** For styling and a modern, responsive UI.

---

## Technology Stack

- **Next.js:** React framework for server‑side rendering and static site generation.
- **TypeScript:** Provides type safety across the application.
- **Tailwind CSS:** Utility‑first CSS framework for fast styling.
- **Lucide React:** Icon library for UI components.
- **Monaco Editor:** Code editor component (used in the CodeArena).
- **React & Radix UI:** For building accessible and composable UI components.
- **ESLint & Prettier:** For code linting and formatting.

---

## Environment Setup

### Prerequisites

- **Node.js:** v16 or later (LTS recommended)
- **npm**

### Installation

1. **Clone the repository:**
   ```bash
   git clone ...
   cd  to /frontend
   npm install
   npm run dev

The application will be available at http://localhost:3000.


# Directory Structure

Directory structure:
└── frontend/
    ├── components.json
    ├── next.config.js
    ├── next.config.mjs
    ├── package-lock.json
    ├── package.json
    ├── postcss.config.ms
    ├── tailwind.config.ts
    ├── tsconfig.json
    ├── .gitignore
    ├── public/
    │   └── images/
    ├── services/
    │   └── code-submission.tsx
    └── src/
        ├── app/
        │   ├── globals-bk.css
        │   ├── heading.tsx
        │   ├── layout.tsx
        │   ├── page.tsx
        │   └── fonts/
        │       ├── GeistMonoVF.woff
        │       └── GeistVF.woff
        ├── components/
        │   ├── HelloWorld.tsx
        │   ├── language_mapping.json
        │   ├── codearena/
        │   │   ├── chat-assistant.tsx
        │   │   ├── code-editor.tsx
        │   │   ├── code_arena.tsx
        │   │   ├── common-code-arena.tsx
        │   │   ├── problem-description.tsx
        │   │   └── test-cases.tsx
        │   ├── common/
        │   │   ├── language_mapping.json
        │   │   └── loading-spinner.tsx
        │   ├── program-wise-practice/
        │   │   └── index.tsx
        │   └── ui/
        │       ├── button.tsx
        │       ├── card.tsx
        │       ├── input.tsx
        │       ├── label.tsx
        │       ├── select.tsx
        │       ├── tabs.tsx
        │       ├── timer.tsx
        │       └── tooltip.tsx
        ├── data/
        │   └── program_data.json
        ├── lib/
        │   ├── codeassist-chat-api.ts
        │   ├── fetch_submission_api.ts
        │   ├── get_problem_api.ts
        │   ├── submission_api.ts
        │   └── utils.ts
        ├── services/
        │   └── code-submission.tsx
        └── styles/
            └── globals.css

## Key Files and Components

### Configuration & Environment
- **next.config.js / next.config.mjs:**  
  Configures API rewrites (e.g., forwarding `/api` requests to the backend) and compiler settings.
- **package.json:**  
  Lists project dependencies and defines scripts for development, build, and start.
- **tsconfig.json:**  
  TypeScript configuration ensuring type safety across the project.
- **postcss.config.ms & tailwind.config.ts:**  
  Configure Tailwind CSS along with custom styles and themes (including dark mode support).
- **components.json:**  
  Defines ShadCN UI settings, aliases, and default styling options.

### Core Application Files
- **src/app/layout.tsx & page.tsx:**  
  Set up the global layout, theming, and primary landing page for the application.
- **globals.css**  
  Provide global styling, including Tailwind base styles, custom scrollbars, and theme variables.

### Components
- **Heading (src/app/heading.tsx):**  
  Renders the main header with navigation links and dropdown menus for categories.
- **CodeArena (src/components/codearena/code_arena.tsx):**  
  Combines the interactive code editor and problem description; it also integrates API calls for code submission.
- **Code Editor (src/components/codearena/code-editor.tsx):**  
  Implements the Monaco Editor with live code editing, auto-resizing, and theme switching.
- **Problem Description (src/components/codearena/problem-description.tsx):**  
  Displays the challenge title, description, difficulty, and tags along with a “Next Challenge” action.
- **Test Cases (src/components/codearena/test-cases.tsx):**  
  Shows input examples and expected outputs, along with feedback from code evaluations.
- **Program Wise Practice (src/components/program-wise-practice/index.tsx):**  
  Enables users to select practice topics based on predefined programs, courses, and sprints.

### UI Library Components
- **Button, Card, Input, Label, Select, Tabs, Tooltip, Timer (src/components/ui/*.tsx):**  
  Custom UI components used across the application for a consistent look and feel.

### API & Service Layer
- **codeassist-chat-api.ts (src/lib/codeassist-chat-api.ts):**  
  Contains functions to send chat messages to the backend and stream responses.
- **fetch_submission_api.ts (src/lib/fetch_submission_api.ts):**  
  Polls submission status from the backend.
- **get_problem_api.ts (src/lib/get_problem_api.ts):**  
  Retrieves new coding challenges from the backend.
- **submission_api.ts (src/lib/submission_api.ts):**  
  Sends code submissions for evaluation.
- **code-submission.tsx (src/services/code-submission.tsx):**  
  Wraps submission API calls and manages the end-to-end submission flow.

### Data & Utility Files
- **language_mapping.json (src/components/language_mapping.json):**  
  Maps language names to display metadata (code, file extension, etc.) for proper editor configuration.
- **program_data.json (src/data/program_data.json):**  
  Contains static JSON data used for program-wise practice, including information on programs, courses, and sprints.
- **Utility Functions (src/lib/utils.ts):**  
  Helper functions for class name merging and other common operations.
- **Common Components (e.g., HelloWorld.tsx in src/components/HelloWorld.tsx):**  
  Sample or demonstration components that illustrate basic UI building blocks.

---



