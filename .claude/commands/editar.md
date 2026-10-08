---
description: Editar un proyecto de video de principio a fin (ej. /editar acme/ad-verano "hook más agresivo, 9:16 y 16:9")
argument-hint: <cliente>/<proyecto> [indicaciones]
---
Editá el proyecto `$ARGUMENTS` de principio a fin como editor senior.

1. Cargá la skill `editor-pro` y seguí todas sus fases (intake → análisis → cortes por guion → plan →
   assets → montaje con revisión de stills/draft → render final → QC → entrega).
2. Las indicaciones extra que vengan después de la ruta tienen prioridad sobre los defaults del playbook.
3. Al final: commit + push de entregables y archivos de trabajo versionados, y un resumen corto.
