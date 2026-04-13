"""
Lei-Seca agent — creates theoretical study materials for Brazilian concursos.

The agent follows a strict 4-stage workflow:
  1. Analytical reading of the legal document
  2. Exam-trap mapping
  3. Thematic organisation
  4. HTML file production

It delegates the heavy reasoning to an LLM (OpenAI-compatible API) and wraps
the response in the full HTML shell from html_generator.py.
"""

from __future__ import annotations

import os
import re
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.html_generator import build_html
from src.prompts import SYSTEM_PROMPT

# ---------------------------------------------------------------------------
# Optional dependency: openai ≥ 1.0
# ---------------------------------------------------------------------------
try:
    from openai import OpenAI  # type: ignore[import]
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False


class LeiSecaAgent:
    """
    Agent that turns a legal document text into a styled HTML study file.

    Parameters
    ----------
    api_key   : OpenAI-compatible API key (falls back to OPENAI_API_KEY env var).
    model     : LLM model identifier (default: gpt-4o).
    base_url  : Optional base URL for non-OpenAI-compatible providers.
    output_dir: Directory where HTML files are saved.
                Defaults to ``/mnt/user-data/outputs`` (writable in prod) or
                ``./outputs`` (fallback for local dev).
    """

    DEFAULT_MODEL = "gpt-4o"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        output_dir: Optional[str] = None,
    ) -> None:
        self.model = model or os.getenv("LEISECA_MODEL", self.DEFAULT_MODEL)
        self.output_dir = Path(
            output_dir
            or os.getenv("LEISECA_OUTPUT_DIR", "/mnt/user-data/outputs")
        )

        # Resolve writable output dir
        if not self.output_dir.exists():
            try:
                self.output_dir.mkdir(parents=True, exist_ok=True)
            except OSError:
                self.output_dir = Path("outputs")
                self.output_dir.mkdir(parents=True, exist_ok=True)

        if _OPENAI_AVAILABLE:
            resolved_key = api_key or os.getenv("OPENAI_API_KEY", "")
            kwargs: dict = {"api_key": resolved_key}
            if base_url:
                kwargs["base_url"] = base_url
            self._client: Optional[OpenAI] = OpenAI(**kwargs)
        else:
            self._client = None

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def process(self, document: str, norm_identifier: str = "") -> Path:
        """
        Process a legal document and write the HTML study file.

        Parameters
        ----------
        document        : Full text of the legal norm.
        norm_identifier : Short label, e.g. ``"Lei nº 8.666/1993"``.
                          Inferred from document text when omitted.

        Returns
        -------
        Path to the saved HTML file.
        """
        norm_identifier = norm_identifier or self._detect_norm(document)
        html_body = self._call_llm(document, norm_identifier)
        title = norm_identifier or "Material Teórico"
        full_html = build_html(title=title, body=html_body)
        output_path = self._save(full_html, norm_identifier)
        return output_path

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _call_llm(self, document: str, norm_identifier: str) -> str:
        """
        Send the document to the LLM and return the raw HTML body fragment.
        Raises RuntimeError if the openai package is not installed.
        """
        if self._client is None:
            raise RuntimeError(
                "The 'openai' package is required. "
                "Install it with:  pip install openai"
            )

        user_message = (
            f"Norma: {norm_identifier}\n\n"
            "Texto integral da norma:\n\n"
            f"{document}"
        )

        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.2,
        )

        content: str = response.choices[0].message.content or ""
        # The LLM may wrap the body in ```html ... ``` — strip opening/closing fences.
        content = re.sub(r"\A```[a-z]*\n", "", content.strip())
        content = re.sub(r"\n```\Z", "", content.strip())
        return content

    @staticmethod
    def _detect_norm(text: str) -> str:
        """
        Attempt to extract a norm identifier from the first 400 chars of text.
        Falls back to an empty string.
        """
        patterns = [
            r"(Lei\s+(?:Complementar\s+)?n[oº°]?\s*[\d\./]+(?:/\d{4})?)",
            r"(Decreto(?:-[Ll]ei)?\s+n[oº°]?\s*[\d\./]+(?:/\d{4})?)",
            r"(Resolução\s+n[oº°]?\s*[\d\./]+(?:/\d{4})?)",
            r"(Instrução\s+Normativa\s+n[oº°]?\s*[\d\./]+(?:/\d{4})?)",
            r"(Portaria\s+n[oº°]?\s*[\d\./]+(?:/\d{4})?)",
        ]
        sample = text[:400]
        for pat in patterns:
            m = re.search(pat, sample, re.IGNORECASE)
            if m:
                return m.group(1).strip()
        return ""

    def _save(self, html: str, norm_identifier: str) -> Path:
        """Persist *html* to a file and return its path."""
        filename = self._make_filename(norm_identifier)
        path = self.output_dir / filename
        path.write_text(html, encoding="utf-8")
        return path

    @staticmethod
    def _make_filename(norm_identifier: str) -> str:
        """
        Build a filesystem-safe filename from the norm identifier.
        Example: ``"Lei nº 8.666/1993"`` → ``"lei-8666-1993-20260413.html"``
        """
        if not norm_identifier:
            stamp = datetime.now().strftime("%Y%m%d")
            return f"material-{stamp}.html"

        # Normalise unicode, lower-case, keep only alphanumerics and hyphens
        nfkd = unicodedata.normalize("NFKD", norm_identifier)
        ascii_str = nfkd.encode("ascii", "ignore").decode("ascii")
        slug = re.sub(r"[^a-z0-9]+", "-", ascii_str.lower()).strip("-")
        stamp = datetime.now().strftime("%Y%m%d")
        return f"{slug}-{stamp}.html"
