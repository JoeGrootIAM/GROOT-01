"""GROOT-01 interactive assistant entry point."""

from .config import load_config
from .llm import LocalLLM
from .logger import setup_logging
from .memory import load_memory
from .policy import check_ram_policy



def main():
    """Start GROOT and enter the interactive conversation loop."""
    config = load_config()

    assistant = config["assistant"]
    model_config = config["model"]
    resource_policy = config["resource_policy"]
    paths = config["paths"]

    logger = setup_logging(
        f"{paths['logs']}/groot.log"
    )

    logger.info(
        "STARTUP | OK | %s v%s",
        assistant["name"],
        assistant["version"],
    )

    print()
    print("================================")
    print(f"          {assistant['name']}-01")
    print("   Personal AI Assistant")
    print("================================")
    print()

    ram_allowed = check_ram_policy(
        logger,
        resource_policy["min_free_ram_mb"],
    )

    if not ram_allowed:
        print("GROOT cannot safely start.")
        print("Resource policy refused startup.")
        return

    memory = load_memory()

    logger.info(
        "MEMORY_LOAD | OK | sections=%s",
        len(memory),
    )

    print(
        f"Persistent memory loaded: {len(memory)} section(s)."
    )

    llm = LocalLLM(
        model_path=model_config["path"],
        context_size=model_config["context_size"],
        threads=model_config["threads"],
        temperature=model_config["temperature"],
        max_tokens=model_config["max_tokens"],
    )

    print("Loading local model...")
    llm.load()

    logger.info(
        "MODEL_LOAD | OK | path=%s context=%s threads=%s",
        model_config["path"],
        model_config["context_size"],
        model_config["threads"],
    )

    print("Model loaded.")
    print()
    print("GROOT is ready.")
    print("Type 'exit' or 'quit' to stop.")
    print()

    try:
        while True:
            try:
                user_input = input("You: ").strip()
            except EOFError:
                print()
                break

            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit"}:
                break

            logger.info(
                "USER_INPUT | OK | chars=%s",
                len(user_input),
            )

            try:
                response = llm.generate(user_input)
            except Exception as exc:
                logger.exception(
                    "MODEL_GENERATION | ERROR | %s",
                    exc,
                )
                print(f"GROOT error: {exc}")
                continue

            print()
            print(f"GROOT: {response}")
            print()

            logger.info(
                "MODEL_GENERATION | OK | chars=%s",
                len(response),
            )

    except KeyboardInterrupt:
        print()
        print()

    finally:
        llm.unload()

        logger.info(
            "SHUTDOWN | OK | %s",
            assistant["name"],
        )

        print("GROOT stopped.")



if __name__ == "__main__":
    main()
