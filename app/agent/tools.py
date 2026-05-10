from google.adk.tools import FunctionTool


def _hello_world() -> str:
    """Prints hello world. Use this to test that tool calling is working."""
    print("Hello, world (sneed)")
    return "Hello, world!"


hello_world = FunctionTool(_hello_world)
