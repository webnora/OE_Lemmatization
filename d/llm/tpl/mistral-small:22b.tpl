{{- if .Messages }}
{{- range $index, $_ := .Messages }}
{{- if eq .Role "user" }}
{{- if and (le (len (slice $.Messages $index)) 2) $.Tools }}[AVAILABLE_TOOLS] {{ $.Tools }}[/AVAILABLE_TOOLS]
{{- end }} [INST] {{ if and $.System (eq (len (slice $.Messages $index)) 1) }}{{ $.System }}

{{ end }}{{ .Content }} [/INST]
{{- else if eq .Role "assistant" }}
{{- if .Content }} {{ .Content }}
{{- if not (eq (len (slice $.Messages $index)) 1) }}</s>
{{- end }}
{{- else if .ToolCalls }}[TOOL_CALLS] [
{{- range .ToolCalls }}{"name": "{{ .Function.Name }}", "arguments": {{ .Function.Arguments }}}
{{- end }}]</s>
{{- end }}
{{- else if eq .Role "tool" }}[TOOL_RESULTS] {"content": {{ .Content }}}[/TOOL_RESULTS]
{{- end }}
{{- end }}
{{- else }} [INST] {{ if .System }}{{ .System }}

{{ end }}{{ .Prompt }} [/INST]
{{- end }}
{{- if .Response }} {{ end }}{{ .Response }}
{{- if .Response }}</s> {{ end }}