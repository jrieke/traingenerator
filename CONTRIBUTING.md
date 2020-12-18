# Want to contribute?

That's very welcome! :heart:


## Before you start

It's best if you get in touch with me so we can quickly check that your plan makes 
sense and nobody else is working on this. The best way is to open an issue on this repo 
but you can also contact me on [Twitter](https://twitter.com/jrieke) or 
[e-mail](mailto:johannes.rieke@gmail.com).

As soon as you start working, you are very welcome to create a 
[Work-in-progress PR](https://github.blog/2019-02-14-introducing-draft-pull-requests/)
so that I and everyone else can give feedback as soon as possible. 


## Before requesting a PR review

Make sure that:

- all tests are passing (see [README.md](README.md) on how to run tests)
- if you created a new template: it contains a file `test-inputs.yml`, which specifies 
a few input values to test the code template (the test is then automatically run by 
pytest)
- you checked all new functionality live, i.e. in the running web app
- you formatted all code with [black](https://github.com/psf/black)
- any generated code is formatted nicely, both in .py and in .ipynb ("nicely" = 
comparable to the existing templates)
- you added comments in your code that explain what it does
- the PR explains in detail what's new
