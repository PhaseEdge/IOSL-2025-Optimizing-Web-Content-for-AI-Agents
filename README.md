# IOSL-2025-2026-Better-Readability-for-LLMs

Branching structure

main                            
├── release                      
│   ├── SPRINT-1                 
│   │   ├── feature/IOSL-1/subs-tier-packages
│   │   ├── improvement/IOSL-2/api-performance
│   │   ├── bugfix/IOSL-3/fix-login-issue
│   │   ├── hotfix/IOSL-4/payment-error
│   │   └── chore/IOSL-5/refactor-legacy-code
│   ├── SPRINT-2
│   │   ├── feature/IOSL-6/user-dashboard
│   │   └── improvement/IOSL-7/cache-optimization
│   └── SPRINT-3
│       └── feature/IOSL-8/new-payment-integration
│
├              
└── development    # Pre-production testing

After each sprint merge current release/SPRINT to main.Then pull request master -> dev. create new release/SPRINT-...
