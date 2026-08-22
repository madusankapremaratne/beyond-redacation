import os

try:
    from dotenv import load_dotenv
    if os.path.exists(".env.local"):
        load_dotenv(".env.local")
    else:
        load_dotenv()
except ImportError:
    pass

def get_api_key(key_name: str = "NVIDIA_API_KEY") -> str:
    """
    Retrieve API key securely across Google Colab and local environments.
    """
    # 1. Try Google Colab secret manager
    try:
        from google.colab import userdata
        val = userdata.get(key_name)
        if val:
            return val
    except Exception:
        pass

    # 2. Fall back to local environment / .env / .env.local file
    val = os.environ.get(key_name)
    if val:
        return val

    print(f"[WARNING] Key '{key_name}' not found in Colab secrets or environment variables.")
    return ""

def get_hf_token() -> str:
    """
    Retrieve Hugging Face API Token (HF_TOKEN) securely.
    """
    return get_api_key("HF_TOKEN")

def get_data_dir() -> str:
    """
    Get persistent data directory path across Google Colab and local environments.
    Creates the directory if it does not exist.
    """
    # 1. Check Google Colab Drive mounts
    colab_paths = [
        "/content/drive/MyDrive/beyond-redaction-data",
        "/content/drive/My Drive/beyond-redaction-data"
    ]
    for cp in colab_paths:
        if os.path.exists(os.path.dirname(cp)):
            os.makedirs(cp, exist_ok=True)
            return cp

    # 2. Local fallback
    data_dir = os.environ.get("DATA_DIR", "./data")
    data_dir = os.path.abspath(data_dir)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

