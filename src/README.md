# Frontend General Design

This frontend is designed to showcase structured HTML content enhanced with semantic metadata using JSON-LD, Microdata, and their combination. It simulates real-world content scenarios like articles and data tables, distributed across multiple structured pages. This content is later evaluated using LLMs in a separate backend pipeline.

## Features

- **Structured Data Variants**: Structured Data Variants: Each content page is available in JSON-LD, Microdata, and JSON-LD+Microdata formats.
- **Thematic Page Groups**: Supports pages for fictional countries, inland articles, and data tables.
- **LLM-Ready Content**: Each article and table page includes an optional llm.txt to support alternative model-ready content.
- **Scalable Structure**: Pages are organized into well-separated folders for easy navigation and backend crawling.
- **Clean CSS Integration**: A shared stylesheet ensures consistent styling across all HTML files.

## Workflow

The diagram below illustrates the complete workflow of the evaluation pipeline.

```mermaid
graph TD
    A([Start]) --> B{Load Page Types};
    B --> C[Fictional Country Pages];
    B --> D[Inland Articles];
    B --> E[Table Pages];
    C --> C1[pageFurkan.html];
    C1 --> C2[imaginaryCountry Variants];
    D --> D1[inland.html];
    D1 --> D2[inlandArticle{1..5}/];
    D2 --> D3[llm.txt files];
    E --> E1[pages-with-table/];
    E1 --> E2[tablePage1 + Variants];
    E1 --> E3[tablePage1WithPagination + Variants];
```

## Pages Created With Their Creators

    frontend/
    ├── css/
    │   └── style.css (Furkan)
    ├── pageColin.html
    ├── pageFurkan.html
    ├── imaginaryCountry.html (Furkan)
    ├── imaginaryCountryJSONLD.html (Furkan)
    ├── imaginaryCountryMicrodata.html (Furkan)
    ├── imaginaryCountryJSONLDandMicrodata.html (Furkan)
    ├── inland.html (Furkan and Sofia)
    ├── pages/
    │   ├── inland-new-pages/
    │   │   ├──inlandMainPage{1..5}/ (Furkan)
    │   │   └──inlandArticle{1..5}/ (Furkan and Sofia)
    │   │       ├── inlandArticleX.html (Sofia and Furkan)
    │   │       ├── llm.txt (Furkan)
    │   │       ├── inlandArticleXJSONLDandMicrodata.html (Furkan)
    │   │       ├── inlandArticleXMicrodata.html (Furkan)
    │   │       └── inlandArticleXJSONLD.html (Sofia)
    │   └── pages-with-table/ (Furkan)
    │       ├── tablePage1/
    │       │   ├── tablePage1.html (Furkan)
    │       │   ├── tablePage1-json-ld.html (Furkan)
    │       │   ├── tablePage1-microdata.html (Furkan)
    │       │   └── tablePage1-json-ld-and-microdata.html (Furkan)
    │       └── tablePage1WithPagination/
    │           └── (same structure as above) (Furkan)
    ├── llm-preview/ (with html content) (Furkan)
    ├── api/
    │   └── people/
    │       ├── table-page-1-llm (JSON Object as a natural language) (Furkan)
    │       └── table-page-1 (vanilla JSON object) (Furkan)

### 1. Prerequisites

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
