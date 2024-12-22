# Dasein-as-a-Degenerate

## Notes
Using RabbitMQ for the hell of it.

## Requirements

- Make sure you have [uv](https://docs.astral.sh/uv/) installed.
- Make sure you have Docker (needed for RabbitMQ) installed and running.

### Keys

- You'll need to transform your Kalshi private key into a base64 string before adding it to the `.env` file; you can do this by running `base64 < your-private-key-file.key > file-string.b64`
- TODO; cache instructions

## Installation

- Run `uv sync` to setup the environment.
- Run `uv run dev` to run the project (see pyproject.toml for available script commands).

## Usage


## Deployment

- Push to the `main` branch and railway will automatically deploy the latest changes.
- You can also run `railway up` to deploy manually.

## TODOS

- fix the src import issue (pyproject.toml based)
- toml setup for dev dependencies
- fix my vim setup
- dockerize rabbitmq approach