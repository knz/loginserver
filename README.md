# Example "serverless" login flow

## For end-users

- Just once:
  - download `cloud.py`
  - run `cloud.py login`
    This will open a web browser and initiate the login flow.

- In client apps: see `example.py` for example use.
  Just the library file `cloud.py` is sufficient to build apps.
  No configuration needed.


## Setup for administrators

- in the cloud, run the `server.py`

- modify `cloud.py` to set `login_service` to the centralized login
  server URL. Distribute `cloud.py` to client apps.
