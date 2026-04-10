# Root launcher for the production package
#
# Flow:
# 1. Add the `src/` package directory to Python path so package imports resolve.
# 2. Import the application entrypoint from `src/mongo_rag_agent/app.py`.
# 3. Run the top-level `main()` function to execute the RAG workflow.
#
# Tool connections (handled inside package):
# - get_information_for_question_answering: vector search over MongoDB chunked documents.
# - get_page_content_for_summarization: lookup full documentation page content.
#
# This launcher keeps the repository runnable directly with `python main.py`
# while preserving the package-based production layout.

import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from mongo_rag_agent.app import main


if __name__ == "__main__":
    main()