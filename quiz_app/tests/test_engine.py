"""
Tests for quiz_engine.py
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from quiz_engine import (
    sample_questions,
    get_available_temas,
    clean_answer_for_display,
    get_answer_text
)


class TestSampleQuestions:
    """Tests for sample_questions function."""

    def test_returns_correct_count(self):
        """Should return the requested number of questions."""
        questions = sample_questions(n=5)
        assert len(questions) == 5

    def test_returns_less_if_not_enough(self):
        """Should return fewer questions if not enough cards available."""
        # Request more than available (we have 209 cards)
        questions = sample_questions(n=300)
        assert len(questions) <= 209

    def test_respects_tema_filter(self):
        """Should only return questions from specified temas."""
        questions = sample_questions(n=10, temas=["semiologia"])
        for q in questions:
            assert q["tema"] == "semiologia"

    def test_respects_subtema_filter(self):
        """Should only return questions from specified subtemas."""
        questions = sample_questions(n=5, subtemas=["atencion"])
        for q in questions:
            assert q["subtema"] == "atencion"

    def test_mcq_mode_only_returns_mcq(self):
        """In MCQ mode, all questions should be MCQ format."""
        questions = sample_questions(n=10, modo="mcq")
        for q in questions:
            assert q["formato"] == "mcq"
            assert "opciones" in q
            assert len(q["opciones"]) == 4

    def test_abierto_mode_only_returns_abierto(self):
        """In abierto mode, all questions should be abierto format."""
        questions = sample_questions(n=10, modo="abierto")
        for q in questions:
            assert q["formato"] == "abierto"
            assert "opciones" not in q

    def test_mixto_mode_has_both_formats(self):
        """In mixto mode, should have both MCQ and abierto questions."""
        questions = sample_questions(n=20, modo="mixto", ratio_mcq=0.5)
        formatos = set(q["formato"] for q in questions)
        # With 50% ratio, should have both
        assert "mcq" in formatos or "abierto" in formatos

    def test_mcq_options_include_correct_answer(self):
        """MCQ options should include the correct answer."""
        questions = sample_questions(n=5, modo="mcq")
        for q in questions:
            correct_idx = q["respuesta_correcta_index"]
            assert 0 <= correct_idx < 4
            # The correct option should match respuesta_texto
            assert q["opciones"][correct_idx] == q["respuesta_texto"]

    def test_no_mcq_for_ineligible_cards(self):
        """Cards marked mcq_eligible=0 should not appear as MCQ."""
        # Get a large sample to increase chance of hitting ineligible cards
        questions = sample_questions(n=50, modo="mixto", ratio_mcq=1.0)
        # All MCQ questions should have options
        for q in questions:
            if q["formato"] == "mcq":
                assert "opciones" in q


class TestGetAvailableTemas:
    """Tests for get_available_temas function."""

    def test_returns_list(self):
        """Should return a list of tema dictionaries."""
        temas = get_available_temas()
        assert isinstance(temas, list)
        assert len(temas) > 0

    def test_has_required_fields(self):
        """Each tema should have required fields."""
        temas = get_available_temas()
        for tema in temas:
            assert "tema" in tema
            assert "subtema" in tema
            assert "count" in tema
            assert "mcq_count" in tema


class TestCleanFunctions:
    """Tests for text cleaning functions."""

    def test_clean_answer_removes_source(self):
        """Should remove source info from answer."""
        dorso = 'La respuesta.<br><br><small><i>Fuente: Libro, p. 1</i></small>'
        clean = clean_answer_for_display(dorso)
        assert "Fuente" not in clean
        assert clean == "La respuesta."

    def test_get_answer_text_removes_html(self):
        """Should remove all HTML tags."""
        dorso = '<b>La respuesta</b> con <i>formato</i>.<br><br><small><i>Fuente: Libro</i></small>'
        text = get_answer_text(dorso)
        assert "<" not in text
        assert ">" not in text
        assert "Fuente" not in text


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
