"""
CLAUDE.md generator using Jinja2 templates.

Combines static analysis results with LLM-enhanced descriptions
to generate folder-level CLAUDE.md files.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .core.scanner import FileScanner, ScannedFolder, ScannedFile
from .core.extractor import SymbolExtractor, FileSymbols
from .core.analyzer import DependencyAnalyzer
from .executions.llm_client import BaseLLMClient, LLMClient
from .executions.executors import FolderSummarizer, FileDescriber, DependencyInferrer
from .metadata import (
    FrontmatterBuilder,
    KeywordExtractor,
    IntentClassifier,
    SearchMetadataBuilder,
)
from .retrieval import HybridSearchStrategy, RankingWeights
from .protocols import LayerProtocolManager, MultiLayerOutput

logger = logging.getLogger(__name__)


@dataclass
class FileEntry:
    """File entry for template rendering."""
    name: str
    symbols: str
    tokens: int
    description: str
    frontmatter: str = ""
    keywords: list[str] = field(default_factory=list)
    chunk_type: str = ""
    when_to_load: list[str] = field(default_factory=list)
    retrieval_triggers: list[str] = field(default_factory=list)
    priority: str = "medium"
    ragas_score: float = 0.0
    retrieval_score: float = 0.0


@dataclass
class ImportRef:
    """Import reference for template rendering."""
    path: str
    note: str = ""


@dataclass
class FolderContext:
    """Complete context for a folder's CLAUDE.md."""
    folder_name: str
    folder_path: Path
    purpose: str
    files: list[FileEntry] = field(default_factory=list)
    imports: list[ImportRef] = field(default_factory=list)
    dependencies: str = ""
    notes: list[str] = field(default_factory=list)


