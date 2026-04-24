from agent.assistant import run
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


if __name__ == "__main__":
    try:
        result = run("Book BJJ next friday at 10 am til 12 am")
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
