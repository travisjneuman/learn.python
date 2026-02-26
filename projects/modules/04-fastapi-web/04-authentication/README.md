# Module 04 / Project 04 — Authentication

Home: [README](../../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

JWT tokens, protected routes, password hashing, user registration and login.

## Why this project exists

Most real APIs need authentication. Users register, log in, and receive a token that proves their identity. This project adds user accounts to the todo API. You will learn how passwords are hashed (never stored in plain text), how JWT tokens work, and how to protect endpoints so only authenticated users can access their own data.

## Run

```bash
cd projects/modules/04-fastapi-web/04-authentication
python app.py
```

Then open **http://127.0.0.1:8000/docs** and follow this workflow:

1. Register a user with `POST /register`
2. Log in with `POST /login` to get a JWT token
3. Click the "Authorize" button in the `/docs` UI and paste the token
4. Now you can use the protected todo endpoints

Press `Ctrl+C` to stop the server.

## Expected output

```bash
# Register
curl -X POST http://127.0.0.1:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret123"}'
# Returns: {"id": 1, "username": "alice"}

# Login
curl -X POST http://127.0.0.1:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret123"}'
# Returns: {"access_token": "eyJhbG...", "token_type": "bearer"}

# Create a todo (with token)
curl -X POST http://127.0.0.1:8000/todos \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbG..." \
  -d '{"title": "Learn JWT"}'
# Returns: {"id": 1, "title": "Learn JWT", "completed": false, ...}

# Without token
curl http://127.0.0.1:8000/todos
# Returns: 401 Unauthorized
```

## Alter it

1. Add token expiration. Make tokens expire after 30 minutes. After expiration, the user must log in again.
2. Add a `GET /me` endpoint that returns the currently logged-in user's info.
3. Add a `PUT /me/password` endpoint that lets users change their password (requires old password and new password).

## Break it

1. Copy a valid JWT token and change one character in the middle. Try to use it. What error do you get?
2. Register a user, then try to register the same username again. What happens?
3. Try to log in with a correct username but wrong password. What response do you get?

## Fix it

1. The tampered token is rejected because JWTs are cryptographically signed. Any change invalidates the signature. This is working correctly.
2. If duplicate registration succeeds, add a check in the register endpoint that queries for existing usernames and raises a 400 error.
3. The wrong password should return a 401 Unauthorized. If it does not, check that the password verification function compares the hashed values correctly.

## Explain it

1. Why do we hash passwords instead of storing them directly? What would happen if the database were stolen?
2. What information is stored inside a JWT token? Can the server read it without the secret key? Can a client read it?
3. What does the `Authorization: Bearer <token>` header mean? Why "Bearer"?
4. What is the difference between authentication (who are you?) and authorization (what can you do?)?

## Mastery check

You can move on when you can:

- register a user and log in without looking at these instructions,
- explain why passwords are hashed and what a salt does,
- describe the three parts of a JWT token (header, payload, signature),
- add a new protected endpoint from memory.

---

## Related Concepts

- [Api Basics](../../../../concepts/api-basics.md)
- [Files and Paths](../../../../concepts/files-and-paths.md)
- [Http Explained](../../../../concepts/http-explained.md)
- [Types and Conversions](../../../../concepts/types-and-conversions.md)
- [Quiz: Api Basics](../../../../concepts/quizzes/api-basics-quiz.py)

## Next

Continue to [05-full-app](../05-full-app/).
