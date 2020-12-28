# Want to contribute?

That's very welcome! :heart:


## Before you start

It's best if you get in touch with me so we can quickly check that your plan makes 
sense and nobody else is working on it. The best way is to [write on Gitter](https://gitter.im/jrieke/traingenerator) 
or open an issue in this repo. You can also reach out on [Twitter](https://twitter.com/jrieke) 
or via [e-mail](mailto:johannes.rieke@gmail.com) if that makes you feel more comfortable :)

As soon as you start working, it's great if you create a 
[work-in-progress PR](https://github.blog/2019-02-14-introducing-draft-pull-requests/)
so that I and everyone else can give feedback as soon as possible. 


## Before requesting a PR review

Make sure that:

- all tests are passing (see [README.md](README.md) on how to run tests)
- if you created a new template: it contains a file `test-inputs.yml`, which specifies 
a few input values to test the code template (the test is then automatically run by 
pytest)
- you formatted all code with [black](https://github.com/psf/black)
- you checked all new functionality live, i.e. in the running web app
- any generated code is formatted nicely, both in .py and in .ipynb ("nicely" = 
comparable to the existing templates)
- you added comments in your code that explain what it does
- the PR explains in detail what's new
