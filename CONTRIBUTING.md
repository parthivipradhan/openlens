# Contributing to LocalityLens

Thank you for your interest in contributing to LocalityLens!

## Ways to Contribute

- Frontend development (Next.js, MapLibre)
- Backend APIs (FastAPI, PostGIS)
- Geospatial analysis
- AI evaluation and open-model integration
- Blockchain verification (Solidity, Foundry)
- Dataset adapters
- Documentation
- Accessibility improvements
- Security reviews
- Testing

## Contribution Workflow

1. Open or select an issue in the GitHub issue tracker.
2. For significant changes, comment on the issue to agree on scope before starting.
3. Fork the repository and create a focused branch (e.g. `feature/evidence-explorer`).
4. Implement the change with tests.
5. Run `make test` and `make lint` to verify quality checks pass.
6. Update relevant documentation.
7. Open a pull request with a description of what was changed and how it was tested.

## Adding a New Data Source

Every new data source adapter must include a dataset manifest documenting:

- Source URL and publisher
- Licence and required attribution
- Geographic and temporal coverage
- Data transformations applied
- Known limitations
- Whether redistribution is permitted

Do not add a data source without verifying its licence allows the intended use.

## Code Style

- Python: `ruff` for linting and formatting (`make lint` / `make format`)
- TypeScript: ESLint via Next.js defaults
- All new features need tests

## Commit Messages

Use clear, descriptive commit messages. Prefix with the affected area:
- `feat: add evidence search filter`
- `fix: correct geocoding precision label`
- `docs: update data sources readme`
- `test: add missing-evidence abstention test`

## Security

See [SECURITY.md](SECURITY.md) for the security disclosure process.

Do not commit secrets, private keys, or populated `.env` files.

## Code of Conduct

Be respectful and constructive. We follow standard open-source community norms.
