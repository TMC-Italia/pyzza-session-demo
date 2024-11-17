# pyzza-session-demo

Pizza session 18 Nov - Python demo

## Abstract


## Installation

### Python environment setup:

```bash
python3 -m venv .venv
. .venv/bin/activate
```

To check that virtual environment is activated:

```bash
which python
```

Copy and set your own environment variables:

```bash
cp .env.sample .env
```

Change the values in the `.env` file.

### Install the dependencies:

```bash
make install

```

## Usage

Build the container:

```bash
make compose-build
```

Run the container:

```bash
make compose-up
```
