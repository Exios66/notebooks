"""
Dataset Loaders for Fine-tuning
Load datasets from HuggingFace, GitHub, Seaborn, and other open dataset platforms
"""

import os
import pandas as pd
from typing import Dict, List, Optional, Union, Tuple
from pathlib import Path
import json
from urllib.parse import urlparse

try:
    from datasets import load_dataset, Dataset, DatasetDict
    from huggingface_hub import list_datasets
    DATASETS_AVAILABLE = True
except ImportError:
    DATASETS_AVAILABLE = False
    print("Warning: 'datasets' library not installed. Install with: pip install datasets")

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    print("Warning: 'seaborn' library not installed. Install with: pip install seaborn")

try:
    from sklearn.datasets import fetch_openml, load_iris, load_wine, load_breast_cancer, load_diabetes
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Warning: 'scikit-learn' library not installed. Install with: pip install scikit-learn")


# HuggingFace Datasets for Fine-tuning
HUGGINGFACE_CHAT_DATASETS = {
    # Instruction following datasets
    "alpaca": "tatsu-lab/alpaca",
    "alpaca_gpt4": "vicgalle/alpaca-gpt4",
    "dolly": "databricks/databricks-dolly-15k",
    "open_orca": "Open-Orca/OpenOrca",
    "ultrachat": "stingning/ultrachat",
    "sharegpt": "anon8231489123/ShareGPT_Vicuna_unfiltered",

    # Question answering
    "squad": "squad",
    "squad_v2": "squad_v2",
    "natural_questions": "natural_questions",
    "ms_marco": "ms_marco",

    # Conversational datasets
    "personachat": "bavard/personachat_truecased",
    "wizard_of_wikipedia": "facebook/wizard_of_wikipedia",
    "empathetic_dialogues": "empathetic_dialogues",
    "daily_dialog": "daily_dialog",

    # Code datasets
    "the_stack": "bigcode/the-stack",
    "code_search_net": "code_search_net",
    "github_python": "bigcode/python_code",

    # Summarization
    "cnn_dailymail": "cnn_dailymail",
    "xsum": "xsum",
    "samsum": "samsum",

    # Translation
    "opus": "Helsinki-NLP/opus_books",
    "wmt14": "wmt14",
    "flores": "facebook/flores",

    # Sentiment analysis
    "imdb": "imdb",
    "yelp_review": "yelp_review_full",
    "amazon_polarity": "amazon_polarity",

    # Classification
    "ag_news": "ag_news",
    "dbpedia_14": "dbpedia_14",
    "yahoo_answers": "yahoo_answers_topics",

    # Math and reasoning
    "gsm8k": "gsm8k",
    "math": "hendrycks/competition_math",
    "mmlu": "cais/mmlu",
    "hellaswag": "hellaswag",
    "arc": "allenai/arc",

    # Safety and alignment
    "anthropic_hh": "Anthropic/hh-rlhf",
    "oasst1": "OpenAssistant/oasst1",
    "beavertails": "PKU-Alignment/beavertails",
}

# Seaborn datasets
SEABORN_DATASETS = [
    "anscombe", "attention", "brain_networks", "car_crashes", "diamonds",
    "dots", "exercise", "flights", "fmri", "geyser", "iris", "mpg",
    "penguins", "planets", "tips", "titanic"
]

# Scikit-learn datasets
SKLEARN_DATASETS = {
    "iris": load_iris,
    "wine": load_wine,
    "breast_cancer": load_breast_cancer,
    "diabetes": load_diabetes,
}

# OpenML datasets (popular ones)
OPENML_DATASETS = {
    "adult": 1590,  # Adult income dataset
    "bank_marketing": 1461,
    "credit_g": 31,
    "diabetes": 37,
    "heart_disease": 38,
    "mushroom": 24,
    "nursery": 26,
    "tic_tac_toe": 50,
    "vote": 56,
    "zoo": 62,
}


