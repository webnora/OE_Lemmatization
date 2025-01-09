{{- if .Messages }}
{{- if or .System .Tools }}<|start_header_id|>system<|end_header_id|>

{{ if .System }}{{ .System }}
{{- end }}
In addition to plain text responses, you can chose to call one or more of the provided functions.

Use the following rule to decide when to call a function:
  * if the response can be generated from your internal knowledge (e.g., as in the case of queries like "What is the capital of Poland?"), do so
  * if you need external information that can be obtained by calling one or more of the provided functions, generate a function calls

If you decide to call functions:
  * prefix function calls with functools marker (no closing marker required)
  * all function calls should be generated in a single JSON list formatted as functools[{"name": [function name], "arguments": [function arguments as JSON]}, ...]
  * follow the provided JSON schema. Do not hallucinate arguments or values. Do to blindly copy values from the provided samples
  * respect the argument type formatting. E.g., if the type if number and format is float, write value 7 as 7.0
  * make sure you pick the right functions that match the user intent

Available functions as JSON spec:
{{- if .Tools }}
{{ .Tools }}
{{- end }}<|eot_id|>
{{- end }}
{{- range .Messages }}
{{- if ne .Role "system" }}<|start_header_id|>{{ .Role }}<|end_header_id|>
{{- if and .Content (eq .Role "tools") }}

{"result": {{ .Content }}}
{{- else if .Content }}

{{ .Content }}
{{- else if .ToolCalls }}

functools[
{{- range .ToolCalls }}{{ "{" }}"name": "{{ .Function.Name }}", "arguments": {{ .Function.Arguments }}{{ "}" }}
{{- end }}]
{{- end }}<|eot_id|>
{{- end }}
{{- end }}<|start_header_id|>assistant<|end_header_id|>

{{ else }}
{{- if .System }}<|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>

{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>

{{ end }}{{ .Response }}{{ if .Response }}<|eot_id|>{{ end }}