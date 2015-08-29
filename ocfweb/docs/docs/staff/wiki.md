[[!meta title="Wiki editing"]]
# Using ikiwiki

[ikiwiki](https://ikiwiki.info/) uses [Markdown][markdown].

## Technical details

Data is stored in `/srv/ikiwiki` on blight, which contains:

 * `public_html/`: output (HTML)
 * `wiki/`: input (Markdown)
 * `wiki.git/`: bare repository (git)
 * `wiki.setup`: ikiwiki configuration file

The wiki's authoritative git repo is [GitHub][github]. Commit your changes and
push them to GitHub, and they will be deployed automatically.

## Editing the wiki

### Using git directly

1. Clone [the repository on GitHub][github].

2. Make changes.

3. Push your changes.

## Troubleshooting

If your edits aren't appearing, try rebuilding the entire wiki from the git
repository.

    $ sudo -u www-data /srv/ikiwiki/rebuild-wiki

[github]: https://github.com/ocf/wiki
[markdown]: https://daringfireball.net/projects/markdown/syntax
