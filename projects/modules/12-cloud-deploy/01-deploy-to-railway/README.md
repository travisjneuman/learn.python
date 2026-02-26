# Module 12 / Project 01 — Deploy to Railway

Home: [README](../../../../README.md) · Module: [Cloud Deployment](../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- Deploying a FastAPI app to Railway
- Environment variables on a cloud platform
- Procfile and runtime configuration
- Viewing logs in production

## Why this project exists

This is the moment your code goes from "runs on my laptop" to "runs on the internet." You will deploy a real FastAPI app to Railway and see it respond to requests from any browser in the world.

## Prerequisites

- A [Railway](https://railway.app) account (free tier available)
- Git installed and configured
- A GitHub account (Railway deploys from GitHub repos)

## Project files

```
01-deploy-to-railway/
├── app.py              # FastAPI app
├── requirements.txt    # Python dependencies
├── Procfile            # Tells Railway how to start the app
├── runtime.txt         # Python version
├── .env.example        # Template for environment variables
└── notes.md
```

## Step-by-step deployment

### 1. Test locally first

```bash
cd projects/modules/12-cloud-deploy/01-deploy-to-railway
pip install -r requirements.txt
python app.py
# Visit http://127.0.0.1:8000/docs
```

### 2. Push to GitHub

Create a new GitHub repo and push this project to it.

### 3. Deploy on Railway

1. Go to https://railway.app and sign in with GitHub.
2. Click "New Project" → "Deploy from GitHub repo."
3. Select your repository.
4. Railway detects the `Procfile` and starts building.
5. Once deployed, Railway gives you a public URL.

### 4. Set environment variables

In Railway dashboard → your service → Variables:
- `APP_ENV=production`
- `APP_NAME=my-fastapi-app`

### 5. Verify

Visit `https://your-app.up.railway.app/health` — you should see a JSON response.

## Expected output

After deployment, visiting your Railway URL returns:

```json
{
  "message": "Hello from the cloud!",
  "environment": "production",
  "version": "1.0.0"
}
```

## Alter it

1. Add a new endpoint and redeploy. Watch Railway's automatic deploy trigger.
2. Add a `PORT` environment variable and make the app read it (Railway sets this automatically).
3. Add basic rate limiting using an in-memory counter.

## Break it

1. Remove the `Procfile`. Can Railway still start the app?
2. Set a wrong Python version in `runtime.txt`. What happens during build?
3. Push code with a syntax error. Check the deploy logs.

## Fix it

1. Add the Procfile back and redeploy.
2. Fix the Python version to match what Railway supports.
3. Fix the syntax error, push, and verify auto-deploy succeeds.

## Explain it

1. What does the Procfile do and why is it needed?
2. Why should you read configuration from environment variables instead of hardcoding?
3. What is the difference between a build step and a run step in deployment?
4. How does Railway know when to redeploy your app?

## Mastery check

You can move on when you can:
- deploy a FastAPI app to Railway from GitHub,
- set and read environment variables,
- check deploy logs to debug issues,
- explain the deploy workflow.

---

## Related Concepts

- [Api Basics](../../../../concepts/api-basics.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [Http Explained](../../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../../concepts/quizzes/api-basics-quiz.py)

## Next

[Project 02 — Deploy with Database](../02-deploy-with-database/)
