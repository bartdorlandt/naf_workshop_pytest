from socket import timeout


def connect(host: str, retries: int = 3):
    """Connect to a network device. Raises on failure."""
    raise NotImplementedError("Replace with a real driver call")


def deploy_config(host: str, config: str, retries: int = 3):
    """Deploy configuration to a device, retrying on transient failures."""
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            device = connect(host)
            device.load_merge_candidate(config=config)
            device.commit_config()
            return
        except Exception as exc:
            last_exc = exc
    raise RuntimeError(f"Failed after {retries} attempts") from last_exc
