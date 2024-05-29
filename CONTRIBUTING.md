# Contributing

Contributions are encouraged, and they are greatly appreciated! Every little bit helps, and credit will always be given.

## Get Started

Ready to contribute? Here's how to set up `sick-tag-loc-connector` for local development.

1. Fork the `sick-tag-loc-connector` repo on [GitHub](https://github.com/inorbit-ai/sick-tag-loc-connector).

2. Clone your fork locally:

    ```bash
    git clone git@github.com:{your_username_here}/sick-tag-loc-connector.git
    ```

3. Install the project in editable mode. (It is also recommended to work in a `virtualenv` environment):

    ```bash
    cd sick-tag-loc-connector
    virtualenv .venv
    source .venv/bin/activate
    pip install -r requirements.txt -r requirements-dev.txt
    ```

4. Create a branch for local development:

    ```bash
    git checkout -b {your_development_type}/short-description
    ```

   Ex: feature/read-tiff-files or bugfix/handle-file-not-found<br>
   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass linting and tests, including testing other Python
   versions with tox:

    ```bash
    tox
    ```

6. Commit your changes and push your branch to GitHub:

    ```bash
    git add .
    git commit -m "Resolves #xyz. Your detailed description of your changes."
    git push origin {your_development_type}/short-description
    ```

7. Submit a pull request through the [GitHub](https://github.com/inorbit-ai/sick-tag-loc-connector/pulls) website.
