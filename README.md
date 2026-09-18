# Multi-Agent Research & Analysis System



A modular AI research system that uses specialized agents to research a question, analyze evidence, fact-check important claims, validate citations, generate a structured report, and automatically evaluate the final answer.



## Overview



Traditional LLM applications often generate answers directly from a single model call. This project explores a more structured approach: **divide the research process into specialized agents and use an orchestrated workflow to improve reliability and traceability.**



The system uses **LangGraph** to coordinate multiple specialized agents and **Gemini** for LLM-based reasoning. Web information is retrieved through **Tavily**, while a dedicated evaluation layer assesses the generated report.



The workflow can dynamically select between three research modes:



* **Quick** — lightweight research for simple factual questions

* **Standard** — research followed by analysis

* **Verified** — research, analysis, and fact-checking for questions where stronger verification is useful



Generated reports then pass through citation validation. If invalid citation references are detected, the reporter can regenerate the report using validation feedback before the final answer is evaluated.



\---



## Key Features



* 🤖 **Multi-agent research workflow**

* 🧭 **Dynamic workflow routing**

* 🔎 **Web-based research using Tavily**

* 🧠 **LLM-powered analysis**

* ✅ **Fact-checking agent**

* 🔗 **Citation validation**

* 🔄 **Citation-aware retry mechanism**

* 📝 **Citation-backed report generation**

* 📊 **Automated answer evaluation**

* 📚 **Source utilization evaluation**

* 🧪 **32 automated tests**

* 🛡️ **LLM retry and response validation utilities**

* 🧩 **Modular project architecture**



\---



## System Architecture



```mermaid

flowchart TD

&#x20;   A\[User Research Question] --> B\[Supervisor]



&#x20;   B --> C\[Researcher]



&#x20;   C -->|Quick| D\[Reporter]

&#x20;   C -->|Standard| E\[Analyst]

&#x20;   C -->|Verified| E



&#x20;   E -->|Standard| D

&#x20;   E -->|Verified| F\[Fact Checker]



&#x20;   F --> D



&#x20;   D --> G\[Citation Validator]



&#x20;   G -->|Valid citations| H\[LLM Judge]

&#x20;   G -->|Invalid citations| D



&#x20;   H --> I\[Final Evaluation]

&#x20;   I --> J\[End]

```



### Citation Validation Loop



The report is checked for citation references in the form:



```text

\[Source 1]

\[Source 2]

\[Source 3]

```



The citation validator compares the referenced source numbers against the sources retrieved during research.



If invalid references are found, feedback is passed back to the reporter so that the report can be regenerated. A retry limit prevents an infinite regeneration loop.



\---



## Agent Architecture



| Agent                  | Responsibility                                                         |

| ---------------------- | ---------------------------------------------------------------------- |

| **Supervisor**         | Selects the appropriate research workflow                              |

| **Researcher**         | Performs web research and creates structured source objects            |

| **Analyst**            | Analyzes research while cross-checking original sources                |

| **Fact Checker**       | Verifies important claims against research and sources                 |

| **Reporter**           | Produces the final structured, citation-backed report                  |

| **Citation Validator** | Validates source references and provides correction feedback           |

| **LLM Judge**          | Evaluates the final report for relevance, completeness, and factuality |



\---



## Research Workflows



### Quick



```text

User Query

&#x20;   ↓

Supervisor

&#x20;   ↓

Researcher

&#x20;   ↓

Reporter

&#x20;   ↓

Citation Validator

&#x20;   ↓

LLM Judge

```



Designed for relatively simple factual questions.



### Standard



```text

User Query

&#x20;   ↓

Supervisor

&#x20;   ↓

Researcher

&#x20;   ↓

Analyst

&#x20;   ↓

Reporter

&#x20;   ↓

Citation Validator

&#x20;   ↓

LLM Judge

```



Used for questions requiring multiple sources, comparisons, summaries, or deeper analysis.



### Verified



