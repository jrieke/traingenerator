"""
Test the code templates by rendering them for different parameter combinations
and checking that the code runs without errors.
"""
import sys
import os

# Activate this in case we need to import some functions, e.g. from utils.
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from jinja2 import Environment, FileSystemLoader
import pytest
# import shutil


def render_template(**kwargs):
    """Renders template (passing in kwargs) and returns Python code."""
    env = Environment(
        loader=FileSystemLoader("templates"), trim_blocks=True, lstrip_blocks=True,
    )
    template = env.get_template(f"image_classification_{kwargs['framework']}.py.jinja")
    code = template.render(header=lambda x: "", notebook=False, **kwargs)
    return code


def execute_code(code, tmp_path):
    """
    Executes code in temporary working directory.
    
    This is required so logs and checkpoints are not saved in the repo.
    """
    cwd = os.getcwd()
    os.chdir(tmp_path)
    # print("Execute code in:", os.getcwd())
    try:
        exec(code, globals())
    finally:
        os.chdir(cwd)
    # print("Back to:", os.getcwd())


@pytest.mark.parametrize(
    "model_func", ["sklearn.svm.SVC", "sklearn.linear_model.Perceptron"]
)
@pytest.mark.parametrize("data_format", ["Numpy arrays", "Image files"])
@pytest.mark.parametrize("scale_mean_std", [True, False])
@pytest.mark.parametrize("visualization_tool", ["Not at all", "Tensorboard"])
def test_sklearn_code(
    model_func, data_format, scale_mean_std, visualization_tool, tmp_path
):
    code = render_template(
        framework="scikit-learn",
        model_func=model_func,
        data_format=data_format,
        resize_pixels=28,
        crop_pixels=28,
        scale_mean_std=scale_mean_std,
        visualization_tool=visualization_tool,
    )
    # if data_format == "Image files":  # copy some test data
    #     shutil.copytree(
    #         "tests/data/image-classification-data", tmp_path / "path/to/data/dir"
    #     )
    execute_code(code, tmp_path)


@pytest.mark.parametrize("model_func", ["resnet18"])
@pytest.mark.parametrize("data_format", ["Numpy arrays", "Image files"])
@pytest.mark.parametrize("gpu", [True, False])  # this will only use GPU if available
@pytest.mark.parametrize("checkpoint", [True, False])
@pytest.mark.parametrize("visualization_tool", ["Not at all", "Tensorboard"])
def test_pytorch_code(
    model_func, data_format, gpu, checkpoint, visualization_tool, tmp_path
):
    code = render_template(
        framework="PyTorch",
        model_func=model_func,
        pretrained=False,
        data_format=data_format,
        gpu=gpu,
        checkpoint=checkpoint,
        loss="CrossEntropyLoss",
        optimizer="Adam",
        lr=0.001,
        batch_size=128,
        num_epochs=1,
        print_every=1,
        visualization_tool=visualization_tool,
    )
    # if data_format == "Image files":  # copy some test data
    #     shutil.copytree(
    #         "tests/data/image-classification-data", tmp_path / "path/to/data/dir"
    #     )
    execute_code(code, tmp_path)

