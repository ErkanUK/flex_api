#!/usr/bin/env bash
set -e

OUT="docs/maps/docs-structure.puml"

echo "@startuml" > "$OUT"
echo "title Documentation Structure Map" >> "$OUT"

echo "package \"docs/\" {" >> "$OUT"
tree docs -L 2 | sed '1d' | sed 's/^/  /' | sed 's/.*/  [ & ]/' >> "$OUT"
echo "}" >> "$OUT"

echo "@enduml" >> "$OUT"

echo "Generated $OUT"