class ClaudeMdGenerator:
    """Generates CLAUDE.md files for folders."""
    
    def __init__(
        self,
        root_path: Path,
        llm_client: Optional[BaseLLMClient] = None,
        offline: bool = False
    ):
        self.root_path = Path(root_path).resolve()
        self.offline = offline
        
        if offline or llm_client is None:
            self.llm_client = LLMClient.from_model_string("offline", offline=True)
        else:
            self.llm_client = llm_client
        
        self.scanner = FileScanner(self.root_path)
        self.extractor = SymbolExtractor()
        self.analyzer = DependencyAnalyzer(self.root_path)
        
        self.folder_summarizer = FolderSummarizer(self.llm_client)
        self.file_describer = FileDescriber(self.llm_client)
        self.dependency_inferrer = DependencyInferrer(self.llm_client)
        
        self.frontmatter_builder = FrontmatterBuilder()
        self.keyword_extractor = KeywordExtractor()
        self.intent_classifier = IntentClassifier()
        
        self.search_metadata_builder = SearchMetadataBuilder()
        self.hybrid_search = HybridSearchStrategy(weights=RankingWeights())
        
        self.layer_manager = LayerProtocolManager()
        self.enable_layers = True
        
        templates_dir = Path(__file__).parent / "templates"
        self.jinja_env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.template = self.jinja_env.get_template("claude_md.jinja2")
    
    def generate_for_folder(self, folder: ScannedFolder) -> str:
        """Generate CLAUDE.md content for a folder."""
        file_symbols_list = []
        for scanned_file in folder.files:
            symbols = self.extractor.extract(scanned_file.path, scanned_file.language)
            file_symbols_list.append(symbols)
            self.analyzer.add_file_symbols(symbols)
        
        all_symbols_summary = []
        for fs in file_symbols_list:
            all_symbols_summary.append(fs.summary)
        symbol_summary = "; ".join(all_symbols_summary[:5])
        
        readme_content = None
        if folder.readme_path:
            try:
                readme_content = folder.readme_path.read_text(encoding="utf-8", errors="replace")[:1000]
            except Exception:
                pass
        
        purpose_result = self.folder_summarizer.summarize(
            folder_name=folder.path.name,
            file_list=[f.path.name for f in folder.files],
            symbol_summary=symbol_summary,
            readme_content=readme_content
        )
        
        file_entries = []
        for scanned_file, file_symbols in zip(folder.files, file_symbols_list):
            first_lines = ""
            file_content = ""
            try:
                file_content = scanned_file.path.read_text(encoding="utf-8", errors="replace")
                first_lines = "\n".join(file_content.split("\n")[:20])
            except Exception:
                pass
            
            desc_result = self.file_describer.describe(
                filename=scanned_file.path.name,
                language=scanned_file.language,
                symbols=[str(s) for s in file_symbols.symbols[:5]],
                first_lines=first_lines,
                docstring=file_symbols.first_docstring
            )
            
            try:
                rel_path = scanned_file.relative_path
                
                intent_result = self.intent_classifier.classify(
                    file_path=str(rel_path),
                    content_sample=file_content[:500],
                    file_type=scanned_file.extension
                )
                
                keywords_result = self.keyword_extractor.extract(
                    content=file_content,
                    file_path=str(rel_path),
                    symbols=[str(s) for s in file_symbols.symbols[:10]]
                )
                
                all_keywords = list(set(
                    keywords_result.semantic + 
                    keywords_result.bm25 + 
                    keywords_result.topics
                ))
                
                priority = self.frontmatter_builder.prioritize(
                    tokens=scanned_file.estimated_tokens,
                    dependency_count=len([fs for fs in file_symbols_list if scanned_file.path.name in str(fs)])
                )
                
                frontmatter = self.frontmatter_builder.build(
                    file_id=scanned_file.path.stem.replace("-", "_"),
                    file_path=str(rel_path),
                    tokens=scanned_file.estimated_tokens,
                    chunk_type=intent_result.chunk_type,
                    keywords=all_keywords,
                    summary=desc_result.text[:200],
                    when_to_load=intent_result.when_to_load,
                    retrieval_triggers=intent_result.retrieval_triggers,
                    priority=priority
                )
            except Exception as e:
                logger.warning(f"Error generating metadata for {scanned_file.path.name}: {e}")
                frontmatter = ""
                intent_result = None
                all_keywords = []
                intent_result = self.intent_classifier.classify(str(scanned_file.relative_path), file_content[:500])
            
            file_entries.append(FileEntry(
                name=scanned_file.path.name,
                symbols=file_symbols.summary[:60],
                tokens=scanned_file.estimated_tokens,
                description=desc_result.text[:100],
                frontmatter=frontmatter,
                keywords=all_keywords if intent_result else [],
                chunk_type=intent_result.chunk_type if intent_result else "reference",
                when_to_load=intent_result.when_to_load if intent_result else [],
                retrieval_triggers=intent_result.retrieval_triggers if intent_result else [],
                priority=priority if intent_result else "medium"
            ))
        
        # Compute ranking and RAGAS scores
        file_entries = self._rank_and_score_files(file_entries)
        
        # Generate and write layer files if enabled
        if self.enable_layers:
            try:
                layer_output = self.generate_layer_outputs(
                    folder=folder,
                    files=file_entries,
                    purpose=purpose_result.text
                )
                self.write_layers_to_disk(layer_output, folder.path)
            except Exception as e:
                logger.warning(f"Error generating layers for {folder.path}: {e}")
        
        imports = []
        for fs in file_symbols_list:
            for imp in fs.imports[:3]:
                if imp.startswith(".") or "/" in imp:
                    imports.append(ImportRef(path=imp))
        imports = imports[:5]
        
        deps = self.analyzer.get_dependency_summary(folder.path)
        dep_result = self.dependency_inferrer.infer(
            folder_name=folder.path.name,
            folder_purpose=purpose_result.text,
            depends_on=deps.get("depends_on", []),
            used_by=deps.get("used_by", []),
            import_examples=[]
        )
        
        context = FolderContext(
            folder_name=folder.path.name,
            folder_path=folder.path,
            purpose=purpose_result.text,
            files=file_entries,
            imports=imports,
            dependencies=dep_result.text if deps.get("depends_on") or deps.get("used_by") else "",
            notes=[]
        )
        
        return self.render(context)
    
    def render(self, context: FolderContext) -> str:
        """Render CLAUDE.md from context using Jinja2 template."""
        return self.template.render(
            folder_name=context.folder_name,
            purpose=context.purpose,
            files=context.files,
            imports=context.imports,
            dependencies=context.dependencies,
            notes=context.notes
        )
    
    def _rank_and_score_files(self, files: list[FileEntry]) -> list[FileEntry]:
        """
        Rank and score files using hybrid retrieval strategies.
        
        Args:
            files: List of FileEntry objects
            
        Returns:
            Files with ranking and RAGAS scores added
        """
        try:
            # Convert to dict format for ranking
            file_dicts = [
                {
                    'id': f.name.split('.')[0],
                    'path': f.name,
                    'name': f.name,
                    'tokens': f.tokens,
                    'chunk_type': f.chunk_type,
                    'keywords': f.keywords,
                }
                for f in files
            ]
            
            # Prepare search metadata and compute RAGAS scores
            search_metadata_list = self.search_metadata_builder.build_collection([
                {
                    'id': d['id'],
                    'path': d['path'],
                    'name': d['name'],
                    'tokens': d['tokens'],
                    'chunk_type': d['chunk_type'],
                    'keywords': d['keywords'],
                    'summary': files[i].description,
                    'when_to_load': files[i].when_to_load,
                    'retrieval_triggers': files[i].retrieval_triggers,
                }
                for i, d in enumerate(file_dicts)
            ])
            
            # Rank files for folder context (generic query)
            folder_query = "retrieve all relevant context"
            ranked_files = self.hybrid_search.rank_files(
                query=folder_query,
                query_keywords=['context', 'relevant'],
                files=file_dicts
            )
            
            # Merge ranking and RAGAS scores back into FileEntry objects
            for entry, ranked, metadata in zip(files, ranked_files, search_metadata_list):
                entry.retrieval_score = ranked.combined_score
                if metadata.ragas_metrics:
                    entry.ragas_score = metadata.ragas_metrics.answer_relevance
            
            # Sort by retrieval score
            return sorted(files, key=lambda f: f.retrieval_score, reverse=True)
            
        except Exception as e:
            logger.warning(f"Error ranking files: {e}")
            # Return unsorted files on error
            return files
    
    def generate_layer_outputs(
        self,
        folder: ScannedFolder,
        files: list[FileEntry],
        purpose: str = ""
    ) -> MultiLayerOutput:
        """Generate all 4 layers for a folder."""
        files_dict = [
            {
                'id': f.name.split('.')[0],
                'path': f.name,
                'name': f.name,
                'tokens': f.tokens,
                'chunk_type': f.chunk_type,
                'keywords': f.keywords,
                'when_to_load': f.when_to_load,
                'retrieval_triggers': f.retrieval_triggers,
                'priority': f.priority,
                'description': f.description,
                'ragas_score': f.ragas_score,
                'retrieval_score': f.retrieval_score,
            }
            for f in files
        ]
        
        return self.layer_manager.generate_all_layers(
            folder_name=folder.path.name,
            folder_path=folder.path,
            files=files_dict,
            purpose=purpose,
            dependencies="",
        )
    
    def write_layers_to_disk(
        self,
        multi_layer_output: MultiLayerOutput,
        output_dir: Path
    ) -> None:
        """Write individual layer files to .claude/ directory."""
        layers_dir = output_dir / ".claude"
        layers_dir.mkdir(parents=True, exist_ok=True)
        
        if multi_layer_output.layer_1:
            (layers_dir / "L1_quick_index.md").write_text(multi_layer_output.layer_1.content)
        if multi_layer_output.layer_2:
            (layers_dir / "L2_metadata.md").write_text(multi_layer_output.layer_2.content)
        if multi_layer_output.layer_3:
            (layers_dir / "L3_context.md").write_text(multi_layer_output.layer_3.content)
        if multi_layer_output.layer_4:
            (layers_dir / "L4_references.md").write_text(multi_layer_output.layer_4.content)
        
        import json
        (layers_dir / "layer_manifest.json").write_text(
            json.dumps(multi_layer_output.layer_manifest, indent=2)
        )
        
        (layers_dir / "all_layers.md").write_text(multi_layer_output.all_layers_combined)
        
        logger.info(f"Layer files written to {layers_dir}")
    
    def generate_all(
        self,
        min_files: int = 1,
        max_depth: int = 10,
        dry_run: bool = False
    ) -> list[tuple[Path, str]]:
        """
        Generate CLAUDE.md for all qualifying folders.
        
        Returns list of (path, content) tuples.
        """
        self.scanner.max_depth = max_depth
        results = []
        
        for folder in self.scanner.scan_all_folders(min_files=min_files):
            logger.info(f"Processing: {folder.relative_path}")
            
            try:
                content = self.generate_for_folder(folder)
                claude_md_path = folder.path / "CLAUDE.md"
                
                if not dry_run:
                    claude_md_path.write_text(content, encoding="utf-8")
                    logger.info(f"  Written: {claude_md_path}")
                else:
                    logger.info(f"  [dry-run] Would write: {claude_md_path}")
                
                results.append((claude_md_path, content))
                
            except Exception as e:
                logger.error(f"  Error processing {folder.path}: {e}")
        
        return results
