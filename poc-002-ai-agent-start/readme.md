# AI Agent Pipeline: YouTube Transcript Summarizer and Strategist

This project provides a local AI-powered pipeline to:

1. Scrape YouTube video transcripts.
2. Summarize the content using Meta's LLaMA 3.1 model via Ollama.
3. Generate actionable strategies based on the summary.
4. Store all outputs—transcript, summary, and strategy—in a PostgreSQL database.

## Project Structure

- `agent_runner.py`: Orchestrates the full agent pipeline.
- `scraper.py`: Extracts and cleans the transcript from a YouTube video.
- `summarizer.py`: Sends the transcript to Ollama for summarization.
- `strategist.py`: Generates strategic insights from the summary.
- `storage.py`: Inserts all results into a PostgreSQL database.
- `db_schema.sql`: Defines the database schema.
- `.env`: Environment configuration for model and database.

## Requirements

- Ubuntu 22.04 or macOS
- Python 3.10+
- PostgreSQL instance running locally or remotely
- Ollama installed and running (`ollama serve &`)
- Meta’s LLaMA 3.1 model pulled with:
