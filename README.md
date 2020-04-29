# springer-crawler

Download all Springer books released for free during the 2020 COVID-19 quarantine

## How to run

Start docker compose:

```
docker-compose up -d
```

Then books will be downloaded into folder:

```
src/wroker/media/books
```

## Tech stack

- Scrapy
- MongoDB
- AsyncIO

## Other guides

- https://github.com/alexgand/springer_free_books