# docker-git-workshop

## Useful docker commands

```sh
# Build a container image
docker build -t <container_name> <src>

# Start a container by name
docker start -d -p <host_port:container_port> <container_name>

# Stop a container by id
docker stop <container_id>

# Execute program in running container
docker exec -i -t <container_id> <program>
```

## SSH Trick

The ssh server is hosted at non-default port 2222, git does not have an option for specifying which port to connect to without writing out a full ssh path. A workaround to get our system to work more naturally is to add the following to `~/.ssh/config`:

```
Host localhost
    HostName localhost
    Port 2222
```
