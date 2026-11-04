# Media Export Converter

Convert a saved Stremio library HTML page into a Trakt-oriented JSON export. The parser reads movie IDs, episode numbers, watched markers, and progress. It runs locally using Python's standard library.

```sh
python stremio_to_trakt.py examples/library.html --no-watchlist -o examples/output.json
python -m unittest discover -s tests -v
```

The example uses fictional titles and identifiers. The two records include a movie and an episode. Invalid media links are skipped. Empty input or a page with no recognized entries exits with an error.

Omit `--no-watchlist` to add a current UTC watchlist timestamp. Use `--watched-only` or `--min-progress 50` to filter records. The script writes a file for review and import. It makes no account requests. Saved page structure and a destination importer's requirements can change, so review the JSON before importing your own data.

This release packages an existing personal conversion script, fixes recognition of camel-case progress classes, and includes CLI regression checks.
