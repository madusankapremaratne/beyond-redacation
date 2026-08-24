"""Beyond Redaction — core relation-aware semantic generalization framework.

This package is the real implementation of the `/framework` component the README
describes: entity extraction, relation extraction, and consistent-placeholder
generalization, designed to run against local (on-device) Ollama models.

Built 2026-08-23 following the item-5 decision (see .madus/plans/Item5-Findings-N50.md):
the N=50 evaluation of the holistic single-prompt rewrite showed it has no
representation of the entity-relation structure it is meant to break (mean SER 0.393,
no fully-suppressed samples, ~11% residual name-leak rate). This package replaces the
rewrite-and-hope approach with an explicit extract -> map -> substitute pipeline.
"""

from .extraction import extract_entities, extract_relations
from .generalization import build_mapping, generalize

__all__ = ["extract_entities", "extract_relations", "build_mapping", "generalize"]
