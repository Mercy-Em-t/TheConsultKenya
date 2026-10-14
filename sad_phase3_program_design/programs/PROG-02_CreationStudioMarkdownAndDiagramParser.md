# Program Specification: CreationStudioMarkdownAndDiagramParser
**Program ID:** `PROG-02` | **Module Type:** Processing & Transformation Engine
**Language / Framework:** `TypeScript / Node.js 20 & WebAssembly (Wasm)`

### Description
Parses modular case study Markdown text, lints and compiles Mermaid syntax blocks into clean vector SVG strings, strips malicious XSS tokens, and verifies code syntax highlighting.

### Systems Design Characteristics
- **Cohesion Type:** Functional Cohesion (Transforms structured markup into sanitized SVG & HTML trees)
- **Coupling Level:** Data Coupling & Stamp Coupling (Accepts RawDraftDTO; returns CompiledCaseStudyDTO)
- **Fan-In:** `3` (High reuse by upstream callers)
- **Fan-Out:** `2` (Optimal controlled subordinate delegations)

### Associated Events & Triggers
- `EVT-STUDIO-KEYSTROKE: User types in Markdown split-screen editor.`
- `EVT-STUDIO-SAVE: User clicks save or 30-second background auto-save fires.`

### Program Input Parameters
| Input Parameter | Data Transfer Object (DTO) | Internal Elements |
| :--- | :--- | :--- |
| **`raw_draft`** | `RawDraftDTO` | case_study_id, markdown_content, template_id |

### Program Output Returns
| Output Return | Data Transfer Object (DTO) | Internal Elements |
| :--- | :--- | :--- |
| **`compiled_view`** | `CompiledViewDTO` | sanitized_html, svg_diagram_nodes, lint_errors_list |

### Detailed Algorithmic Pseudocode
```python
FUNCTION CompileCaseStudyDeck(raw_markdown: String) -> CompiledView:
    INPUT: raw_markdown
    OUTPUT: CompiledView (sanitized_html, svg_nodes, lint_errors)

    lint_errors = []
    svg_nodes = []

    // 1. Extract and Validate Mermaid Code Blocks
    diagram_blocks = RegexExtract(raw_markdown, /```mermaid([\s\S]*?)```/g)
    FOR EACH block IN diagram_blocks:
        TRY
            parsed_ast = MermaidParser.ParseSyntax(block.content)
            svg_string = MermaidRenderer.RenderToSVG(parsed_ast)
            svg_nodes.Append(ID=block.id, svg=svg_string)
        CATCH SyntaxError AS err:
            lint_errors.Append(Line=block.line_number, Message=err.message, Suggestion=err.fix_hint)
            // Render error placeholder box
            svg_nodes.Append(ID=block.id, svg=GenerateErrorPlaceholderSVG(err))
        END TRY
    END FOR

    // 2. Sanitize HTML & Prevent XSS Attacks
    sanitized_html = DOMPurify.Sanitize(MarkdownParser.ToHTML(raw_markdown), AllowedTags=["h1","h2","h3","p","code","pre","div","span"])

    // 3. Extract Meta Metrics (Dwell weights, readability score)
    word_count = CountWords(sanitized_html)
    estimated_read_time_seconds = word_count / 3.5

    RETURN CompiledView(
        html=sanitized_html,
        diagrams=svg_nodes,
        errors=lint_errors,
        read_time=estimated_read_time_seconds
    )
END FUNCTION
```
