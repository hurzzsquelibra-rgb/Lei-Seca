"""
Tests for Lei-Seca.

These tests exercise the components that do NOT require an OpenAI API key:
- html_generator.build_html
- agent.LeiSecaAgent._detect_norm
- agent.LeiSecaAgent._make_filename
- agent.LeiSecaAgent.process (with mocked LLM)
- prompts.SYSTEM_PROMPT content
"""

from __future__ import annotations

import re
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Ensure src is importable
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).parent.parent))


# ===========================================================================
# html_generator
# ===========================================================================

class TestBuildHtml:
    def test_returns_valid_html_doctype(self):
        from src.html_generator import build_html

        result = build_html("Teste", "<p>conteúdo</p>")
        assert result.startswith("<!DOCTYPE html>")

    def test_title_in_head(self):
        from src.html_generator import build_html

        result = build_html("Lei nº 8.666/1993", "<p>body</p>")
        assert "Lei nº 8.666/1993 — Lei-Seca" in result

    def test_body_fragment_included(self):
        from src.html_generator import build_html

        body = "<section><h1>Olá</h1></section>"
        result = build_html("X", body)
        assert body in result

    def test_google_fonts_link_present(self):
        from src.html_generator import build_html

        result = build_html("X", "")
        assert "fonts.googleapis.com" in result

    def test_base_css_included(self):
        from src.html_generator import build_html

        result = build_html("X", "")
        assert ".cover" in result
        assert ".callout" in result
        assert ".badge-prazo" in result

    def test_palette_override_injected(self):
        from src.html_generator import build_html

        palette = "  :root { --color-primary: #2a6a3a; }"
        result = build_html("X", "", palette=palette)
        assert "#2a6a3a" in result

    def test_palette_omitted_when_empty(self):
        from src.html_generator import build_html

        result = build_html("X", "", palette="")
        # Should not have a second <style> block
        assert result.count("<style>") == 1

    def test_html_lang_pt_br(self):
        from src.html_generator import build_html

        result = build_html("X", "")
        assert 'lang="pt-BR"' in result

    def test_css_variables_present(self):
        from src.html_generator import build_html

        result = build_html("X", "")
        assert "--color-primary" in result
        assert "--font-body" in result
        assert "--font-mono" in result

    def test_responsive_breakpoint_present(self):
        from src.html_generator import build_html

        result = build_html("X", "")
        assert "680px" in result

    def test_print_media_query_present(self):
        from src.html_generator import build_html

        result = build_html("X", "")
        assert "@media print" in result
        assert "print-color-adjust" in result


# ===========================================================================
# agent — static helpers (no API key needed)
# ===========================================================================

class TestDetectNorm:
    def _detect(self, text: str) -> str:
        from src.agent import LeiSecaAgent
        return LeiSecaAgent._detect_norm(text)

    def test_detects_lei(self):
        assert "8.666" in self._detect("Lei nº 8.666/1993 — Licitações")

    def test_detects_decreto(self):
        assert "9.580" in self._detect("Decreto nº 9.580/2018, que regulamenta...")

    def test_detects_resolucao(self):
        result = self._detect("Resolução nº 23/2021 do TSE")
        assert "23" in result

    def test_detects_instrucao_normativa(self):
        result = self._detect("Instrução Normativa nº 5/2017")
        assert "5" in result

    def test_detects_portaria(self):
        result = self._detect("Portaria nº 1.234/2020 do Ministério")
        assert "1.234" in result

    def test_returns_empty_string_when_no_match(self):
        assert self._detect("Sem identificador aqui.") == ""

    def test_only_scans_first_400_chars(self):
        # Identifier after 400 chars should NOT be detected
        padding = "x" * 400
        text = padding + " Lei nº 1.000/2000"
        assert self._detect(text) == ""


class TestMakeFilename:
    def _make(self, norm: str) -> str:
        from src.agent import LeiSecaAgent
        return LeiSecaAgent._make_filename(norm)

    def test_slug_from_lei(self):
        name = self._make("Lei nº 8.666/1993")
        assert name.startswith("lei-n-8-666-1993") or "8" in name
        assert name.endswith(".html")

    def test_fallback_when_empty(self):
        name = self._make("")
        assert name.startswith("material-")
        assert name.endswith(".html")

    def test_no_spaces_in_filename(self):
        name = self._make("Lei Complementar nº 101/2000")
        assert " " not in name

    def test_no_special_chars(self):
        name = self._make("Lei nº 8.666/1993")
        # Only alphanumeric, hyphen, dot allowed
        assert re.match(r"^[a-z0-9\-\.]+$", name)

    def test_date_stamp_appended(self):
        name = self._make("Decreto nº 9.580/2018")
        # Expect 8-digit date stamp near end
        assert re.search(r"\d{8}\.html$", name)


