from mongo_rag_agent.app import main


def test_app_import():
    assert callable(main)
