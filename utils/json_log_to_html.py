import json
import html


def json_log_to_html(json_log_entries):
    """
    Convert JSON test logs into a visually appealing HTML report
    with color-coded status indicators
    """
    html_output = _get_docuement_style()
    html_output += _get_document_body(json_log_entries)

    print(html)
    return html_output


def _get_docuement_style():
    """
    Get the style sheet for the document.
    """
    html_output = """
        <style>
            :root {
                --pass-color: #4CAF50;
                --fail-color: #F44336;
                --info-color: #2196F3;
                --warning-color: #FFC107;
                --card-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f7fa;
            }

            .test-case {
                background: white;
                border-radius: 8px;
                margin-bottom: 20px;
                overflow: hidden;
                box-shadow: var(--card-shadow);
                border-left: 4px solid var(--pass-color);
            }

            .test-case.failed {
                border-left-color: var(--fail-color);
            }

            .test-header {
                padding: 15px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                background-color: #f9f9f9;
                border-bottom: 1px solid #eee;
            }

            .test-id {
                font-weight: bold;
                font-size: 1.1rem;
            }

            .status-badge {
                padding: 5px 12px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 0.85rem;
                text-transform: uppercase;
            }

            .status-pass { background-color: var(--pass-color); color: white; }
            .status-fail { background-color: var(--fail-color); color: white; }

            .test-content {
                padding: 0 20px;
                max-height: 2000px;
                overflow: hidden;
                transition: max-height 0.3s ease, padding 0.3s ease;
            }

            .metadata-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 6px;
            }

            .metadata-item strong {
                display: block;
                color: #666;
                font-size: 0.85rem;
                margin-bottom: 5px;
            }

            .steps-table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }

            .steps-table th, .steps-table td {
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #eee;
            }

            .steps-table th {
                background-color: #f1f8ff;
                font-weight: 600;
            }

            .error-section {
                background-color: #fff8f8;
                border-left: 4px solid var(--fail-color);
                padding: 15px;
                border-radius: 0 6px 6px 0;
                margin-top: 20px;
                font-family: monospace;
                white-space: pre-wrap;
                overflow-x: auto;
            }

            .env-tag {
                display: inline-block;
                background: #e0f7fa;
                color: #006064;
                padding: 3px 8px;
                border-radius: 4px;
                font-size: 0.8rem;
                margin-right: 5px;
            }
        </style>"""
    return html_output


def _get_document_body(json_log_entries):
    """
    Get the html body from the log entries in JSON format.
    """
    test_case_html = ""
    for json_log_entry in json_log_entries:
        test_case_html += _add_test_case(json_log_entry)

    html_output = f"""
        <body>
        {test_case_html}
        </body>"""

    return html_output


def _add_test_case(json_log_entry):
    """
    Add all the test cases to the body of the html.
    """
    log_entry = json.loads(json_log_entry)

    status = log_entry.get("status", "undefined")
    test_header_html = _get_test_header_html(log_entry)
    metadata_html = _get_metadata_html(log_entry)
    steps_html = _get_steps_html(log_entry)
    error_html = _get_error_html(log_entry)

    html_output = f"""
    <div class="test-case {'failed' if status == "FAIL" else ""}">
        {test_header_html}
        <div class="test-content">
            {metadata_html}
            {steps_html}
            {error_html}
        </div>
    </div>"""
    return html_output


def _get_test_header_html(log_entry):
    """
    Add a header to a test case.
    """
    status = log_entry.get("status", "undefined")
    test_id = log_entry.get("test_id", "")
    description = log_entry.get('description', '')

    html_output = f"""
    <div class="test-header">
            <div>
                <div class="test-id">{html.escape(test_id)}</div>
                <div>
                    <strong>Description: </strong>{html.escape(description)}
                </div>
            </div>
            <div class="status-badge
            {'status-pass' if status == 'PASS' else 'status-fail'}">
                {status}
            </div>
        </div>"""
    return html_output


def _get_metadata_html(log_entry):
    """
    Add Metadata to a test case.
    """
    metadata = log_entry.get("metadata", {})
    run_id = html.escape(metadata.get('run_id', ''))
    severity = html.escape(metadata.get('severity', ''))
    owner = html.escape(metadata.get('owner', ''))
    env_tags = ""
    for tag in metadata.get('env', []):
        env_tags += f"<span class='env-tag'>{html.escape(tag)}</span>"

    metadata_html = f"""
    <div class="metadata-grid">
        <div class="metadata-item">
            <strong>Run ID</strong>
            {run_id}
        </div>
        <div class="metadata-item">
            <strong>Severity</strong>
            {severity}
        </div>
        <div class="metadata-item">
            <strong>Owner</strong>
            {owner}
        </div>
        <div class="metadata-item">
            <strong>Environment</strong>
            {env_tags}
        </div>
    </div>"""
    return metadata_html


def _get_steps_html(log_entry):
    """
    Add executed steps to a test case.
    """
    steps_html = """
    <h3>Execution Steps</h3>
    <table class="steps-table">
        <thead>
            <tr>
                <th>Step #</th>
                <th>Description</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>"""

    for step_num, step_data in log_entry.get("steps", {}).items():
        step_desc = html.escape(step_data.get("descrpition", ''))
        step_state = html.escape(step_data.get("state", ''))
        if step_state.lower() == "finished":
            state_class = "status-pass"
        else:
            state_class = "status-fail"

        steps_html += f"""
        <tr>
            <td>{html.escape(step_num)}</td>
            <td>{step_desc}</td>
            <td><span class="{state_class}">{step_state}</span></td>
        </tr>"""

    steps_html += "</tbody></table>"
    return steps_html


def _get_error_html(log_entry):
    """
    Add error info to a test case.
    """
    status = log_entry.get("status", "undefined")

    error_html = ""
    if status == "FAIL" and "error" in log_entry:
        error = log_entry["error"]
        error_msg = "<strong>Error Message:</strong>" \
            f"\n{html.escape(error.get('message', ''))}"
        stacktrace = "<strong>Stack Trace:</strong>" \
            f"<pre>{html.escape("\n".join(error.get("stacktrace", [])))}</pre>"

        error_html = f"""
        <div class="error-section">{error_msg}
        <hr>{stacktrace}
        </div>"""
    
    return error_html
