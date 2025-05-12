# Contributing to AIS Global Fishing Wrapper Library

As an open source project, AIS Global Fishing Wrapper Library welcomes contributions of many forms.

## Examples of contributions include:

- Code patches
- Documentation improvements
- Bug reports and patch reviews
- Feature suggestions
- Answering questions on issues

## How to Contribute

### Reporting Bugs

- Check if the bug has already been reported in the [Issues](https://github.com/dkdndes/ais-stream-lib/issues)
- If not, create a new issue with a clear title and description
- Include as much relevant information as possible
- Include code samples, error messages, and steps to reproduce

### Suggesting Features

- Check if the feature has already been suggested in the [Issues](https://github.com/dkdndes/ais-stream-lib/issues)
- Provide a clear and detailed explanation of the feature
- Explain why this feature would be useful to most users

### Code Contributions

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Write tests for your changes
4. Ensure all tests pass
5. Submit a pull request

**Important: Non-trivial pull requests (anything more than fixing a typo) should be linked to an existing issue!** Please [file an issue](https://github.com/dkdndes/ais-stream-lib/issues/new) first to discuss changes.

## Development Setup

```bash
# Clone your fork
git clone git@github.com:YOUR_USERNAME/ais-stream-lib.git

# Add the main repository as a remote
git remote add upstream git@github.com:dkdndes/ais-stream-lib.git

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
pip install -r requirements-dev.txt  # if available
```

## Pull Request Guidelines

- Update documentation if introducing new features
- Add tests for new features or bug fixes
- Follow the existing code style
- Keep pull requests focused on a single topic
- Write clear, descriptive commit messages

## License Considerations

By contributing to this project, you agree that your contributions will be licensed under the project's [Business Source License 1.1](LICENSE).

## Code of Conduct

As a contributor, you agree to abide by the project's code of conduct. Please be respectful and considerate of others when contributing to the project.

## Questions?

If you have any questions about contributing, please open an issue or contact the project maintainer directly.

# Contributing to AIS Global Fishing Wrapper Library

Thank you for your interest in contributing to the AIS Global Fishing Wrapper project! This document provides guidelines and instructions for contributing.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/dkdndes/ais-global-fishing.git
   cd ais-global-fishing
   ```

2. Set up the development environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync
   ```

3. Install development dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```

## Code Style

This project follows PEP 8 style guidelines. Please ensure your code adheres to these standards.

## Testing

Before submitting a pull request, please run the tests to ensure your changes don't break existing functionality:

```bash
pytest
```

## Submitting Changes

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes
4. Run tests to ensure they pass
5. Submit a pull request

## Pull Request Process

1. Update the README.md or documentation with details of changes if appropriate
2. Update the examples if needed
3. The PR should work on the main branch

## Contact

If you have any questions, feel free to contact Peter Rosemann at dkdndes@gmail.com.
