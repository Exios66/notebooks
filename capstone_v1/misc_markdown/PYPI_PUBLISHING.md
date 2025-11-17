# PyPI Publishing Guide

This guide explains how to publish the `chatbot-api-wrapper` package to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts on:
   - [Test PyPI](https://test.pypi.org/) (for testing)
   - [PyPI](https://pypi.org/) (for production)

2. **Install Build Tools**:

   ```bash
   pip install --upgrade build twine
   ```

3. **Configure Credentials**:
   Create `~/.pypirc`:

   ```ini
   [distutils]
   index-servers =
       pypi
       testpypi

   [pypi]
   username = __token__
   password = pypi-<your-token-here>

   [testpypi]
   username = __token__
   password = pypi-<your-test-token-here>
   ```

   Or use environment variables:

   ```bash
   export TWINE_USERNAME=__token__
   export TWINE_PASSWORD=pypi-<your-token-here>
   ```

## Building the Package

1. **Clean Previous Builds**:

   ```bash
   rm -rf dist/ build/ *.egg-info
   ```

2. **Build Distribution Packages**:

   ```bash
   python -m build
   ```

   This creates:
   - `dist/chatbot-api-wrapper-1.0.0.tar.gz` (source distribution)
   - `dist/chatbot_api_wrapper-1.0.0-py3-none-any.whl` (wheel)

3. **Verify Build**:

   ```bash
   # Check package contents
   tar -tzf dist/chatbot-api-wrapper-*.tar.gz

   # Verify metadata
   twine check dist/*
   ```

## Testing on Test PyPI

1. **Upload to Test PyPI**:

   ```bash
   twine upload --repository testpypi dist/*
   ```

2. **Test Installation**:

   ```bash
   pip install --index-url https://test.pypi.org/simple/ chatbot-api-wrapper
   ```

3. **Verify Installation**:

   ```python
   from api_wrapper import ChatbotWrapper
   print(ChatbotWrapper.__module__)
   ```

## Publishing to PyPI

1. **Final Check**:
   - [ ] Version number updated in `pyproject.toml`
   - [ ] CHANGELOG.md updated
   - [ ] All tests passing
   - [ ] Documentation updated
   - [ ] Build succeeds without errors

2. **Upload to PyPI**:

   ```bash
   twine upload dist/*
   ```

3. **Verify Publication**:
   - Check package page: `https://pypi.org/project/chatbot-api-wrapper/`
   - Test installation: `pip install chatbot-api-wrapper`

## Version Management

### Semantic Versioning

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Updating Version

1. Update version in `pyproject.toml`:

   ```toml
   version = "1.0.1"
   ```

2. Update version in `api_wrapper/__init__.py`:

   ```python
   __version__ = "1.0.1"
   ```

3. Update CHANGELOG.md with changes

4. Commit and tag:

   ```bash
   git add pyproject.toml api_wrapper/__init__.py CHANGELOG.md
   git commit -m "Bump version to 1.0.1"
   git tag v1.0.1
   git push origin main --tags
   ```

## Automated Publishing with GitHub Actions

The included `.github/workflows/publish.yml` workflow can automatically publish to PyPI when you:

1. Create a release on GitHub
2. Push a tag starting with `v` (e.g., `v1.0.0`)

### Setup

1. Add PyPI token to GitHub Secrets:
   - Go to Repository → Settings → Secrets → Actions
   - Add `PYPI_API_TOKEN` with your PyPI API token

2. Create a release:

   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

   Then create a release on GitHub with the same tag.

## Troubleshooting

### Common Issues

1. **"Package already exists"**:
   - Version already published
   - Solution: Increment version number

2. **"Invalid distribution"**:
   - Build artifacts corrupted
   - Solution: Clean and rebuild

3. **"Authentication failed"**:
   - Invalid token or credentials
   - Solution: Regenerate PyPI token

4. **"Missing required files"**:
   - README.md or LICENSE not found
   - Solution: Ensure files exist in project root

### Best Practices

1. **Always test on Test PyPI first**
2. **Use API tokens instead of passwords**
3. **Keep tokens secure** (never commit to git)
4. **Update CHANGELOG.md** with each release
5. **Tag releases** in git
6. **Test installation** after publishing

## Post-Publication

1. **Monitor Package**:
   - Check download statistics on PyPI
   - Monitor GitHub issues for user feedback

2. **Update Documentation**:
   - Update installation instructions
   - Add PyPI badge to README

3. **Announce Release**:
   - Update release notes on GitHub
   - Notify users if breaking changes

## Security Considerations

- **Never commit API tokens** to version control
- **Use environment variables** or secure credential storage
- **Rotate tokens** regularly
- **Use 2FA** on PyPI account
- **Review package contents** before publishing

## Additional Resources

- [PyPI Documentation](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/guides/distributing-packages-using-setuptools/)
