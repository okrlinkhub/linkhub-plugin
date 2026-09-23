#!/usr/bin/env python3
"""Generate matching Markdown and one-page A4 PDF Strategy Canvas artifacts."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import tempfile
import unicodedata
from datetime import date
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "linkhub-strategy-canvas/v1"
SOURCE_URL = "https://www.okrlinkhub.com/blog/strategy-canvas"
ALLOWED_DIRECTIONS = {"at_or_below", "at_or_above"}
RISK_COLORS = ("#CFF58A", "#A9D3F7", "#F36A82")


class CanvasValidationError(ValueError):
    """Report invalid or non-renderable Strategy Canvas input."""

    pass


def parse_args() -> argparse.Namespace:
    """Parse renderer command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Render a LinkHub Strategy Canvas from canonical JSON.",
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args()


def require_string(value: Any, path: str) -> str:
    """Return a trimmed non-empty string or identify the invalid field."""

    if not isinstance(value, str) or not value.strip():
        raise CanvasValidationError(f"{path} deve essere una stringa non vuota")
    return value.strip()


def require_number(value: Any, path: str) -> int | float:
    """Return a finite number or identify the invalid field."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CanvasValidationError(f"{path} deve essere numerico")
    if not math.isfinite(value):
        raise CanvasValidationError(f"{path} deve essere un numero finito")
    return value


def validate_payload(raw: Any) -> dict[str, Any]:
    """Validate and normalize the canonical Strategy Canvas payload."""

    if not isinstance(raw, dict):
        raise CanvasValidationError("Il payload deve essere un oggetto JSON")
    if raw.get("schemaVersion") != SCHEMA_VERSION:
        raise CanvasValidationError(
            f"schemaVersion deve essere esattamente {SCHEMA_VERSION}"
        )

    payload: dict[str, Any] = {
        "schemaVersion": SCHEMA_VERSION,
        "teamName": require_string(raw.get("teamName"), "teamName"),
        "objective": require_string(raw.get("objective"), "objective"),
    }

    key_results = raw.get("keyResults")
    if not isinstance(key_results, list) or not 1 <= len(key_results) <= 3:
        raise CanvasValidationError("keyResults deve contenere da 1 a 3 elementi")

    normalized_krs = []
    kr_refs: set[str] = set()
    lead_refs: list[str] = []
    for index, item in enumerate(key_results, start=1):
        if not isinstance(item, dict):
            raise CanvasValidationError(f"keyResults[{index - 1}] deve essere un oggetto")
        ref = require_string(item.get("ref"), f"keyResults[{index - 1}].ref")
        if ref in kr_refs:
            raise CanvasValidationError(f"Riferimento KR duplicato: {ref}")
        kr_refs.add(ref)
        due_date = require_string(
            item.get("dueDate"), f"keyResults[{index - 1}].dueDate"
        )
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", due_date):
            raise CanvasValidationError(
                f"keyResults[{index - 1}].dueDate deve usare YYYY-MM-DD"
            )
        try:
            parsed_due_date = date.fromisoformat(due_date)
        except ValueError as error:
            raise CanvasValidationError(
                f"keyResults[{index - 1}].dueDate deve usare YYYY-MM-DD"
            ) from error
        if parsed_due_date <= date.today():
            raise CanvasValidationError(
                f"keyResults[{index - 1}].dueDate deve essere futura"
            )
        is_lead = item.get("isLead")
        if not isinstance(is_lead, bool):
            raise CanvasValidationError(
                f"keyResults[{index - 1}].isLead deve essere booleano"
            )
        if is_lead:
            lead_refs.append(ref)
        normalized_krs.append(
            {
                "ref": ref,
                "indicatorName": require_string(
                    item.get("indicatorName"),
                    f"keyResults[{index - 1}].indicatorName",
                ),
                "unit": require_string(
                    item.get("unit"), f"keyResults[{index - 1}].unit"
                ),
                "targetValue": require_number(
                    item.get("targetValue"),
                    f"keyResults[{index - 1}].targetValue",
                ),
                "dueDate": due_date,
                "isLead": is_lead,
            }
        )
    if len(lead_refs) != 1:
        raise CanvasValidationError("Deve esistere esattamente un KR guida")
    lead_ref = lead_refs[0]
    payload["keyResults"] = normalized_krs

    risks = raw.get("risks")
    if not isinstance(risks, list) or len(risks) != 3:
        raise CanvasValidationError("risks deve contenere esattamente 3 elementi")
    normalized_risks = []
    risk_refs: set[str] = set()
    initiative_refs: set[str] = set()
    for risk_index, risk in enumerate(risks, start=1):
        if not isinstance(risk, dict):
            raise CanvasValidationError(f"risks[{risk_index - 1}] deve essere un oggetto")
        ref = require_string(risk.get("ref"), f"risks[{risk_index - 1}].ref")
        if ref in risk_refs:
            raise CanvasValidationError(f"Riferimento rischio duplicato: {ref}")
        risk_refs.add(ref)
        key_result_ref = require_string(
            risk.get("keyResultRef"), f"risks[{risk_index - 1}].keyResultRef"
        )
        if key_result_ref != lead_ref:
            raise CanvasValidationError(
                f"{ref} deve riferirsi al KR guida {lead_ref}, non a {key_result_ref}"
            )

        kpi = risk.get("kpi")
        normalized_kpi = None
        if kpi is not None:
            if not isinstance(kpi, dict):
                raise CanvasValidationError(
                    f"risks[{risk_index - 1}].kpi deve essere un oggetto o null"
                )
            direction = kpi.get("triggerDirection")
            if direction not in ALLOWED_DIRECTIONS:
                raise CanvasValidationError(
                    f"risks[{risk_index - 1}].kpi.triggerDirection non valido"
                )
            normalized_kpi = {
                "indicatorName": require_string(
                    kpi.get("indicatorName"),
                    f"risks[{risk_index - 1}].kpi.indicatorName",
                ),
                "unit": require_string(
                    kpi.get("unit"), f"risks[{risk_index - 1}].kpi.unit"
                ),
                "triggerDirection": direction,
                "triggerValue": require_number(
                    kpi.get("triggerValue"),
                    f"risks[{risk_index - 1}].kpi.triggerValue",
                ),
            }

        initiatives = risk.get("initiatives")
        if not isinstance(initiatives, list) or not 1 <= len(initiatives) <= 3:
            raise CanvasValidationError(
                f"{ref}.initiatives deve contenere da 1 a 3 elementi"
            )
        normalized_initiatives = []
        for initiative_index, initiative in enumerate(initiatives, start=1):
            if not isinstance(initiative, dict):
                raise CanvasValidationError(
                    f"{ref}.initiatives[{initiative_index - 1}] deve essere un oggetto"
                )
            initiative_ref = require_string(
                initiative.get("ref"),
                f"{ref}.initiatives[{initiative_index - 1}].ref",
            )
            if initiative_ref in initiative_refs:
                raise CanvasValidationError(
                    f"Riferimento iniziativa duplicato: {initiative_ref}"
                )
            initiative_refs.add(initiative_ref)
            normalized_initiatives.append(
                {
                    "ref": initiative_ref,
                    "description": require_string(
                        initiative.get("description"),
                        f"{ref}.initiatives[{initiative_index - 1}].description",
                    ),
                }
            )

        normalized_risks.append(
            {
                "ref": ref,
                "keyResultRef": key_result_ref,
                "description": require_string(
                    risk.get("description"),
                    f"risks[{risk_index - 1}].description",
                ),
                "kpi": normalized_kpi,
                "initiatives": normalized_initiatives,
            }
        )
    payload["risks"] = normalized_risks
    return payload


def slugify(value: str) -> str:
    """Convert a team name to the stable filename slug required by the contract."""

    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value.lower()).strip("-")
    return slug or "team"


def existing_canvas_team_name(markdown_path: Path) -> str:
    """Read the team identity from an existing canonical Markdown artifact."""

    try:
        markdown = markdown_path.read_text(encoding="utf-8")
    except OSError as error:
        raise CanvasValidationError(
            f"Impossibile verificare il Canvas esistente: {markdown_path}"
        ) from error

    matches = list(
        re.finditer(
            r"```json linkhub-strategy-canvas\s*\n(.*?)\n```",
            markdown,
            flags=re.DOTALL,
        )
    )
    if len(matches) != 1:
        raise CanvasValidationError(
            "Il Canvas esistente non contiene un unico blocco canonico "
            f"verificabile: {markdown_path}"
        )
    try:
        existing_payload = json.loads(matches[0].group(1))
    except json.JSONDecodeError as error:
        raise CanvasValidationError(
            f"I dati canonici del Canvas esistente non sono validi: {markdown_path}"
        ) from error
    return require_string(existing_payload.get("teamName"), "teamName esistente")


def assert_output_identity(
    team_name: str,
    markdown_path: Path,
    pdf_path: Path,
) -> None:
    """Prevent one team from overwriting artifacts belonging to another team."""

    if not markdown_path.exists():
        if pdf_path.exists():
            raise CanvasValidationError(
                "Esiste già un PDF senza Markdown canonico: rimuovilo o spostalo "
                "prima di esportare"
            )
        return

    existing_team_name = existing_canvas_team_name(markdown_path)
    if existing_team_name != team_name:
        raise CanvasValidationError(
            "Il nome del team collide con un Canvas esistente: "
            f"'{team_name}' e '{existing_team_name}' producono lo stesso team-slug"
        )


def format_value(value: int | float) -> str:
    """Format numeric values for Italian-facing artifacts."""

    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).replace(".", ",")


def format_date(iso_date: str) -> str:
    """Format an ISO date for the Italian-facing PDF."""

    parsed = date.fromisoformat(iso_date)
    return parsed.strftime("%d/%m/%Y")


def markdown_escape(value: Any) -> str:
    """Escape content inserted into Markdown tables."""

    return str(value).replace("|", "\\|").replace("\n", " ")


def make_markdown(payload: dict[str, Any]) -> str:
    """Render the readable handoff and its canonical JSON block."""

    lines = [
        f"# Strategy Canvas — {payload['teamName']}",
        "",
        f"**Team:** {payload['teamName']}",
        "",
        f"**Objective:** {payload['objective']}",
        "",
        "## Key Results",
        "",
        "| Ref | Indicatore | Unità | Target | Data | Ruolo |",
        "|---|---|---:|---:|---|---|",
    ]
    for kr in payload["keyResults"]:
        role = "KR guida" if kr["isLead"] else "Complementare"
        lines.append(
            "| {ref} | {indicator} | {unit} | {target} | {date} | {role} |".format(
                ref=markdown_escape(kr["ref"]),
                indicator=markdown_escape(kr["indicatorName"]),
                unit=markdown_escape(kr["unit"]),
                target=markdown_escape(format_value(kr["targetValue"])),
                date=markdown_escape(kr["dueDate"]),
                role=role,
            )
        )

    lines.extend(["", "## Rischi, KPI e iniziative", ""])
    for risk in payload["risks"]:
        lines.extend(
            [
                f"### {risk['ref']} — {risk['description']}",
                "",
                f"**KR collegato:** {risk['keyResultRef']} (KR guida)",
                "",
            ]
        )
        if risk["kpi"] is None:
            lines.extend(["**KPI di allerta:** non definito (opzionale)", ""])
        else:
            kpi = risk["kpi"]
            direction = (
                "a o sotto" if kpi["triggerDirection"] == "at_or_below" else "a o sopra"
            )
            lines.extend(
                [
                    "**KPI di allerta:** "
                    f"{kpi['indicatorName']} ({kpi['unit']}), soglia {direction} "
                    f"{format_value(kpi['triggerValue'])}",
                    "",
                ]
            )
        lines.append("**Iniziative:**")
        lines.append("")
        for initiative in risk["initiatives"]:
            lines.append(f"- **{initiative['ref']}** — {initiative['description']}")
        lines.append("")

    lines.extend(
        [
            "## Handoff per LinkHub",
            "",
            "Questo documento descrive i componenti approvati nel workshop, ma non "
            "attesta che siano già stati creati in LinkHub. Gli indicatori dei KR e "
            "gli eventuali KPI devono essere selezionati o creati in piattaforma; "
            "non sono presenti `indicatorId`. I KR complementari non ricevono rischi "
            "da questo Canvas. Pesi, priorità, assignee e cadenze saranno definiti "
            "contro lo stato reale del team nella successiva sessione operativa.",
            "",
            f"Fonte metodologica: {SOURCE_URL}",
            "",
            "## Dati canonici",
            "",
            "```json linkhub-strategy-canvas",
            json.dumps(payload, ensure_ascii=False, indent=2),
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def pdf_text(value: Any) -> str:
    """Normalize text to characters supported by the built-in PDF font."""

    return (
        str(value)
        .replace("–", "-")
        .replace("—", "-")
        .replace("‑", "-")
        .replace("\n", " ")
    )


def render_pdf(payload: dict[str, Any], output_path: Path) -> None:
    """Render one readable A4 landscape Strategy Canvas page."""

    try:
        from reportlab.lib.colors import HexColor, white
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.pdfbase.pdfmetrics import stringWidth
        from reportlab.pdfgen.canvas import Canvas
    except ImportError as error:
        raise RuntimeError(
            "ReportLab non disponibile: installa il pacchetto Python 'reportlab'"
        ) from error

    page_width, page_height = landscape(A4)
    margin = 22.0
    gap = 10.0
    inner_width = page_width - 2 * margin

    def wrap(text: Any, width: float, font: str, size: float) -> list[str]:
        words = pdf_text(text).split()
        if not words:
            return [""]
        lines: list[str] = []
        current = ""
        for word in words:
            if stringWidth(word, font, size) > width:
                raise CanvasValidationError(
                    f"Testo non impaginabile senza spezzare parole: {word}"
                )
            if not current:
                current = word
                continue
            candidate = f"{current} {word}"
            if stringWidth(candidate, font, size) <= width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines

    def draw_lines(
        canvas: Canvas,
        lines: list[str],
        x: float,
        y: float,
        font: str,
        size: float,
        leading: float,
        color: Any,
    ) -> float:
        canvas.setFont(font, size)
        canvas.setFillColor(color)
        for line in lines:
            canvas.drawString(x, y, line)
            y -= leading
        return y

    header_bottom = 402.0
    header_top = page_height - 51.0
    header_height = header_top - header_bottom
    objective_width = inner_width * 0.38
    kr_x = margin + objective_width + 14
    kr_width = inner_width - objective_width - 28

    objective_lines = wrap(payload["objective"], objective_width - 24, "Helvetica-Bold", 14)
    if len(objective_lines) * 17 > header_height - 48:
        raise CanvasValidationError(
            "Overflow PDF: accorciare objective prima dell'export"
        )
    if stringWidth(f"Team: {pdf_text(payload['teamName'])}", "Helvetica", 9.5) > inner_width * 0.42:
        raise CanvasValidationError(
            "Overflow PDF: accorciare il nome del team prima dell'export"
        )

    kr_render_data = []
    kr_height = 0.0
    for kr in payload["keyResults"]:
        label = f"{kr['ref']} - {'KR GUIDA' if kr['isLead'] else 'KR COMPLEMENTARE'}"
        value = (
            f"{kr['indicatorName']} ({kr['unit']}): "
            f"{format_value(kr['targetValue'])} entro {format_date(kr['dueDate'])}"
        )
        value_lines = wrap(value, kr_width - 8, "Helvetica", 9.2)
        block_height = 12 + len(value_lines) * 10.5 + 4
        kr_height += block_height
        kr_render_data.append((label, value_lines, block_height))
    if kr_height > header_height - 30:
        raise CanvasValidationError(
            "Overflow PDF: accorciare i nomi degli indicatori KR prima dell'export"
        )

    columns_top = header_bottom - 12
    columns_bottom = 28.0
    column_height = columns_top - columns_bottom
    column_width = (inner_width - 2 * gap) / 3
    risk_render_data = []
    overflow_fields = []
    for index, risk in enumerate(payload["risks"]):
        risk_lines = wrap(risk["description"], column_width - 20, "Helvetica-Bold", 10.5)
        risk_height = 27 + len(risk_lines) * 12 + 9

        if risk["kpi"] is None:
            kpi_lines = ["Nessun KPI di allerta definito (opzionale)"]
        else:
            kpi = risk["kpi"]
            symbol = "<=" if kpi["triggerDirection"] == "at_or_below" else ">="
            kpi_text = (
                f"{kpi['indicatorName']} ({kpi['unit']}) {symbol} "
                f"{format_value(kpi['triggerValue'])}"
            )
            kpi_lines = wrap(kpi_text, column_width - 26, "Helvetica", 9)
        kpi_height = 48 + len(kpi_lines) * 10.5

        initiative_blocks = []
        initiatives_height = 28.0
        for initiative in risk["initiatives"]:
            text = f"{initiative['ref']} - {initiative['description']}"
            lines = wrap(text, column_width - 24, "Helvetica", 9)
            block_height = len(lines) * 10.5 + 7
            initiatives_height += block_height
            initiative_blocks.append(lines)
        total_height = risk_height + kpi_height + initiatives_height
        if total_height > column_height:
            overflow_fields.append(risk["ref"])
        risk_render_data.append((risk_lines, kpi_lines, initiative_blocks))

    if overflow_fields:
        raise CanvasValidationError(
            "Overflow PDF: accorciare descrizioni/KPI/iniziative per "
            + ", ".join(overflow_fields)
        )

    canvas = Canvas(
        str(output_path),
        pagesize=(page_width, page_height),
        pageCompression=1,
        invariant=1,
    )
    canvas.setTitle(f"Strategy Canvas - {payload['teamName']}")
    canvas.setAuthor("LinkHub Strategy Canvas")

    canvas.setFillColor(HexColor("#111827"))
    canvas.setFont("Helvetica-Bold", 17)
    canvas.drawString(margin, page_height - 27, "LINKHUB STRATEGY CANVAS")
    canvas.setFont("Helvetica", 9.5)
    canvas.drawRightString(page_width - margin, page_height - 25, f"Team: {pdf_text(payload['teamName'])}")

    canvas.setFillColor(HexColor("#28C6CE"))
    canvas.roundRect(margin, header_bottom, inner_width, header_height, 7, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(margin + 12, header_top - 18, "OBJECTIVE")
    draw_lines(
        canvas,
        objective_lines,
        margin + 12,
        header_top - 40,
        "Helvetica-Bold",
        14,
        17,
        white,
    )
    canvas.setStrokeColor(HexColor("#FFFFFF"))
    canvas.setLineWidth(0.7)
    canvas.line(kr_x - 8, header_bottom + 12, kr_x - 8, header_top - 12)

    y = header_top - 18
    for label, value_lines, block_height in kr_render_data:
        canvas.setFont("Helvetica-Bold", 9)
        canvas.setFillColor(white)
        canvas.drawString(kr_x, y, label)
        y -= 12
        y = draw_lines(canvas, value_lines, kr_x, y, "Helvetica", 9.2, 10.5, white)
        y -= 4

    for index, risk in enumerate(payload["risks"]):
        x = margin + index * (column_width + gap)
        risk_lines, kpi_lines, initiative_blocks = risk_render_data[index]
        color = HexColor(RISK_COLORS[index])

        canvas.setFillColor(color)
        canvas.roundRect(x, columns_bottom, column_width, column_height, 6, fill=1, stroke=0)
        canvas.setFillColor(HexColor("#111827"))
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(x + 10, columns_top - 19, f"RISCHIO {index + 1} - {risk['ref']}")
        y = columns_top - 38
        y = draw_lines(
            canvas,
            risk_lines,
            x + 10,
            y,
            "Helvetica-Bold",
            10.5,
            12,
            HexColor("#111827"),
        )
        y -= 8

        kpi_box_height = 38 + len(kpi_lines) * 10.5
        canvas.setFillColor(HexColor("#F3F4F6"))
        canvas.roundRect(x + 8, y - kpi_box_height, column_width - 16, kpi_box_height, 4, fill=1, stroke=0)
        canvas.setFillColor(HexColor("#111827"))
        canvas.setFont("Helvetica-Bold", 9.5)
        canvas.drawString(x + 14, y - 15, "KPI DI ALLERTA")
        draw_lines(
            canvas,
            kpi_lines,
            x + 14,
            y - 30,
            "Helvetica",
            9,
            10.5,
            HexColor("#374151"),
        )
        y -= kpi_box_height + 12

        canvas.setFillColor(HexColor("#111827"))
        canvas.setFont("Helvetica-Bold", 9.5)
        canvas.drawString(x + 10, y, "INIZIATIVE")
        y -= 16
        for lines in initiative_blocks:
            y = draw_lines(
                canvas,
                lines,
                x + 12,
                y,
                "Helvetica",
                9,
                10.5,
                HexColor("#111827"),
            )
            y -= 7

    canvas.setFillColor(HexColor("#4B5563"))
    canvas.setFont("Helvetica", 6.7)
    canvas.drawString(margin, 12, f"Metodo LinkHub - {SOURCE_URL}")
    canvas.drawRightString(
        page_width - margin,
        12,
        "Handoff formativo: nessun record LinkHub creato",
    )
    canvas.showPage()
    canvas.save()


def write_outputs(payload: dict[str, Any], output_dir: Path) -> tuple[Path, Path]:
    """Generate matching Markdown and PDF artifacts without unsafe overwrites."""

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{slugify(payload['teamName'])}-strategy-canvas"
    markdown_path = output_dir / f"{stem}.md"
    pdf_path = output_dir / f"{stem}.pdf"
    assert_output_identity(payload["teamName"], markdown_path, pdf_path)
    markdown = make_markdown(payload)

    markdown_temp: Path | None = None
    pdf_temp: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=f".{stem}-",
            suffix=".md.tmp",
            dir=output_dir,
            delete=False,
        ) as stream:
            stream.write(markdown)
            markdown_temp = Path(stream.name)
        with tempfile.NamedTemporaryFile(
            prefix=f".{stem}-",
            suffix=".pdf.tmp",
            dir=output_dir,
            delete=False,
        ) as stream:
            pdf_temp = Path(stream.name)
        render_pdf(payload, pdf_temp)
        os.replace(markdown_temp, markdown_path)
        markdown_temp = None
        os.replace(pdf_temp, pdf_path)
        pdf_temp = None
    finally:
        for temporary in (markdown_temp, pdf_temp):
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    return markdown_path, pdf_path


def main() -> int:
    """Validate input, render both artifacts, and report their paths."""

    args = parse_args()
    try:
        with args.input.open(encoding="utf-8") as stream:
            raw = json.load(stream)
        payload = validate_payload(raw)
        markdown_path, pdf_path = write_outputs(payload, args.output_dir)
    except (OSError, json.JSONDecodeError, CanvasValidationError, RuntimeError) as error:
        print(f"Errore Strategy Canvas: {error}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "markdown": str(markdown_path.resolve()),
                "pdf": str(pdf_path.resolve()),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
