# Publishing the workshop presentations

- `origin`: personal GitHub repository, `kcaisley/hotpot`.
- `gitlab`: university repository, `hotpot-workshop/hotpot-chip-design-workshop`.
- `dev`: full development sources; push only to GitHub.
- `main`: attendee repository, preserving existing GitLab content and adding `slides/`.
- `main` is published to both GitLab and GitHub with identical commits.
- Local development checkout: `~/Documents/hotpot`, on `dev`.
- Local attendee checkout: `~/Documents/hotpot-public`, on `main`.

## Update the attendee decks

Build the development PDFs, then export from the development checkout:

```sh
make -C docs/slides
python3 docs/slides/export_attendee_slides.py ../hotpot-public
make -B -C ../hotpot-public/slides
```

The export copies the four TeX/PDF pairs, shared TeX, only referenced images,
a small Makefile. It embeds displayed code
snippets into the TeX, keeping the attendee bundle independent of generators,
external PDKs, OpenROAD, KLayout and ngspice.

Before exporting, fetch GitLab and fast-forward the attendee checkout to any
new workshop changes. Review the exported files, then commit and push `main`
to `gitlab` and `origin`. Commit development edits separately on `dev` and
push that branch to `origin`. Do not merge `dev` into attendee `main`.

Ordinary future updates should be fast-forward pushes. The initial migration
preserves the original GitHub main history in `dev` and makes `main` share the
GitLab history; it is not a procedure to repeat for later releases.
