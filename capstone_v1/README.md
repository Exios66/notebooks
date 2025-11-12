# Capstone Project - Version 1

## Overview

This is the first version (v1.0) of the capstone 2026 project. It is a simple starter template for the final production ready project that will be used hypothetically for the graduation requirements.

## Project Structure

The project structure is as follows:

- `data/`: Contains the data for the project.
- `models/`: Contains the models for the project.
- `notebooks/`: Contains the notebooks for the project.
- `api_wrapper/`: Contains the chatbot API wrapper for HuggingFace and OpenAI.

## Chatbot API Wrapper

This project includes a comprehensive API wrapper for interacting with chatbot models from HuggingFace and OpenAI. The wrapper provides:

- Unified interface for multiple chatbot providers
- Support for specialized models from both platforms
- Streaming responses and conversation management
- Local and cloud-based model support

## Documentation

**Complete documentation is available in the `docs/` folder:**

- **[Startup Guide](docs/STARTUP_GUIDE.md)** - Complete step-by-step setup for new users
- **[Getting Started](docs/getting-started.md)** - Quick installation and basic usage
- **[API Reference](docs/api-reference.md)** - Comprehensive API documentation
- **[API Endpoints](docs/api-endpoints.md)** - Detailed endpoint reference
- **[Examples](docs/examples.md)** - Code examples and use cases
- **[Chatbot Interface](docs/chatbot-interface.html)** - Interactive web-based chatbot UI

### Quick Access

- **For New Users**: Start with [STARTUP_GUIDE.md](docs/STARTUP_GUIDE.md)
- **For Developers**: See [API Reference](docs/api-reference.md) and [Examples](docs/examples.md)
- **For Testing**: Use the [Interactive Chatbot Interface](docs/chatbot-interface.html)

### GitHub Pages

The documentation can be deployed as a GitHub Pages site. See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for deployment instructions.

### Local Documentation

To view the documentation locally:

```bash
cd docs
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000> in your browser.

## Package Documentation

See `api_wrapper/README.md` for package-specific documentation and usage examples.

## Examples

Example usage scripts can be found in the `examples/` folder. These scripts demonstrate:

- How to instantiate and use the API wrapper with different providers
- Streaming and non-streaming chatbot interfaces
- Integration with interactive UIs

### Interactive Visualization Example

For interactive data visualization leveraging advanced models and embeddings, see `examples/graph.py`. This script shows how to:

- Load data and perform dimensionality reduction using t-SNE
- Generate interactive 3D plots with Plotly to visualize embeddings
- Customize appearance and export results

**To run the visualization example:**

```bash
cd examples
python graph.py
```

This will open an interactive 3D t-SNE visualization of the sample dataset in your web browser.

## Contributing

We welcome contributions! If you'd like to contribute:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a Pull Request.

For details, see `CONTRIBUTING.md`.

## Support

If you encounter any issues or have questions:

- Open an issue on GitHub
- Refer to the [FAQ](docs/FAQ.md)
- Email the maintainer (see `pyproject.toml` or the repository profile)

---

© 2024 Capstone Team. All rights reserved.


