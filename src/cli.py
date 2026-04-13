"""
Lei-Seca CLI — command-line entry point.

Usage
-----
  python -m src.cli <document_file> [--norm "Lei nº 8.666/1993"] [--model gpt-4o]

The document file can be plain text (.txt) or a PDF (.pdf — requires pdfminer.six).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _read_document(filepath: str) -> str:
    """Read document text from a .txt or .pdf file."""
    path = Path(filepath)
    if not path.exists():
        print(f"[erro] Arquivo não encontrado: {filepath}", file=sys.stderr)
        sys.exit(1)

    if path.suffix.lower() == ".pdf":
        try:
            from pdfminer.high_level import extract_text  # type: ignore[import]
        except ImportError:
            print(
                "[erro] Para processar PDFs instale pdfminer.six:  pip install pdfminer.six",
                file=sys.stderr,
            )
            sys.exit(1)
        return extract_text(str(path))

    return path.read_text(encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="leiseca",
        description="Gera material teórico doutrinário em HTML a partir de uma norma jurídica.",
    )
    parser.add_argument(
        "document",
        help="Caminho para o arquivo de texto (.txt) ou PDF (.pdf) da norma.",
    )
    parser.add_argument(
        "--norm",
        metavar="IDENTIFICADOR",
        default="",
        help=(
            "Identificador curto da norma, ex.: 'Lei nº 8.666/1993'. "
            "Quando omitido, é detectado automaticamente."
        ),
    )
    parser.add_argument(
        "--model",
        default="",
        help="Modelo LLM a usar (padrão: gpt-4o ou LEISECA_MODEL env var).",
    )
    parser.add_argument(
        "--output-dir",
        metavar="DIR",
        default="",
        help=(
            "Diretório de saída. "
            "Padrão: /mnt/user-data/outputs (ou ./outputs em desenvolvimento)."
        ),
    )
    parser.add_argument(
        "--api-key",
        metavar="KEY",
        default="",
        help="Chave de API OpenAI (ou use a variável de ambiente OPENAI_API_KEY).",
    )

    args = parser.parse_args(argv)

    # Lazy import so tests can import cli without openai installed
    from src.agent import LeiSecaAgent

    agent = LeiSecaAgent(
        api_key=args.api_key or None,
        model=args.model or None,
        output_dir=args.output_dir or None,
    )

    document_text = _read_document(args.document)
    norm = args.norm

    print(f"[lei-seca] Processando: {args.document}")
    if norm:
        print(f"[lei-seca] Norma identificada manualmente: {norm}")

    output_path = agent.process(document=document_text, norm_identifier=norm)

    print(f"[lei-seca] Material salvo em: {output_path}")


if __name__ == "__main__":
    main()
