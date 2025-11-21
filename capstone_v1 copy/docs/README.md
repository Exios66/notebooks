# Documentation Site

This directory contains the GitHub Pages documentation site for the Chatbot API Wrapper.

## Local Development

To run the documentation site locally:

1. Install Jekyll and dependencies:

```bash
cd docs
bundle install
```

2. Run the Jekyll server:

```bash
cd docs
bundle exec jekyll serve --livereload
```

3. Open  <http://localhost:4000> in your browser

## Structure

- `_config.yml` - Jekyll configuration
- `_layouts/` - HTML layouts
- `index.md` - Home page
- `getting-started.md` - Setup guide
- `api-reference.md` - API documentation
- `examples.md` - Code examples
- `chatbot-interface.html` - Interactive chatbot UI

## Deployment

This site can be deployed to GitHub Pages automatically when pushed to the repository.
