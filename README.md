# Project: Better Readability for LLMs

This project is an experimental framework to investigate and improve how Large Language Models (LLMs) comprehend web content. We use a backend pipeline to systematically evaluate the performance of different AI models (e.g., from OpenAI, Google, and Ollama) on question-answering tasks using transformed web content. The goal is to identify which content structures and formats yield the best machine readability and understanding.

## Project Structure

The repository is organized into the following key directories:

- **/src**: Contains the source code for the frontend application.
- **/backend**: Includes the Python-based backend evaluation pipeline, helper classes, and configuration files.
- **/public**: Holds public assets for the frontend.
- **/evaluate**: Contains evaluation scripts and results.

## Getting Started

Below are the instructions to set up and run both the frontend and backend components of the project.

### Frontend Setup

The frontend is a Node.js application. Follow these steps to run it locally.

**Prerequisites:**
- Node.js

**Installation and Execution:**

1.  Install the necessary packages:
    ```bash
    npm install
    ```

2.  Start the development server:
    ```bash
    npm run dev
    ```
    On Windows, you may need to use:
    ```bash
    npm run dev:win
    ```
    The application will be available in your browser, and the page will automatically reload upon saving changes.

### Backend Setup

The backend is a Python-based pipeline for crawling websites and evaluating LLM-generated content. It supports models from Gemini, OpenAI, and Ollama.

For detailed instructions on how to configure the environment, set up API keys, and run the evaluation, please refer to the dedicated backend documentation:

**[Backend README](./backend/README.md)**

## Branching Strategy

The project follows a Gitflow-like branching model to manage development and releases.

- **main**: The primary production-ready branch.
- **development**: Pre-production branch for testing integrated features.
- **release/SPRINT-***: Branches for managing sprint-based releases. Features, bugfixes, and improvements are merged here before being integrated into `development` and `main`.

**Workflow:**
1.  Develop features on branches off `release/SPRINT-*` (e.g., `feature/IOSL-1/...`).
2.  Merge completed features into the current sprint release branch.
3.  After a sprint, merge the release branch into `main`.
4.  Update the `development` branch from `main` to ensure it has the latest production code.
5.  Create a new `release/SPRINT-*` branch for the next sprint's work.
