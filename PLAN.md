# 🗓️ Daily Standup Summary Automation — Cloud Native AWS Plan (Python + GitLab + CloudFormation + SNS)

A serverless application that collects a software engineer's daily tasks, schedules, commits, and tickets from Notion, Google Calendar, GitLab, and Jira. It summarizes the information using OpenAI and sends a report via Amazon SNS every weekday at 9:00 AM.

---

## ✅ Phase 1: Project Setup & Scheduling

**Goal**: Set up the foundational infrastructure and scheduling.

### Tasks
- [x] Create Python project using hexagonal structure:
  - `app/domain/` (ports, model, exceptions, commands, command_handlers)
  - `app/adapters/` (external service adapters)
  - `app/entrypoints/` (lambda handler)
  - `app/libraries/` (shared utilities)
- [x] Initialize Github repo
- [x] Create CloudFormation template for:
  - [x] EventBridge scheduled rule (e.g. cron: 9:00 AM WIB)
  - [x] Lambda function and execution role
  - [x] SNS topic and policy
- [x] Deploy skeleton function with logging

### Deliverables
- [x] `infra/template.yaml`
- [x] `app/entrypoints/lambda_handler.py`
- [x] `scripts/deploy.sh`
- [x] IAM policies for SNS, EventBridge

---

## ✅ Phase 2: Adapter – Notion (Tasks)

**Goal**: Fetch today's tasks from Notion database.

### Tasks
- [ ] Define `NotionPort` in `app/domain/ports/notion_port.py`
- [ ] Create `Task` entity in `app/domain/model/task.py`
- [ ] Implement `NotionAdapter` in `app/adapters/notion/notion_adapter.py`
- [ ] Load database ID and token from env or secrets

### Deliverables
- [ ] Unit tests for Notion adapter in `app/adapters/tests/`
- [ ] Reusable task list for summarizer

---

## ✅ Phase 3: Adapter – Google Calendar (Schedules)

**Goal**: Fetch today's calendar events.

### Tasks
- [ ] Define `GoogleCalendarPort` in `app/domain/ports/google_calendar_port.py`
- [ ] Create `Schedule` entity in `app/domain/model/schedule.py`
- [ ] Implement `GoogleCalendarAdapter` in `app/adapters/google_calendar/`
- [ ] Configure service account auth (using `GOOGLE_APPLICATION_CREDENTIALS` or IAM)
- [ ] Share calendar with service account

### Deliverables
- [ ] Working adapter with UTC filtering for today
- [ ] Example printout of meetings

---

## ✅ Phase 4: Adapter – GitLab (Commits)

**Goal**: Fetch GitLab commits or MRs from yesterday until today.

### Tasks
- [ ] Define `GitLabPort` interface in `app/domain/ports/gitlab_port.py`
- [ ] Create `Commit` entity in `app/domain/model/commit.py`
- [ ] Implement `GitLabAdapter` in `app/adapters/gitlab/` with GitLab API (use personal token or project access token)
- [ ] Filter by author/email and date range

### Deliverables
- [ ] GitLab commits grouped by repo
- [ ] Unit-tested port and adapter

---

## ✅ Phase 5: Adapter – Jira (Tickets)

**Goal**: Fetch recently updated or closed Jira tickets.

### Tasks
- [ ] Define `JiraPort` interface in `app/domain/ports/jira_port.py`
- [ ] Create `Ticket` entity in `app/domain/model/ticket.py`
- [ ] Implement `JiraAdapter` in `app/adapters/jira/` using Jira REST API (JQL filtering)
- [ ] Handle auth using basic auth or OAuth

---

## ✅ Phase 6: Adapter – OpenAI (Summarization)

**Goal**: Summarize all collected data into a coherent update.

### Tasks
- [ ] Define `SummarizerPort` interface in `app/domain/ports/summarizer_port.py`
- [ ] Implement `OpenAIAdapter` in `app/adapters/openai/` using GPT-4-turbo
- [ ] Prompt engineering (system + dynamic content)
- [ ] Handle token limits, chunking, retry

---

## ✅ Phase 7: Adapter – SNS (Delivery)

**Goal**: Publish the daily summary to an SNS topic.

### Tasks
- [ ] Define `MessengerPort` interface in `app/domain/ports/messenger_port.py`
- [ ] Implement `SnsAdapter` in `app/adapters/sns/` using boto3
- [ ] Format plain-text summary output
- [ ] Configure SNS topic + subscription via CloudFormation

---

## ✅ Phase 8: Composition & Entry Point

**Goal**: Wire everything in the Lambda entrypoint.

### Tasks
- [ ] Compose adapters in `app/entrypoints/lambda_handler.py`
- [ ] Execute flow: Notion + Calendar + GitLab + Jira → Summarizer → SNS
- [ ] Log or trace each stage
- [ ] Add try/catch and fallback logic

---

## ✅ Phase 9: CI/CD with GitLab

**Goal**: Automate deployment using GitLab CI.

### Tasks
- [ ] Add `.gitlab-ci.yml` with:
  - `poetry install` or pip
  - `pytest` unit tests
  - `zip` Lambda package
  - `aws cloudformation deploy`
- [ ] Store credentials as GitLab CI/CD variables

---

## ✅ Phase 10: Monitoring & Alerting

**Goal**: Add visibility for runtime behavior.

### Tasks
- [ ] Enable structured logging
- [ ] Set up CloudWatch metrics and alarms for:
  - Lambda errors
  - SNS delivery failures
- [ ] Optional: Dead-letter queue (DLQ)

---

## ✅ Bonus (Optional Enhancements)

- [ ] Add time blocking logic for gaps in calendar
- [ ] Allow summary overrides or context hints
- [ ] Email fallback (via SES) if SNS fails
- [ ] CLI runner for local development
- [ ] Add comprehensive documentation in `docs/` directory
- [ ] Implement command handlers in `app/domain/command_handlers/` for business logic
- [ ] Add custom exceptions in `app/domain/exceptions/` for better error handling
