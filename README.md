# API Test Suite for JSONPlaceholder

This is an automated test suite I built for the [JSONPlaceholder](https://jsonplaceholder.typicode.com) public REST API, written in Python using `requests` and `pytest`. The goal was to verify that the API behaves the way its specification says it should, which means correct status codes, correctly structured responses, and sensible behavior when things go wrong, such as requesting a resource that does not exist.

## Why JSONPlaceholder?

I looked at a few public APIs before settling on this one. JSONPlaceholder won out for three practical reasons: it needs no API key or authentication, so anyone cloning this repo can run the tests immediately; it has no meaningful rate limits; and it supports all the major HTTP methods (GET, POST, PUT, and DELETE) across several resource types. That made it possible to cover real create, update, and delete flows instead of just reads.

One quirk worth knowing is that JSONPlaceholder **simulates** write operations. When you POST a new resource, it responds exactly like a real API would, returning `201 Created` with your payload echoed back and a freshly assigned `id`, but nothing is actually saved on the server. Because of that, my write tests assert against the response itself (status code, echoed fields, and the new id) rather than trying to fetch the created resource afterward, which would fail by design. This is documented in the test docstrings as well.

## What's tested

The suite contains **15 test cases** across three endpoints, and every test checks more than just whether the request returned 200. Each one validates the status code, the shape of the response, and the actual content.

**`/posts`** gets the fullest coverage since it supports every method:
- GET all posts confirms a 200, that the response is a list, and that it contains the expected 100 records
- GET a single post applies a strict schema check (the response must have exactly the keys `userId`, `id`, `title`, and `body`) and confirms the right record came back
- GET a post that does not exist confirms the API correctly returns 404 instead of an error page or an empty 200
- POST a new post confirms 201, that the API echoes back every field I sent, and that it assigned id 101 (the dataset has 100 posts, so a correctly simulated create should always produce 101)
- PUT an update confirms 200 and that the updated fields actually appear in the response
- DELETE confirms the API accepts the deletion with a 200

**`/users`** is where I test nested data structures. User objects contain an embedded `address` object, which itself contains a `geo` object. The tests verify that nesting exists and then go one step further: the geo coordinates come back as strings, so the test passes them through `float()`, meaning that if the API ever returned a malformed coordinate the test would fail. There is also a 404 check for a nonexistent user.

**`/comments`** is where I test query parameter filtering. Requesting `/comments?postId=1` should return only comments belonging to post 1, so the test asserts that every comment in the response has `postId == 1` rather than just checking that something came back. A second test confirms that filtering by a postId that does not exist returns an empty list with a 200, which is the correct "no results" behavior (as opposed to a 404, which would mean the route itself was not found).

## How the project is organized

```
api-test-suite/
├── tests/
│   ├── test_posts.py       # GET, POST, PUT, DELETE
│   ├── test_users.py       # nested schema validation
│   └── test_comments.py    # query param filtering
├── conftest.py             # shared pytest fixtures
├── pytest.ini              # pytest configuration
├── requirements.txt
└── .github/workflows/tests.yml   # CI pipeline
```

The file `conftest.py` holds shared fixtures, namely the API base URL and a sample payload for the create tests. Pytest injects these into any test that asks for them, which means the base URL lives in exactly one place. If I ever pointed this suite at a different environment, such as a staging server, it would be a one line change.

## Setup

You will need Python 3.10 or newer.

```
git clone https://github.com/PuchalapalliSathvic/api-test-suite.git
cd api-test-suite
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate with `venv\Scripts\activate` instead.

## Running the tests

```
pytest
```

That is all it takes, since `pytest.ini` already configures verbose output. You will see each test listed with PASSED or FAILED in the terminal along with a summary at the end. It also generates `report.html`, a self contained HTML report you can open in any browser, with per test durations and filterable results.

A couple of variations I find useful:

```
pytest tests/test_posts.py
pytest -k "404"
```

The first runs a single file and the second runs only the error handling tests.

## Continuous integration

The repo includes a GitHub Actions workflow that runs the full suite on every push and pull request to `main`. It also uploads the HTML report as a build artifact, and it does so even when tests fail, since a failing run is exactly when you would want to inspect the report. The green check on the repo means the suite passes in a clean environment and not just on my machine.
