# pit38-ibkr

Template Python project using Python 3.13, `uv`, and Docker Compose.
To read more about the tax calculations and implementation details, see [Objective file](OBJECTIVE.md).

## Requirements

- Docker
- Docker Compose (v2)

## Quick start

```bash
make build
make run
```

You should see output from `src/main.py`.

## Make commands

- `make build` - Build the Docker image
- `make up` - Start the app service
- `make run` - Run the app once
- `make shell` - Open a shell in the app container
- `make logs` - Follow container logs
- `make down` - Stop and remove containers
- `make clean` - Stop containers and remove built images

## Dependency management with uv

Dependencies are defined in `pyproject.toml` and managed with `uv`.

- Add a dependency locally:

  ```bash
  uv add <package>
  ```

- Rebuild the image after dependency changes:

  ```bash
  make build
  ```

Inside Docker, the project uses `uv run ...` to execute Python in the managed environment.
