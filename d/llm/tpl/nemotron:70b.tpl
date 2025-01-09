<|start_header_id|>system<|end_header_id|>

{{ if .Tools }}You have access to the following functions. To call a function, please respond with JSON for a function call. Respond in the format {"name": function name, "parameters": dictionary of argument name and its value}. Do not use variables.

{{ range .Tools }}{{ . }}

{{ end }}
{{- end }}{{ .System }}<|eot_id|>
{{- range $i, $_ := .Messages }}
{{- $isLastMessage := eq (len (slice $.Messages $i)) 1 -}}
{{- if eq .Role "system" }}
{{- else if eq .Role "assistant" }}<|start_header_id|>assistant<|end_header_id|>

{{ if .Content }}{{ .Content }}
{{- else if .ToolCalls }}
{{- range .ToolCalls }}{"name": "{{ .Function.Name }}", "parameters": {{ .Function.Arguments }} }
{{- end }}
{{- end }}
{{- if not $isLastMessage }}<|eot_id|>
{{- end }}
{{- else if eq .Role "tool" }}<|start_header_id|>ipython<|end_header_id|>

{{ .Content }}<|eot_id|>
{{- if $isLastMessage }}<|start_header_id|>assistant<|end_header_id|>

{{ end }}
{{- else }}<|start_header_id|>{{ .Role }}<|end_header_id|>

{{ .Content }}<|eot_id|>
{{- if $isLastMessage }}<|start_header_id|>assistant<|end_header_id|>

{{ end }}
{{- end }}
{{- end }}