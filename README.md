# Pybuster

Website directory enumeration tool writte in Python. Hobby project inspired by [Gobuster](https://github.com/OJ/gobuster).

Pybuster can be used as a Python CLI tool:

![alt text](https://github.com/Nyquist01/pybuster/blob/main/docs/images/cli.png)

Or run locally and interacted with in a browser:

![alt text](https://github.com/Nyquist01/pybuster/blob/main/docs/images/web.png)

# Usage

## CLI

Using Pybuster from the CLI requires:

- Python 3.13 or above

Enumerate a target website using:

```
bash pybuster.sh google.com
```

## Browser

Using Pybuster with a browser frontend requires Docker to be installed on your machine.

You can the run the app by running `docker compose up` and navigate to `http://localhost:8080/static` in your browser.
