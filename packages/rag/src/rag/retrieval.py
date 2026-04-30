import lancedb
from backend.constants import VECTOR_DB_PATH, TABLE_NAME

db = lancedb.connect(VECTOR_DB_PATH)


def retrieve_documents(query: str, k: int = 3):
    results = db[TABLE_NAME].search(query).limit(k).to_list()
    return [
        {
            "document_name": result["document_name"],
            "file_path": result["file_path"],
            "content": result["content"],
            "distance": result["_distance"],
        }
        for result in results
    ]


def get_document(document_name: str):
    table = db[TABLE_NAME]
    df = table.to_pandas()
    match = df[df["document_name"] == document_name]
    if match.empty:
        return None

    row = match.iloc[-1]
    return {
        "document_name": str(row["document_name"]),
        "file_path": str(row["file_path"]),
        "content": str(row["content"]),
    }


def list_document_names(*, include_extension: bool = False):
    table = db[TABLE_NAME]
    df = table.to_pandas()
    if df.empty or "document_name" not in df.columns:
        return []
    # preserve insertion order of first occurrence while de-duping
    names = list(dict.fromkeys(df["document_name"].astype(str).tolist()))
    if include_extension:
        return names
    return [name.removesuffix(".md") for name in names]
