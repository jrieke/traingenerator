# Want to contribute?

That's very welcome! :heart:


## Before you start

It's best if you get in touch with me so we can quickly check that your plan makes 
sense and nobody else is working on this. The best way is to open an issue on this repo 
but you can also contact me on [Twitter](https://twitter.com/jrieke) or 
[e-mail](mailto:johannes.rieke@gmail.com).


## Before opening a PR

Make sure that:

- all tests are passing (see [README.md](README.md) on how to run tests)
- each new template dir contains a file `test-inputs.yml` that specifies a few input 
values to test the template (the template is then automatically tested by pytest)
- you tested all new functionality live, i.e. in the running web app
- you formatted all code with [black](https://github.com/psf/black)
- any generated code is formatted nicely, both in .py and in .ipynb ("nicely" = 
comparable to the existing templates)
- you added comments in your code that explain what it does
- the PR explains in detail what's new


## Some ideas for future work

- add template for pytorch-lightning
- add template for keras/tensorflow
- add templates for other tasks, e.g. object detection, segmentation, 
text classification, ...
- allow more options in the sidebar (e.g. more hyperparameters)
- add some tensorboard visualizations
