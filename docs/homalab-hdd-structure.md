# HDD Structure Design: `2025-J4F-01`

## Overview
This document outlines the proposed directory structure and file organization strategy for the external 5TB HDD labeled `2025-J4F-01`. The goal is to ensure scalability, clarity, and automation-friendly data access across different devices and scripts.

## Base Directory Layout

```
2025-J4F-01/
├── MEDIA
│   ├── movies
│   └── series
├── WORKSPACE
│   └── repositories
│       ├── 0xj4f                # personal GitHub
│       └── github               # cloned or watched public repos
├── DATASOURCE
│   ├── pdfs
│   ├── youtube
│   │   └── [author]/[title]/
│   │       ├── video_name.mp4
│   │       ├── video_name_transcript.txt
│   │       └── metadata.txt
│   ├── linkedin_posts
│   ├── reddit
│   ├── blogs
│   │   ├── medium
│   │   └── custom
│   └── sqlites
```

## YouTube Directory Convention

To simplify access and ensure consistency across scraping and LLM pipelines, YouTube data is organized as follows:

```
youtube/
├── [artist_or_channel_name]/
│   └── [video_title]/
│       ├── video_name.mp4
│       ├── video_name_transcript.txt
│       └── metadata.txt
```

### Example:
```
youtube/
├── Lex Fridman/
│   └── Sam Altman Interview/
│       ├── sam_altman_interview.mp4
│       ├── sam_altman_interview_transcript.txt
│       └── metadata.txt
```

### metadata.txt Contents:
```txt
title: Sam Altman Interview
channel: Lex Fridman
published: 2023-05-18
source_url: https://youtube.com/watch?v=abc123
scraped_at: 2025-01-15T20:33:00
keywords: AI, OpenAI, Interview
```

This ensures any analysis or processing scripts can rely on structured metadata and filenames.

## Notes for Automation
- Filenames should be lowercase, underscore-separated for uniformity.
- Directory names can retain spaces or original titles for readability.
- Python scripts should walk the `youtube/` tree recursively to extract data or train LLMs.
- SQLite metadata index can reference the `[author]/[title]/` path and tie it to transcripts and metadata for fast lookups.

This layout supports traceable, queryable, and reproducible pipelines for AI workflows, scraping routines, and media management.
