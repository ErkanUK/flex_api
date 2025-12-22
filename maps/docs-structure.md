```mermaid
graph TD
  docs --> diagrams
  docs --> maps
  docs --> api

  diagrams --> test_puml[test.puml]
  diagrams --> readme[README.md]