"""
Test the code templates by rendering them for different parameter combinations
and checking that the code runs without errors.
"""
import sys
import os

# Activate this in case we need to import some functions, e.g. from utils.
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import yaml
import itertools
from jinja2 import Environment, FileSystemLoader
import pytest
import tempfile

# import shutil


# def render_template(**kwargs):
#     """Renders template (passing in kwargs) and returns Python code."""
#     env = Environment(
#         loader=FileSystemLoader("templates"), trim_blocks=True, lstrip_blocks=True,
#     )
#     template = env.get_template(f"image_classification_{kwargs['framework']}.py.jinja")
#     code = template.render(header=lambda x: "", notebook=False, **kwargs)
#     return code


def exec_in_tmp_dir(code):
    """Executes code in temporary working directory."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        cwd = os.getcwd()
        os.chdir(tmp_dir)
        # print("Execute code in:", os.getcwd())
        try:
            exec(code, globals())
        finally:
            os.chdir(cwd)
        # print("Back to:", os.getcwd())


class PseudoDirEntry:
    def __init__(self, path):
        self.path = os.path.realpath(path)
        self.name = os.path.basename(self.path)
        self.is_dir = os.path.isdir(self.path)
        self.stat = lambda: os.stat(self.path)


def test_all_templates(subtests, pytestconfig):
    """
    Automatically tests all templates in the templates dir. 
    
    For every template, it renders the code (with input values defined in the 
    accompanying test-inputs.yml file) and checks that it runs without errors.
    """

    # TODO: This tests all templates in one big test function. This makes it hard
    # to find out what went wrong. Ideally, generate tests on the fly, e.g. sth like:
    # generate_test(template, inputs).run()

    # Find available templates (based on --template option).
    template_option = pytestconfig.getoption("template")
    if template_option is None:  # use all templates except for "example" (default)
        template_dirs = [
            f for f in os.scandir("templates") if f.is_dir() and f.name != "example"
        ]
    else:  # use only given template
        template_dirs = [PseudoDirEntry(os.path.join("templates", template_option))]
        if not os.path.exists(template_dirs[0].path):
            raise ValueError(
                "Template option given but no matching template found: "
                f"{template_option}"
            )

    # print(template_dirs)
    # assert False

    for template_dir in template_dirs:
        # Load template from "code-template.py.jinja".
        env = Environment(
            loader=FileSystemLoader(template_dir.path),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        template = env.get_template(f"code-template.py.jinja")

        # Load test inputs from "test-inputs.yml".
        with open(os.path.join(template_dir.path, "test-inputs.yml"), "r") as f:
            input_dict = yaml.safe_load(f)

        # Compute all possible combinations of test inputs.
        if input_dict:
            keys, values = zip(*input_dict.items())
            # Wrap single elements in list.
            values = [v if isinstance(v, list) else [v] for v in values]
            # print(values)
            # print(itertools.product(*values))
            input_combinations = [
                dict(zip(keys, v)) for v in itertools.product(*values)
            ]
            # print(input_combinations)
        else:  # no input values defined
            input_combinations = [{}]

        # Generate and execute code (in tmp dir, so logs are not stored here).
        # TODO: Use parametrize instead of for loop here.
        for inputs in input_combinations:
            inputs_str = ",".join(f"{k}={v}" for k, v in inputs.items())
            with subtests.test(msg=template_dir.name + "---" + inputs_str):
                # print(inputs)
                code = template.render(header=lambda x: "", notebook=False, **inputs)
                exec_in_tmp_dir(code)
                # assert False


# a_list = [1, 2, 3]
# input_combinations = [[1, 2], [3, 4]]


# @pytest.mark.parametrize("a", a_list)
# @pytest.mark.parametrize("inputs", input_combinations)
# def test_abc(a, inputs):
#     a ** 2


# @pytest.mark.parametrize(
#     "model_func", ["sklearn.svm.SVC", "sklearn.linear_model.Perceptron"]
# )
# @pytest.mark.parametrize("data_format", ["Numpy arrays", "Image files"])
# @pytest.mark.parametrize("scale_mean_std", [True, False])
# @pytest.mark.parametrize("visualization_tool", ["Not at all", "Tensorboard"])
# def test_sklearn_code(
#     model_func, data_format, scale_mean_std, visualization_tool, tmp_path
# ):
#     code = render_template(
#         framework="scikit-learn",
#         model_func=model_func,
#         data_format=data_format,
#         resize_pixels=28,
#         crop_pixels=28,
#         scale_mean_std=scale_mean_std,
#         visualization_tool=visualization_tool,
#     )
#     # if data_format == "Image files":  # copy some test data
#     #     shutil.copytree(
#     #         "tests/data/image-classification-data", tmp_path / "path/to/data/dir"
#     #     )
#     execute_code(code, tmp_path)


# @pytest.mark.parametrize("model_func", ["resnet18"])
# @pytest.mark.parametrize("data_format", ["Numpy arrays", "Image files"])
# @pytest.mark.parametrize("gpu", [True, False])  # this will only use GPU if available
# @pytest.mark.parametrize("checkpoint", [True, False])
# @pytest.mark.parametrize("visualization_tool", ["Not at all", "Tensorboard"])
# def test_pytorch_code(
#     model_func, data_format, gpu, checkpoint, visualization_tool, tmp_path
# ):
#     code = render_template(
#         framework="PyTorch",
#         model_func=model_func,
#         pretrained=False,
#         data_format=data_format,
#         gpu=gpu,
#         checkpoint=checkpoint,
#         loss="CrossEntropyLoss",
#         optimizer="Adam",
#         lr=0.001,
#         batch_size=128,
#         num_epochs=1,
#         print_every=1,
#         visualization_tool=visualization_tool,
#     )
#     # if data_format == "Image files":  # copy some test data
#     #     shutil.copytree(
#     #         "tests/data/image-classification-data", tmp_path / "path/to/data/dir"
#     #     )
#     execute_code(code, tmp_path)

