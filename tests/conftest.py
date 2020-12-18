def pytest_addoption(parser):
    parser.addoption(
        "--template",
        action="store",
        default=None,
        help="Name of the template dir to test (default: all)",
    )

