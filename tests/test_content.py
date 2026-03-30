"""Tests for Loan Officer Exam Prep content integrity."""
import pytest
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLASHCARDS_DIR = os.path.join(BASE_DIR, "flashcards")
PRACTICE_TESTS_DIR = os.path.join(BASE_DIR, "practice-tests")
SESSIONS_DIR = os.path.join(BASE_DIR, "sessions")


class TestDirectoryStructure:
    """Verify all expected directories and files exist."""

    def test_flashcards_directory_exists(self):
        assert os.path.isdir(FLASHCARDS_DIR)

    def test_practice_tests_directory_exists(self):
        assert os.path.isdir(PRACTICE_TESTS_DIR)

    def test_sessions_directory_exists(self):
        assert os.path.isdir(SESSIONS_DIR)

    def test_index_html_exists(self):
        assert os.path.isfile(os.path.join(BASE_DIR, "index.html"))

    def test_flashcard_files_exist(self):
        expected = [
            "acronyms-master-list.md",
            "all-laws-and-regulations.md",
            "key-numbers-and-dates.md",
            "protected-classes-and-laws.md",
        ]
        for f in expected:
            path = os.path.join(FLASHCARDS_DIR, f)
            assert os.path.isfile(path), f"Missing flashcard file: {f}"

    def test_practice_test_files_exist(self):
        expected = [
            "practice-test-01.md",
            "practice-test-02.md",
            "practice-test-03.md",
            "scenario-bank.md",
        ]
        for f in expected:
            path = os.path.join(PRACTICE_TESTS_DIR, f)
            assert os.path.isfile(path), f"Missing practice test file: {f}"

    def test_session_files_exist(self):
        for i in range(1, 17):
            pattern = f"session-{i:02d}-"
            matches = [
                f for f in os.listdir(SESSIONS_DIR) if f.startswith(pattern)
            ]
            assert len(matches) >= 1, f"Missing session file for session {i}"


class TestFlashcardContent:
    """Verify flashcard files have valid content."""

    def _read_file(self, filename):
        path = os.path.join(FLASHCARDS_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def test_acronyms_file_is_non_empty(self):
        content = self._read_file("acronyms-master-list.md")
        assert len(content) > 100, "Acronyms file is suspiciously short"

    def test_acronyms_contains_key_terms(self):
        content = self._read_file("acronyms-master-list.md")
        key_terms = ["TILA", "RESPA", "ECOA", "HMDA", "FCRA", "CFPB", "NMLS"]
        for term in key_terms:
            assert term in content, f"Acronyms file missing key term: {term}"

    def test_laws_file_is_non_empty(self):
        content = self._read_file("all-laws-and-regulations.md")
        assert len(content) > 100

    def test_key_numbers_file_is_non_empty(self):
        content = self._read_file("key-numbers-and-dates.md")
        assert len(content) > 100

    def test_protected_classes_file_is_non_empty(self):
        content = self._read_file("protected-classes-and-laws.md")
        assert len(content) > 100

    def test_all_flashcard_files_are_valid_markdown(self):
        """Every .md file should have at least one heading."""
        for filename in os.listdir(FLASHCARDS_DIR):
            if filename.endswith(".md"):
                content = self._read_file(filename)
                assert "#" in content, f"{filename} has no markdown headings"

    def test_no_empty_flashcard_files(self):
        for filename in os.listdir(FLASHCARDS_DIR):
            if filename.endswith(".md"):
                path = os.path.join(FLASHCARDS_DIR, filename)
                size = os.path.getsize(path)
                assert size > 0, f"{filename} is empty"


class TestPracticeTestContent:
    """Verify practice test files have valid structure."""

    def _read_file(self, filename):
        path = os.path.join(PRACTICE_TESTS_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def test_practice_tests_have_questions(self):
        for i in range(1, 4):
            content = self._read_file(f"practice-test-{i:02d}.md")
            question_count = len(re.findall(r"\*\*\d+\.\*\*", content))
            assert question_count >= 10, (
                f"practice-test-{i:02d}.md has only {question_count} questions"
            )

    def test_practice_tests_have_answer_choices(self):
        for i in range(1, 4):
            content = self._read_file(f"practice-test-{i:02d}.md")
            a_choices = len(re.findall(r"- A\)", content))
            b_choices = len(re.findall(r"- B\)", content))
            assert a_choices > 0, f"practice-test-{i:02d}.md has no A) choices"
            assert b_choices > 0, f"practice-test-{i:02d}.md has no B) choices"

    def test_practice_tests_have_answer_key(self):
        """Each practice test should have an answer key section."""
        for i in range(1, 4):
            content = self._read_file(f"practice-test-{i:02d}.md")
            has_answers = (
                "Answer Key" in content
                or "ANSWERS" in content
                or "answer key" in content.lower()
                or re.search(r"\d+\.\s*[A-D]", content) is not None
            )
            assert has_answers, f"practice-test-{i:02d}.md has no answer key"

    def test_scenario_bank_exists_and_has_content(self):
        content = self._read_file("scenario-bank.md")
        assert len(content) > 200, "Scenario bank is too short"

    def test_question_numbers_are_sequential(self):
        """Question numbers should be sequential within each test."""
        for i in range(1, 4):
            content = self._read_file(f"practice-test-{i:02d}.md")
            numbers = [
                int(m) for m in re.findall(r"\*\*(\d+)\.\*\*", content)
            ]
            if numbers:
                for j in range(1, len(numbers)):
                    assert numbers[j] == numbers[j - 1] + 1, (
                        f"practice-test-{i:02d}.md: question {numbers[j]} "
                        f"follows {numbers[j-1]} (expected {numbers[j-1]+1})"
                    )


class TestSessionContent:
    """Verify study session files."""

    def test_all_16_sessions_exist(self):
        files = os.listdir(SESSIONS_DIR)
        md_files = [f for f in files if f.endswith(".md")]
        assert len(md_files) >= 16, f"Expected 16 sessions, found {len(md_files)}"

    def test_session_files_are_non_empty(self):
        for filename in os.listdir(SESSIONS_DIR):
            if filename.endswith(".md"):
                path = os.path.join(SESSIONS_DIR, filename)
                size = os.path.getsize(path)
                assert size > 100, f"Session {filename} is suspiciously short ({size} bytes)"

    def test_session_files_have_headings(self):
        for filename in os.listdir(SESSIONS_DIR):
            if filename.endswith(".md"):
                path = os.path.join(SESSIONS_DIR, filename)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                assert "#" in content, f"Session {filename} has no headings"


class TestIndexHtml:
    """Verify the main index.html file."""

    def _read_index(self):
        path = os.path.join(BASE_DIR, "index.html")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def test_index_is_valid_html(self):
        content = self._read_index()
        assert "<!DOCTYPE html>" in content or "<!doctype html>" in content.lower()
        assert "<html" in content
        assert "</html>" in content

    def test_index_has_title(self):
        content = self._read_index()
        assert "<title>" in content
        assert "NMLS" in content or "MLO" in content or "Exam" in content

    def test_index_has_meta_charset(self):
        content = self._read_index()
        assert 'charset="UTF-8"' in content or "charset=UTF-8" in content
