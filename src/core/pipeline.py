"""LangGraph Pipeline für Playwright Test-Generierung."""

import asyncio
import subprocess
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import AzureChatOpenAI


load_dotenv(Path(__file__).parent.parent.parent / ".env")


from src.core.schemas import Ctx, PageJob
from src.core.colors import print_info, print_success, print_error, print_section, print_header
from src.core.config import TestGenerationConfig, DEFAULT_CONFIG
from src.tools.crawl_links import crawl_links
from src.tools.scan_site import scan_site
from src.tools.extract_model import extract_model
from src.tools.generate_pom import generate_pom
from src.tools.generate_tests_ts import generate_tests_ts
from src.tools.verify_pom import verify_pom
from src.tools.repair import repair_file


class PlaywrightPipeline:
    """
    LangGraph Workflow für die Test-Generierung.
    
    Orchestriert den gesamten Prozess:
    1. Crawling → 2. Processing → 3. Verify → 4. Repair → 5. Summary → 6. UI öffnen
    """

    def __init__(self, config: TestGenerationConfig = None):
        """Initialisiere die Pipeline mit optionaler Konfiguration."""
        self.config = config or DEFAULT_CONFIG
        
        self.llm_gpt5 = AzureChatOpenAI(
            base_url="https://api.competence-centre-cc-genai-prod.enbw-az.cloud/openai/deployments/gpt-5",
            openai_api_version="2024-10-21",
            api_key=os.environ.get("api_key", ""),
        )
        
        self.graph = self._build_graph()

    def _build_graph(self):
        """Baut den LangGraph Workflow mit allen Nodes und Edges."""

        async def crawl_node(state: Ctx) -> Ctx:
            """
            SCHRITT 1: Crawle Basis-URL und finde alle Links.
            
            Nutzt Playwright um alle Links auf der Startseite zu finden.
            """
            print_section("Crawling")
            try:
                result = await crawl_links(state.base_url)
                all_links = result.get("links", [])
                state.links = all_links[:state.max_pages] if state.max_pages else all_links
                print_success(f"Found {len(state.links)} links")
                return state
            except Exception as e:
                state.errors.append(f"Crawl error: {str(e)}")
                return state

        async def process_pages_node(state: Ctx) -> Ctx:
            """
            SCHRITT 2: Verarbeite alle gefundenen Seiten.
            
            Für jede Seite:
            - Scanne DOM
            - Extrahiere UI-Modell mit LLM
            - Generiere POM (mit optionaler KI-Verbesserung)
            - Generiere TypeScript-Tests
            """
            if not state.links:
                return state

            print_section("Processing")
            for idx, url in enumerate(state.links, 1):
                job = PageJob(url=url)
                
                try:
                    # 2.1: Scanne die Seite und hole DOM
                    page_data = await scan_site(url)
                    job.dom = page_data.get("dom", "")
                    
                    # 2.2: Extrahiere UI-Modell mit LLM
                    model = extract_model(url, job.dom, state.stories)
                    job.model = model
                    
                    # 2.3: Generiere Klassennamen aus URL
                    url_part = url.split("/")[-1] or url.split("/")[-2]
                    class_name = "".join(
                        word.capitalize() for word in url_part.replace("-", "_").split("_")
                    ) or "HomePage"
                    
                    # 2.4: Generiere POM (mit KI-Enhancement je nach Config)
                    pom_path = generate_pom(class_name, model, use_ai=self.config.enhance_pom)
                    job.pom_path = pom_path
                    
                    # 2.5: Generiere TypeScript Tests
                    test_path = generate_tests_ts(pom_path, state.stories)
                    job.test_path = test_path
                    
                    print_success(f"[{idx}/{len(state.links)}] {class_name}")
                    state.total_processed += 1
                    
                except Exception as e:
                    job.errors.append(str(e))
                    state.total_errors += 1
                    print_error(f"[{idx}/{len(state.links)}] Error: {str(e)[:60]}")

                state.jobs[url] = job

            return state

        def verify_node(state: Ctx) -> Ctx:
            """
            SCHRITT 3: Verifiziere alle generierten POMs.
            
            Prüft ob die POMs syntaktisch korrekt sind.
            """
            if not state.jobs:
                return state
                
            print_section("Verifying")
            for url, job in state.jobs.items():
                if job.pom_path:
                    try:
                        ok, msg = verify_pom(job.pom_path)
                        if not ok:
                            job.errors.append("Verification failed")
                    except Exception as e:
                        job.errors.append(str(e))
            return state

        def repair_node(state: Ctx) -> Ctx:
            """
            SCHRITT 4: Repariere fehlerhafte POMs.
            
            Nutzt LLM um Syntax-Fehler automatisch zu beheben.
            """
            has_errors = any(job.errors for job in state.jobs.values())
            if not has_errors:
                return state
                
            print_section("Repairing")
            for url, job in state.jobs.items():
                if job.errors and job.pom_path:
                    try:
                        repair_file(job.pom_path)
                        job.errors.clear()
                        print_success("Repaired")
                    except Exception as e:
                        pass
            return state

        def summary_node(state: Ctx) -> Ctx:
            """
            SCHRITT 5: Zeige Zusammenfassung.
            
            Gibt Statistiken über erfolgreiche/fehlgeschlagene Jobs aus.
            """
            print_section("Summary")
            successful = len([j for j in state.jobs.values() if not j.errors])
            failed = len([j for j in state.jobs.values() if j.errors])
            
            print_success(f"Processed: {len(state.jobs)}, Success: {successful}, Failed: {failed}")
            return state
        
        def open_playwright_ui_node(state: Ctx) -> Ctx:
            """
            SCHRITT 6: Öffne Playwright UI im Browser.
            
            Startet automatisch die Playwright Test-UI falls Tests erfolgreich generiert wurden.
            """
            # Öffne nur wenn wir erfolgreiche Tests haben
            successful = len([j for j in state.jobs.values() if not j.errors])
            if successful > 0:
                print_section("Opening Playwright UI")
                try:
                    # Ensure we're in the out directory where tests are
                    out_dir = Path("out").resolve()
                    if out_dir.exists():
                        print_info("Starting Playwright UI...")
                        # Open Playwright UI in background (non-blocking)
                        subprocess.Popen(
                            ["npx", "playwright", "test", "--ui"],
                            cwd=str(out_dir),
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        print_success("Playwright UI opened!")
                except Exception as e:
                    print_error(f"Could not open Playwright UI: {str(e)}")
            return state

        # Workflow-Graph
        workflow = StateGraph(Ctx)
        
        # Füge alle Nodes (Schritte) hinzu
        workflow.add_node("crawl", crawl_node)              # 1. Crawling
        workflow.add_node("process", process_pages_node)    # 2. Processing
        workflow.add_node("verify", verify_node)            # 3. Verification
        workflow.add_node("repair", repair_node)            # 4. Reparatur
        workflow.add_node("summary", summary_node)          # 5. Zusammenfassung
        workflow.add_node("open_ui", open_playwright_ui_node)  # 6. UI öffnen
        
        # Definiere die Workflow-Reihenfolge (Edges = Pfeile zwischen Nodes)
        workflow.set_entry_point("crawl")          # Start bei "crawl"
        workflow.add_edge("crawl", "process")      # crawl → process
        workflow.add_edge("process", "verify")     # process → verify
        workflow.add_edge("verify", "repair")      # verify → repair
        workflow.add_edge("repair", "summary")     # repair → summary
        workflow.add_edge("summary", "open_ui")    # summary → open_ui
        workflow.add_edge("open_ui", END)          # open_ui → ENDE
        
        # Kompiliere den Graphen zu einem ausführbaren Workflow
        return workflow.compile()

    async def execute(self, base_url: str, max_pages: int = 10, stories: Optional[str] = None, 
                     config: TestGenerationConfig = None) -> Ctx:
        """
        Führt die komplette Pipeline aus.
        
        Args:
            base_url: Start-URL für Crawling
            max_pages: Maximale Anzahl zu verarbeitender Seiten
            stories: Optionale User Stories für Test-Generierung
            config: Optionale Konfiguration (überschreibt Standard)
        
        Returns:
            Finaler Context mit allen Ergebnissen
        """
        # Überschreibe Config falls angegeben
        if config:
            self.config = config
        
        # Zeige Start-Info
        print_header("PLAYWRIGHT TEST GENERATOR")
        print_info(f"URL: {base_url} | Max: {max_pages} | Quality: {self.config.quality}")
        
        # Erstelle initialen State
        initial_state = Ctx(
            base_url=base_url,
            max_pages=max_pages,
            stories=stories or "",
        )
        
        # Führe den Workflow aus und gib Ergebnis zurück
        result_dict = await self.graph.ainvoke(initial_state.model_dump())
        return Ctx(**result_dict)