# ===========================================================================
# agent — process() with mocked LLM
# ===========================================================================

class TestAgentProcess:
    """Test LeiSecaAgent.process using a mock LLM client."""

    _FAKE_BODY = (
        '<section class="cover"><span class="norm-badge">Lei nº 8.666/1993</span>'
        "<h1>Licitações e Contratos</h1></section>"
    )

    def _make_mock_client(self):
        """Return a mock OpenAI client whose completions return _FAKE_BODY."""
        choice = MagicMock()
        choice.message.content = self._FAKE_BODY
        completion = MagicMock()
        completion.choices = [choice]
        client = MagicMock()
        client.chat.completions.create.return_value = completion
        return client

    def test_process_saves_html_file(self, tmp_path):
        from src.agent import LeiSecaAgent

        agent = LeiSecaAgent(output_dir=str(tmp_path))
        agent._client = self._make_mock_client()

        path = agent.process(
            document="Lei nº 8.666/1993 — texto...",
            norm_identifier="Lei nº 8.666/1993",
        )

        assert path.exists()
        assert path.suffix == ".html"

    def test_output_contains_full_html_shell(self, tmp_path):
        from src.agent import LeiSecaAgent

        agent = LeiSecaAgent(output_dir=str(tmp_path))
        agent._client = self._make_mock_client()

        path = agent.process(
            document="Lei nº 8.666/1993 — texto...",
            norm_identifier="Lei nº 8.666/1993",
        )
        content = path.read_text(encoding="utf-8")

        assert "<!DOCTYPE html>" in content
        assert '<html lang="pt-BR">' in content
        assert self._FAKE_BODY in content

    def test_llm_code_fence_stripped(self, tmp_path):
        """LLM sometimes wraps output in ```html ... ``` — must be stripped."""
        from src.agent import LeiSecaAgent

        choice = MagicMock()
        choice.message.content = "```html\n" + self._FAKE_BODY + "\n```"
        completion = MagicMock()
        completion.choices = [choice]
        client = MagicMock()
        client.chat.completions.create.return_value = completion

        agent = LeiSecaAgent(output_dir=str(tmp_path))
        agent._client = client

        path = agent.process(document="Lei nº 8.666/1993", norm_identifier="Lei nº 8.666/1993")
        content = path.read_text(encoding="utf-8")

        assert "```" not in content

    def test_norm_auto_detected_when_not_provided(self, tmp_path):
        from src.agent import LeiSecaAgent

        agent = LeiSecaAgent(output_dir=str(tmp_path))
        agent._client = self._make_mock_client()

        path = agent.process(document="Lei nº 14.133/2021, nova lei de licitações...")
        # File should mention 14 (from "14.133") in filename
        assert "14" in path.name

    def test_raises_without_openai_client(self, tmp_path):
        from src.agent import LeiSecaAgent

        agent = LeiSecaAgent(output_dir=str(tmp_path))
        agent._client = None  # simulate missing openai package

        with pytest.raises(RuntimeError, match="openai"):
            agent.process(document="qualquer texto")


# ===========================================================================
# prompts — sanity checks
# ===========================================================================

class TestSystemPrompt:
    def test_prompt_not_empty(self):
        from src.prompts import SYSTEM_PROMPT
        assert len(SYSTEM_PROMPT.strip()) > 500

    def test_four_stages_mentioned(self):
        from src.prompts import SYSTEM_PROMPT
        for stage in ["ETAPA 1", "ETAPA 2", "ETAPA 3", "ETAPA 4"]:
            assert stage in SYSTEM_PROMPT

    def test_trap_patterns_mentioned(self):
        from src.prompts import SYSTEM_PROMPT
        for trap in ["Troca de modalidade", "Adulteração de prazo",
                     "Troca de agente", "Supressão de condição"]:
            assert trap in SYSTEM_PROMPT

    def test_visual_element_criteria_present(self):
        from src.prompts import SYSTEM_PROMPT
        for criterion in ["Tabela de prazos", "Fluxo procedimental",
                          "Cards comparativos"]:
            assert criterion in SYSTEM_PROMPT

    def test_html_format_directives_present(self):
        from src.prompts import SYSTEM_PROMPT
        assert "Google Fonts" in SYSTEM_PROMPT
        assert "Lora" in SYSTEM_PROMPT
        assert "DM Sans" in SYSTEM_PROMPT

    def test_output_dir_mentioned(self):
        from src.prompts import SYSTEM_PROMPT
        assert "/mnt/user-data/outputs" in SYSTEM_PROMPT

    def test_callout_types_mentioned(self):
        from src.prompts import SYSTEM_PROMPT
        for colour in ["Azul", "Verde", "Amarelo", "Vermelho"]:
            assert colour in SYSTEM_PROMPT