class DatasetLoader:
    """
    Unified loader for datasets from multiple sources
    """

    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize dataset loader

        Args:
            cache_dir: Directory to cache downloaded datasets
        """
        self.cache_dir = cache_dir or os.path.join(Path.home(), ".cache", "datasets")
        os.makedirs(self.cache_dir, exist_ok=True)

    def load_huggingface(
        self,
        dataset_name: str,
        split: Optional[Union[str, List[str]]] = None,
        streaming: bool = False,
        **kwargs
    ) -> Union[Dataset, DatasetDict]:
        """
        Load a dataset from HuggingFace

        Args:
            dataset_name: Name or path of the dataset
            split: Dataset split(s) to load (e.g., 'train', 'test', ['train', 'validation'])
            streaming: Whether to use streaming mode for large datasets
            **kwargs: Additional arguments for load_dataset

        Returns:
            HuggingFace Dataset or DatasetDict

        Example:
            >>> loader = DatasetLoader()
            >>> dataset = loader.load_huggingface("squad", split="train")
        """
        if not DATASETS_AVAILABLE:
            raise ImportError("'datasets' library is required. Install with: pip install datasets")

        try:
            # Check if it's a predefined dataset
            if dataset_name in HUGGINGFACE_CHAT_DATASETS:
                dataset_name = HUGGINGFACE_CHAT_DATASETS[dataset_name]

            dataset = load_dataset(
                dataset_name,
                split=split,
                streaming=streaming,
                cache_dir=self.cache_dir,
                **kwargs
            )
            return dataset
        except Exception as e:
            raise Exception(f"Failed to load HuggingFace dataset '{dataset_name}': {str(e)}")

    def load_seaborn(self, dataset_name: str) -> pd.DataFrame:
        """
        Load a dataset from Seaborn

        Args:
            dataset_name: Name of the seaborn dataset

        Returns:
            pandas DataFrame

        Example:
            >>> loader = DatasetLoader()
            >>> df = loader.load_seaborn("titanic")
        """
        if not SEABORN_AVAILABLE:
            raise ImportError("'seaborn' library is required. Install with: pip install seaborn")

        if dataset_name not in SEABORN_DATASETS:
            raise ValueError(
                f"Unknown seaborn dataset '{dataset_name}'. "
                f"Available: {', '.join(SEABORN_DATASETS)}"
            )

        try:
            return sns.load_dataset(dataset_name)
        except Exception as e:
            raise Exception(f"Failed to load seaborn dataset '{dataset_name}': {str(e)}")

    def load_sklearn(self, dataset_name: str, return_X_y: bool = False) -> Union[Tuple, Dict]:
        """
        Load a dataset from scikit-learn

        Args:
            dataset_name: Name of the sklearn dataset
            return_X_y: If True, return (data, target) tuple instead of Bunch object

        Returns:
            Dataset as Bunch object or (X, y) tuple

        Example:
            >>> loader = DatasetLoader()
            >>> data = loader.load_sklearn("iris")
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("'scikit-learn' library is required. Install with: pip install scikit-learn")

        if dataset_name not in SKLEARN_DATASETS:
            raise ValueError(
                f"Unknown sklearn dataset '{dataset_name}'. "
                f"Available: {', '.join(SKLEARN_DATASETS.keys())}"
            )

        loader_func = SKLEARN_DATASETS[dataset_name]
        return loader_func(return_X_y=return_X_y)

    def load_openml(
        self,
        dataset_id: Union[int, str],
        version: Optional[int] = None,
        as_frame: bool = True
    ) -> Union[pd.DataFrame, Tuple]:
        """
        Load a dataset from OpenML

        Args:
            dataset_id: OpenML dataset ID or name from OPENML_DATASETS
            version: Dataset version (optional)
            as_frame: Return as pandas DataFrame

        Returns:
            Dataset as DataFrame or (X, y) tuple

        Example:
            >>> loader = DatasetLoader()
            >>> df = loader.load_openml("adult")
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError("'scikit-learn' library is required. Install with: pip install scikit-learn")

        # Check if it's a predefined dataset name
        if isinstance(dataset_id, str) and dataset_id in OPENML_DATASETS:
            dataset_id = OPENML_DATASETS[dataset_id]

        try:
            dataset = fetch_openml(
                data_id=dataset_id if isinstance(dataset_id, int) else None,
                name=dataset_id if isinstance(dataset_id, str) else None,
                version=version,
                as_frame=as_frame,
                return_X_y=not as_frame,
                cache=True,
                data_home=self.cache_dir
            )
            return dataset
        except Exception as e:
            raise Exception(f"Failed to load OpenML dataset '{dataset_id}': {str(e)}")

    def load_from_github(
        self,
        repo_url: str,
        file_path: str,
        file_format: str = "csv",
        **kwargs
    ) -> pd.DataFrame:
        """
        Load a dataset from a GitHub repository

        Args:
            repo_url: GitHub repository URL (e.g., 'https://github.com/user/repo')
            file_path: Path to the file in the repository
            file_format: File format ('csv', 'json', 'tsv', 'parquet')
            **kwargs: Additional arguments for pandas read function

        Returns:
            pandas DataFrame

        Example:
            >>> loader = DatasetLoader()
            >>> df = loader.load_from_github(
            ...     "https://github.com/mwaskom/seaborn-data",
            ...     "titanic.csv"
            ... )
        """
        # Convert GitHub URL to raw content URL
        if "github.com" in repo_url:
            repo_url = repo_url.replace("github.com", "raw.githubusercontent.com")
            if not repo_url.endswith("/"):
                repo_url += "/"
            if not repo_url.endswith("main/") and not repo_url.endswith("master/"):
                repo_url += "main/"  # Default to main branch

        file_url = f"{repo_url}{file_path}"

        try:
            if file_format == "csv":
                return pd.read_csv(file_url, **kwargs)
            elif file_format == "json":
                return pd.read_json(file_url, **kwargs)
            elif file_format == "tsv":
                return pd.read_csv(file_url, sep="\t", **kwargs)
            elif file_format == "parquet":
                return pd.read_parquet(file_url, **kwargs)
            else:
                raise ValueError(f"Unsupported file format: {file_format}")
        except Exception as e:
            raise Exception(f"Failed to load dataset from GitHub: {str(e)}")

    def load_from_url(
        self,
        url: str,
        file_format: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load a dataset from a direct URL

        Args:
            url: Direct URL to the dataset file
            file_format: File format (auto-detected if None)
            **kwargs: Additional arguments for pandas read function

        Returns:
            pandas DataFrame

        Example:
            >>> loader = DatasetLoader()
            >>> df = loader.load_from_url("https://example.com/data.csv")
        """
        if file_format is None:
            # Auto-detect from URL
            parsed = urlparse(url)
            file_format = os.path.splitext(parsed.path)[1][1:]  # Remove leading dot

        try:
            if file_format == "csv" or url.endswith(".csv"):
                return pd.read_csv(url, **kwargs)
            elif file_format == "json" or url.endswith(".json"):
                return pd.read_json(url, **kwargs)
            elif file_format == "tsv" or url.endswith(".tsv"):
                return pd.read_csv(url, sep="\t", **kwargs)
            elif file_format == "parquet" or url.endswith(".parquet"):
                return pd.read_parquet(url, **kwargs)
            else:
                # Try CSV as default
                return pd.read_csv(url, **kwargs)
        except Exception as e:
            raise Exception(f"Failed to load dataset from URL: {str(e)}")

    def load_from_file(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Load a dataset from a local file

        Args:
            file_path: Path to the local file
            **kwargs: Additional arguments for pandas read function

        Returns:
            pandas DataFrame
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        suffix = file_path.suffix.lower()

        try:
            if suffix == ".csv":
                return pd.read_csv(file_path, **kwargs)
            elif suffix == ".json":
                return pd.read_json(file_path, **kwargs)
            elif suffix == ".tsv":
                return pd.read_csv(file_path, sep="\t", **kwargs)
            elif suffix == ".parquet":
                return pd.read_parquet(file_path, **kwargs)
            elif suffix == ".xlsx" or suffix == ".xls":
                return pd.read_excel(file_path, **kwargs)
            else:
                raise ValueError(f"Unsupported file format: {suffix}")
        except Exception as e:
            raise Exception(f"Failed to load dataset from file: {str(e)}")

    def list_huggingface_datasets(self, search: Optional[str] = None) -> List[str]:
        """
        List available HuggingFace datasets

        Args:
            search: Optional search term to filter datasets

        Returns:
            List of dataset names
        """
        if not DATASETS_AVAILABLE:
            raise ImportError("'datasets' library is required")

        try:
            if search:
                datasets = list_datasets(search=search)
            else:
                datasets = list_datasets()
            return [d.id for d in datasets]
        except Exception as e:
            print(f"Warning: Could not list HuggingFace datasets: {e}")
            return list(HUGGINGFACE_CHAT_DATASETS.keys())

    def convert_to_chat_format(
        self,
        dataset: Union[Dataset, pd.DataFrame],
        instruction_col: str = "instruction",
        input_col: Optional[str] = "input",
        output_col: str = "output",
        system_col: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Convert a dataset to chat format for fine-tuning

        Args:
            dataset: HuggingFace Dataset or pandas DataFrame
            instruction_col: Column name for instructions
            input_col: Column name for input (optional)
            output_col: Column name for output/response
            system_col: Column name for system prompt (optional)

        Returns:
            List of message dictionaries in chat format

        Example:
            >>> loader = DatasetLoader()
            >>> dataset = loader.load_huggingface("alpaca", split="train")
            >>> chat_data = loader.convert_to_chat_format(
            ...     dataset,
            ...     instruction_col="instruction",
            ...     input_col="input",
            ...     output_col="output"
            ... )
        """
        messages_list = []

        # Convert to pandas if needed
        if isinstance(dataset, Dataset):
            df = dataset.to_pandas()
        else:
            df = dataset.copy()

        for _, row in df.iterrows():
            messages = []

            # Add system message if available
            if system_col and system_col in row and pd.notna(row[system_col]):
                messages.append({
                    "role": "system",
                    "content": str(row[system_col])
                })

            # Build user message
            user_content = str(row[instruction_col])
            if input_col and input_col in row and pd.notna(row[input_col]) and str(row[input_col]).strip():
                user_content += f"\n\nInput: {row[input_col]}"

            messages.append({
                "role": "user",
                "content": user_content
            })

            # Add assistant response
            messages.append({
                "role": "assistant",
                "content": str(row[output_col])
            })

            messages_list.append(messages)

        return messages_list

    def save_chat_format(
        self,
        chat_data: List[Dict[str, str]],
        output_path: str,
        format: str = "jsonl"
    ):
        """
        Save chat format data to file

        Args:
            chat_data: List of message dictionaries
            output_path: Path to save the file
            format: File format ('jsonl', 'json', 'csv')
        """
        output_path = Path(output_path)

        if format == "jsonl":
            with open(output_path, "w", encoding="utf-8") as f:
                for item in chat_data:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")
        elif format == "json":
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(chat_data, f, indent=2, ensure_ascii=False)
        elif format == "csv":
            # Flatten for CSV (simplified)
            rows = []
            for item in chat_data:
                row = {}
                for i, msg in enumerate(item):
                    row[f"role_{i}"] = msg["role"]
                    row[f"content_{i}"] = msg["content"]
                rows.append(row)
            df = pd.DataFrame(rows)
            df.to_csv(output_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")


# Convenience functions
def load_huggingface_dataset(dataset_name: str, **kwargs):
    """Convenience function to load HuggingFace dataset"""
    loader = DatasetLoader()
    return loader.load_huggingface(dataset_name, **kwargs)


def load_seaborn_dataset(dataset_name: str):
    """Convenience function to load Seaborn dataset"""
    loader = DatasetLoader()
    return loader.load_seaborn(dataset_name)


def get_available_datasets() -> Dict[str, List[str]]:
    """
    Get list of all available datasets from different sources

    Returns:
        Dictionary mapping source names to lists of dataset names
    """
    return {
        "huggingface": list(HUGGINGFACE_CHAT_DATASETS.keys()),
        "seaborn": SEABORN_DATASETS,
        "sklearn": list(SKLEARN_DATASETS.keys()),
        "openml": list(OPENML_DATASETS.keys()),
    }
