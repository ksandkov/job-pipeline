from jobpipeline.pipeline import dedupe


def test_dedupe_removes_duplicates():
    jobs = [
        {"title": "SRE", "company": "A", "location": "Remote"},
        {"title": "SRE", "company": "A", "location": "Remote"},
        {"title": "SRE", "company": "B", "location": "Remote"},
    ]
    assert len(dedupe(jobs)) == 2


def test_dedupe_preserves_order():
    jobs = [
        {"title": "1", "company": "A", "location": "X"},
        {"title": "2", "company": "B", "location": "Y"},
    ]
    assert [j["title"] for j in dedupe(jobs)] == ["1", "2"]
