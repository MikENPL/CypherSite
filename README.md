# Cypher
A extensible site for ciphers.
___
## Extending
To add a new cipher to the list:
1. Add a python file to the `src/cyphersite/ciphers` directory.
2. Put `from cyphersite.common import exposed` at the top.
3. Add a new function and add a `@exposed` decorator to it.
4. Make sure every parameter has a type specified, and the function returns something.

Done!
___
## Runnning
All you need to run this is **docker** and **make** which you should already have.
Run:
- `make build` to build the container
- `make dev` to start the dev server
- `make start` to start the uvicorn server
- `make stop` to stop the containers