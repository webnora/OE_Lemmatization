{{- range $i, $_ := .Messages }}
{{- $last := eq (len (slice $.Messages $i)) 1 -}}
<|im_start|>{{ .Role }}
{{ .Content }}
{{- if not $last }}<|im_end|>
{{ else if ne .Role "assistant" }}<|im_end|>
<|im_start|>assistant
{{ end }}
{{- end }}