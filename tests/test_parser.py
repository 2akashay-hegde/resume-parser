from pathlib import Path

from app.parser import parse_resume


def test_parse_resume_extracts_key_fields() -> None:
    text = """
    John Doe
    john.doe@example.com
    +1 555-123-4567
    Skills: Python, JavaScript, SQL
    Education: B.Tech in Computer Science
    Experience: Senior Software Engineer at Acme Corp for 5 years
    """

    result = parse_resume(text)

    assert result["name"] == "John Doe"
    assert result["email"] == "john.doe@example.com"
    assert result["phone"] == "+1 555-123-4567"
    assert "Python" in result["skills"]
    assert "JavaScript" in result["skills"]
    assert "B.Tech in Computer Science" in result["education"]
    assert "Senior Software Engineer at Acme Corp for 5 years" in result["experience"]


def test_parse_resume_from_sample_fixture() -> None:
    fixture_path = Path(__file__).parent / "sample_data" / "sample_resume_1.txt"
    text = fixture_path.read_text(encoding="utf-8")

    result = parse_resume(text)

    assert result["name"] == "John Doe"
    assert result["email"] == "john.doe@example.com"
    assert result["phone"] == "+1 555-123-4567"
    assert "Python" in result["skills"]
    assert "Docker" in result["skills"]
    assert "B.Tech in Computer Science" in result["education"]
    assert "Senior Software Engineer at Acme Corp for 5 years" in result["experience"]
