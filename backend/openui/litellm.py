import yaml
import os
import tempfile
import openai
from .logs import logger


def generate_config():
    models = []
    if "GEMINI_API_KEY" in os.environ:
        models.extend(
            [
                {
                    "model_name": "gemini-1.5-flash",
                    "litellm_params": {
                        "model": "gemini/gemini-1.5-flash-latest",
                    },
                },
                {
                    "model_name": "gemini-1.5-pro",
                    "litellm_params": {
                        "model": "gemini/gemini-1.5-pro-latest",
                    },
                },
                {
                    "model_name": "gemini-2.5-pro",
                    "litellm_params": {
                        "model": "gemini/gemini-2.5-flash-preview-04-17",
                    },
                },
                {
                    "model_name": "gemini-2.0-flash",
                    "litellm_params": {
                        "model": "gemini/gemini-2.0-flash",
                    },
                },
            ]
        )

    if "DEEPSEEK_API_KEY" in os.environ:
        models.extend(
            [
                {
                    "model_name": "deepseek-V3",
                    "litellm_params": {
                        "model": "deepseek/deepseek-chat",
                        "max_tokens": 1234567
                    },
                },
                {
                    "model_name": "deepseek-R1",
                    "litellm_params": {
                        "model": "deepseek/deepseek-reasoner",
                    },
                },
            ]
        )

    if "ANTHROPIC_API_KEY" in os.environ:
        models.extend(
            [
                {
                    "model_name": "claude-3-opus",
                    "litellm_params": {
                        "model": "claude-3-opus-20240229",
                    },
                },
                {
                    "model_name": "claude-3-5-sonnet",
                    "litellm_params": {
                        "model": "claude-3-5-sonnet-20240620",
                    },
                },
                {
                    "model_name": "claude-3-haiku",
                    "litellm_params": {
                        "model": "claude-3-haiku-20240307",
                    },
                },
            ]
        )

    if "COHERE_API_KEY" in os.environ:
        models.extend(
            [
                {
                    "model_name": "command-r-plus",
                    "litellm_params": {
                        "model": "command-r-plus",
                    },
                },
                {
                    "model_name": "command-r",
                    "litellm_params": {
                        "model": "command-r",
                    },
                },
                {
                    "model_name": "command-light",
                    "litellm_params": {
                        "model": "command-light",
                    },
                },
            ]
        )

    if "MISTRAL_API_KEY" in os.environ:
        models.extend(
            [
                {
                    "model_name": "mistral-small",
                    "litellm_params": {
                        "model": "mistral/mistral-small-latest",
                    },
                },
                {
                    "model_name": "mistral-medium",
                    "litellm_params": {
                        "model": "mistral/mistral-medium-latest",
                    },
                },
                {
                    "model_name": "mistral-large",
                    "litellm_params": {
                        "model": "mistral/mistral-large-latest",
                    },
                },
            ]
        )

    if "OPENAI_COMPATIBLE_ENDPOINT" in os.environ:
        client = openai.OpenAI(
            api_key=os.getenv("OPENAI_COMPATIBLE_API_KEY"),
            base_url=os.getenv("OPENAI_COMPATIBLE_ENDPOINT"),
        )
        try:
            for model in client.models.list().data:
                models.append(
                    {
                        "model_name": model.id,
                        "litellm_params": {
                            "model": f"openai/{model.id}",
                            "api_key": os.getenv("OPENAI_COMPATIBLE_API_KEY"),
                            "base_url": os.getenv("OPENAI_COMPATIBLE_ENDPOINT"),
                        },
                    }
                )
        except Exception as e:
            logger.exception(
                f"Error listing models for {os.getenv('OPENAI_COMPATIBLE_ENDPOINT')}: %s",
                e,
            )

    yaml_structure = {"model_list": models}
    with tempfile.NamedTemporaryFile(
        delete=False, mode="w", suffix=".yaml"
    ) as tmp_file:
        tmp_file.write(yaml.dump(yaml_structure, sort_keys=False))
        tmp_file_path = tmp_file.name

    return tmp_file_path
