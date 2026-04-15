---
name: public-apis
description: Search and explore 1400+ free public APIs from the public-apis repository. Use this skill when you need to find free APIs for research, data retrieval, or integration. Load this skill to search by category, keyword, auth type, or features. Run the search script to find relevant APIs.
keywords: [public-apis, free APIs, API discovery, research, data, integration, open source APIs]
version: 1.0.0
author: Awesome Hermes
license: MIT
---

# Public APIs Skill

Search and explore 1400+ free public APIs from the [public-apis repository](https://github.com/public-apis/public-apis).

## Quick Search

Use the `search_apis.py` script to find APIs:

```bash
# Search by keyword
python3 ~/.hermes/tools/public-apis/search_apis.py --query "weather"

# Filter by category
python3 ~/.hermes/tools/public-apis/search_apis.py --category "Finance"

# Filter by auth type
python3 ~/.hermes/tools/public-apis/search_apis.py --auth "apiKey"

# Filter by HTTPS support
python3 ~/.hermes/tools/public-apis/search_apis.py --https

# Combine filters
python3 ~/.hermes/tools/public-apis/search_apis.py --query "news" --category "News" --https
```

## All Categories

The repository covers these categories:
- Animals, Anime, Anti-Malware, Art & Design
- Authentication & Authorization, Blockchain, Books, Business
- Calendar, Cloud Storage & File Sharing, Continuous Integration
- Cryptocurrency, Currency Exchange, Data Validation
- Development, Dictionaries, Documents & Productivity
- Email, Entertainment, Environment
- Finance, Food & Drink, Games & Comics
- Geocoding, Government, Health, History
- Jobs, Machine Learning, Music, News
- Open Data, Personality, Photography, Programming
- Science & Math, Security, Shopping, Sports
- Stock Market, Transportation, Travel, URL Shorteners
- Utilities, Vehicle, Video, Weather

## API Properties

Each API entry includes:
- **Name** - API name
- **URL** - Documentation/website URL
- **Description** - What the API does
- **Category** - Category it belongs to
- **Auth** - Authentication type (apiKey, OAuth, No, etc.)
- **HTTPS** - Whether HTTPS is supported (Yes/No)
- **CORS** - CORS support (Yes/No/Unknown)

## Research Use Cases

This skill is especially useful for research when you need:
1. Free data sources (financial, scientific, government data)
2. News/article APIs for content monitoring
3. Academic/research APIs (arXiv, PubMed, etc.)
4. Real-time data (weather, stocks, crypto)
5. Government/open data portals

## Manual Exploration

You can also browse the raw data:
- JSON index: `~/.hermes/tools/public-apis/apis.json`
- Source README: `~/.hermes/tools/public-apis/README.md`
