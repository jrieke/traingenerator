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
import runpy


def run_in_tmp_dir(code):
    """Executes code in temporary working directory."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        cwd = os.getcwd()
        os.chdir(tmp_dir)

        # Use runpy instead of exec here because a) it doesn't interfere with
        # globals and b) it gives better error messages.
        with open("code.py", "w") as f:
            f.write(code)
        try:
            runpy.run_path("code.py")
        finally:
            os.chdir(cwd)


class PseudoDirEntry:
    def __init__(self, path):
        self.path = os.path.realpath(path)
        self.name = os.path.basename(path)


def test_all_templates(subtests, pytestconfig):
    """
    Automatically tests all templates in the templates dir. 
    
    For every template, it renders the code (with input values defined in the 
    accompanying test-inputs.yml file) and checks that it runs without errors.
    Uses the pytest-subtests package to run each template/combination of input values 
    in its own test.
    """

    # TODO: This uses pytest-subtests at the moment. This is better than testing
    # everything at once in this function but it's still not perfect:
    # - doesn't run tests in parallel
    # - doesn't produce intermediate output while running the tests
    # - runs the code via exec which doesn't give good errors

    # Find available templates (based on --template option).
    template_option = pytestconfig.getoption("template")
    if template_option is None:
        # Default: Use all templates except for "example" and ones that don't contain
        # "test-inputs.yml".
        template_dirs = [
            f
            for f in os.scandir("templates")
            if f.is_dir()
            and f.name != "example"
            and os.path.isfile(os.path.join(f, "test-inputs.yml"))
        ]
    else:
        # Use only the template specified via --template.
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
                run_in_tmp_dir(code)
                # assert False


# a_list = [1, 2, 3]
# input_combinations = [[1, 2], [3, 4]]


# @pytest.mark.parametrize("a", a_list)
# @pytest.mark.parametrize("inputs", input_combinations)
# def test_abc(a, inputs):
#     a ** 2
