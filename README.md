# IOSL-2025-2026-Better-Readability-for-LLMs

\*\*\* Requirements:

1. Node.js

\*\*\* To start the project

1. npm install
2. npm run dev (browser sync -> it will reload the content whenever you make changes and save them)

Branching structure

main # Main production branch
├── release # Sprint-based releases
│ ├── SPRINT-1 # Current active sprint
│ │ ├── feature/IOSL-1/subs-tier-packages
│ │ ├── improvement/IOSL-2/api-performance
│ │ ├── bugfix/IOSL-3/fix-login-issue
│ │ ├── hotfix/IOSL-4/payment-error
│ │ └── chore/IOSL-5/refactor-legacy-code
│ ├── SPRINT-2
│ │ ├── feature/IOSL-6/user-dashboard
│ │ └── improvement/IOSL-7/cache-optimization
│ └── SPRINT-3
│ └── feature/IOSL-8/new-payment-integration
│
├── development # Pre-production testing

After each sprint merge current release/SPRINT to main.Then pull request master -> dev. create new release/SPRINT-...
