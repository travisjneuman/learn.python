# Module 09 / Project 02 — Multi-Stage Build

Home: [README](../../../../README.md)

## Focus

Multi-stage Docker builds to reduce image size, and `.dockerignore` to exclude unnecessary files.

## Why this project exists

A single-stage Dockerfile works, but the resulting image is larger than necessary because it includes build tools (pip, setuptools, wheel) that are only needed during installation. Multi-stage builds split the process into a "builder" stage that installs dependencies and a "production" stage that copies only the final artifacts. The result is a smaller, more secure image with a reduced attack surface.

## Run

### Build both images for comparison

```bash
cd projects/modules/09-docker-deployment/02-multi-stage-build

# Build the single-stage image
docker build -f Dockerfile.simple -t single-stage-app .

# Build the multi-stage image
docker build -t multi-stage-app .
```

### Compare image sizes

```bash
docker images | grep -E "single-stage|multi-stage"
```

You should see the multi-stage image is noticeably smaller. The exact difference depends on your system, but expect 20-50 MB savings.

### Run the multi-stage image

```bash
docker run -p 8000:8000 multi-stage-app
```

Visit http://127.0.0.1:8000 to verify it works.

## Expected output

Both images produce the same API response:

```json
{"message": "Hello from a multi-stage build!", "version": "1.0.0"}
```

The `docker images` comparison shows something like:

```
REPOSITORY         TAG       SIZE
single-stage-app   latest    195MB
multi-stage-app    latest    155MB
```

(Your sizes will vary. The point is the multi-stage image is smaller.)

## Alter it

1. Add a third stage to the Dockerfile that runs tests before building the production image. (Hint: add a "test" stage between builder and production that runs `python -c "import fastapi; print('OK')"`)
2. Remove `.git/` from `.dockerignore` temporarily. Rebuild both images and compare sizes. Add it back.
3. Add a `LABEL` instruction to the production stage with your name and the build date.

## Break it

1. In the multi-stage Dockerfile, change `COPY --from=builder /build/.venv /app/.venv` to `COPY --from=builder /build/.venv /wrong/path`. Rebuild and run. What error do you get?
2. Remove the `ENV PATH` line in the production stage. Rebuild and run. What happens when uvicorn tries to start?
3. Delete the `.dockerignore` file and rebuild. Is the image larger? Check with `docker images`.

## Fix it

1. Restore the correct path `/app/.venv`. The virtual environment must be where the PATH expects it.
2. Restore the `ENV PATH` line. Without it, the shell cannot find `uvicorn` or any installed packages.
3. Restore the `.dockerignore` file. Without it, Docker copies everything (including `.git/`, `__pycache__/`, and local `.venv/`) into the build context.

## Explain it

1. What is a "stage" in a multi-stage build? How many stages does our Dockerfile have?
2. Why do we create a virtual environment in the builder stage instead of installing packages globally?
3. What does `COPY --from=builder` do? How is it different from a regular `COPY`?
4. What is the purpose of `.dockerignore`? How is it similar to `.gitignore`?

## Mastery check

You can move on when you can:

- explain why multi-stage builds produce smaller images,
- write a multi-stage Dockerfile from scratch,
- create a `.dockerignore` file with appropriate exclusions,
- describe what `COPY --from=<stage>` does.

---

## Related Concepts

- [Files and Paths](../../../../concepts/files-and-paths.md)
- [The Terminal Deeper](../../../../concepts/the-terminal-deeper.md)
- [Virtual Environments](../../../../concepts/virtual-environments.md)
- [Quiz: Files and Paths](../../../../concepts/quizzes/files-and-paths-quiz.py)

## Next

Continue to [03-docker-compose](../03-docker-compose/).