```text

User Query

&#x20;   ↓

Supervisor

&#x20;   ↓

Researcher

&#x20;   ↓

Analyst

&#x20;   ↓

Fact Checker

&#x20;   ↓

Reporter

&#x20;   ↓

Citation Validator

&#x20;   ↓

LLM Judge

```



Used when stronger verification of important factual claims is appropriate.



\---



## Evaluation Framework



The project includes both **deterministic evaluation metrics** and an **LLM-as-a-Judge evaluation layer**.



### LLM Judge



The final report is evaluated on three dimensions:



| Metric           | Description                                                        |

| ---------------- | ------------------------------------------------------------------ |

| **Relevance**    | How directly the report addresses the user's question              |

| **Completeness** | How completely the report covers important aspects of the question |

| **Factuality**   | How well the report is supported by the provided research evidence |



Each dimension is scored from:



```text

0.0 → Very poor

0.5 → Partially satisfactory

1.0 → Excellent

```



The LLM judge returns structured output validated using Pydantic.



### Overall Score



The current overall score gives equal weight to the three LLM-judge dimensions:



```text

Overall Score =

(Relevance + Completeness + Factuality) / 3

```



### Citation Accuracy



Citation accuracy measures the proportion of cited source references that are valid.



```text

Citation Accuracy =

Valid Citations / Total Cited Sources

```



### Source Utilization



Source utilization measures how many retrieved sources were actually referenced by the final report.



```text

Source Utilization =

Unique Cited Sources / Total Retrieved Sources

```



### Answer Coverage



The project also contains a deterministic answer-coverage metric that checks how many required topics appear in the generated report.



This metric is currently implemented as a simple topic-presence check and is **not a semantic quality judgment**.



\---



## Reliability Features



### LLM Retry Handling



LLM calls are wrapped with retry utilities to handle failures during model invocation.



The system also validates and extracts text from LLM responses before passing results to downstream agents.



### Citation Retry



The citation validator can trigger report regeneration when invalid source references are detected.



A retry limit is used to prevent an infinite report-generation loop.



\---



## Tech Stack



| Technology        | Purpose                           |

| ----------------- | --------------------------------- |

| **Python**        | Core implementation               |

| **LangGraph**     | Agent workflow orchestration      |

| **LangChain**     | LLM application framework         |

| **Google Gemini** | LLM reasoning and generation      |

| **Tavily**        | Web search and research retrieval |

| **Pydantic**      | Structured data validation        |

| **Pytest**        | Automated testing                 |

| **python-dotenv** | Environment configuration         |



\---



## Project Structure



```text

multi-agent-research-analysis-system/

│

├── app/

│   ├── agents/

│   │   ├── supervisor.py

│   │   ├── researcher.py

│   │   ├── analyst.py

│   │   ├── fact\_checker.py

│   │   ├── citation\_validator.py

│   │   └── reporter.py

│   │

│   ├── config/

│   │   ├── llm.py

│   │   └── settings.py

│   │

│   ├── evaluation/

│   │   ├── answer\_eval.py

│   │   ├── citation\_eval.py

│   │   ├── source\_eval.py

│   │   ├── llm\_judge.py

│   │   └── aggregate\_eval.py

│   │

│   ├── graph/

│   │   └── workflow.py

│   │

│   ├── models/

│   │   ├── schemas.py

│   │   └── state.py

│   │

│   ├── prompts/

│   │   ├── supervisor.txt

│   │   ├── researcher.txt

│   │   ├── analyst.txt

│   │   ├── fact\_checker.txt

│   │   └── reporter.txt

│   │

│   ├── tools/

│   │   ├── web\_search.py

│   │   └── calculator.py

│   │

│   ├── utils/

│   │   ├── llm\_response.py

│   │   └── llm\_retry.py

│   │

│   └── main.py

│

├── tests/

│   ├── test\_agents.py

│   ├── test\_workflow.py

│   ├── test\_tools.py

│   ├── test\_evaluation.py

│   ├── test\_answer\_evaluation.py

│   ├── test\_source\_evaluation.py

│   ├── test\_aggregate\_eval.py

│   └── test\_llm\_judge.py

│

├── notebooks/

│

├── .env.example

├── .gitignore

├── Dockerfile

├── requirements.txt

└── gemini\_check.py

```



\---



## Installation



### 1. Clone the repository



```bash

git clone https://github.com/PrathmSingh/multi-agent-research-analysis-system.git

cd multi-agent-research-analysis-system

```



### 2. Create a virtual environment



#### Windows



```powershell

python -m venv .venv

.venv\\Scripts\\Activate.ps1

```



#### Linux / macOS



```bash

python3 -m venv .venv

source .venv/bin/activate

```



### 3. Install dependencies



```bash

pip install -r requirements.txt

```



### 4. Configure environment variables



Create a `.env` file in the project root:



```text

GEMINI\_API\_KEY=your\_gemini\_api\_key

TAVILY\_API\_KEY=your\_tavily\_api\_key

```



Never commit your `.env` file or API keys to GitHub.



\---



## Usage



Run the application with:



```bash

python -m app.main

```



The system will ask:



```text

Enter your research question:

```



Enter a research question and the multi-agent workflow will execute.



The CLI displays:



1\. Final research report

2\. Relevance score

3\. Completeness score

4\. Factuality score

5\. Overall score

6\. Citation accuracy

7\. Source utilization



\---



## Running Tests



Run the complete test suite:



```bash

pytest -q

```



Current baseline:



```text

32 passed in 9.04s

```



The test suite covers agents, workflow behavior, tools, and evaluation components.



\---



## Current Status



### Implemented



* \[x] Multi-agent architecture

* \[x] Supervisor routing

* \[x] Quick workflow

* \[x] Standard workflow

* \[x] Verified workflow

* \[x] Web research

* \[x] Analysis

* \[x] Fact checking

* \[x] Citation validation

* \[x] Citation retry mechanism

* \[x] LLM-as-a-Judge evaluation

* \[x] Citation accuracy evaluation

* \[x] Source utilization evaluation

* \[x] Automated tests



### Planned



* \[ ] OpenAI model provider

* \[ ] Provider-independent LLM configuration

* \[ ] FastAPI interface

* \[ ] Dockerized application

* \[ ] Web-based user interface

* \[ ] Research report export

* \[ ] Evaluation benchmark dataset

* \[ ] Automated CI pipeline

* \[ ] Screenshots and demo

* \[ ] Improved semantic evaluation metrics



\---



## Design Goals



The project is designed around several principles:



### Modularity



Each major research responsibility is implemented as an independent agent or module.



### Evidence Grounding



Agents are instructed to base research, analysis, and reporting on retrieved evidence rather than introducing unsupported information.



### Verification



The verified workflow introduces an explicit fact-checking stage.



### Citation Reliability



Generated citations are validated before the final report is evaluated, with feedback-driven regeneration when necessary.



### Measurable Evaluation



The system evaluates generated reports instead of treating successful generation as the only measure of quality.



\---



## Limitations



The current system has several limitations:



* Search quality depends on the retrieved web sources.

* The current citation validator validates source-reference numbers rather than independently verifying the truth of cited claims.

* Source utilization does not measure source quality.

* Answer coverage uses simple topic matching rather than semantic similarity.

* LLM-as-a-Judge scores can vary between evaluations.

* The current CLI is the primary interface.

* OpenAI support is planned but not yet integrated into the application.



\---



## Roadmap



Future development will focus on:



1\. Multi-provider LLM support

2\. FastAPI-based API interface

3\. Docker deployment

4\. Automated CI testing

5\. Benchmark-based evaluation

6\. Improved semantic evaluation

7\. Better source-quality assessment

8\. Research report export

9\. Web UI

10\. Observability and tracing



\---



## Contributors



\- **Pratham Singh** — Team Lead, System Architecture, Agent Workflow, Evaluation Framework

\- **Shivansh Shukla** — Software Development, Testing, Documentation & Collaboration

\---



## License



This project is currently being prepared for public portfolio use. A license will be added before the repository is considered finalized.

