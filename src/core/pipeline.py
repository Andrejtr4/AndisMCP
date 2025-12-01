"""LangGraph pipeline for Playwright test generation."""

from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

load_dotenv(Path(__file__).parent.parent.parent / ".env")

from src.core.schemas import Ctx, PageJob
from src.core.colors import print_info, print_success, print_error, print_section, print_header
from src.tools.crawl_links import crawl_links
from src.tools.scan_site import scan_site
from src.tools.extract_model import extract_model
from src.tools.generate_pom import generate_pom
from src.tools.generate_tests import generate_tests
from src.tools.verify_pom import verify_pom
from src.tools.repair import repair_file


class PlaywrightPipeline:
    """LangGraph workflow for test generation."""

    def __init__(self):
        """Initialize the pipeline."""
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the LangGraph workflow."""

        async def crawl_node(state: Ctx) -> Ctx:
            """Step 1: Crawl base URL and find all links."""
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
            """Step 2: Process all pages."""
            if not state.links:
                return state

            print_section("Processing")
            for idx, url in enumerate(state.links, 1):
                job = PageJob(url=url)
                
                try:
                    # Scan
                    page_data = await scan_site(url)
                    job.dom = page_data.get("dom", "")
                    
                    # Extract with LLM
                    model = extract_model(url, job.dom, state.stories)
                    job.model = model
                    
                    # Generate class name
                    url_part = url.split("/")[-1] or url.split("/")[-2]
                    class_name = "".join(
                        word.capitalize() for word in url_part.replace("-", "_").split("_")
                    ) or "HomePage"
                    
                    # Generate POM
                    pom_path = generate_pom(class_name, model)
                    job.pom_path = pom_path
                    
                    # Generate Tests
                    test_path = generate_tests(pom_path)
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
            """Step 3: Verify POMs."""
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
            """Step 4: Repair POMs."""
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
            """Step 5: Summary."""
            print_section("Summary")
            successful = len([j for j in state.jobs.values() if not j.errors])
            failed = len([j for j in state.jobs.values() if j.errors])
            
            print_success(f"Processed: {len(state.jobs)}, Success: {successful}, Failed: {failed}")
            return state

        # Build workflow
        workflow = StateGraph(Ctx)
        
        # Add nodes
        workflow.add_node("crawl", crawl_node)
        workflow.add_node("process", process_pages_node)
        workflow.add_node("verify", verify_node)
        workflow.add_node("repair", repair_node)
        workflow.add_node("summary", summary_node)
        
        # Add edges (workflow path)
        workflow.set_entry_point("crawl")
        workflow.add_edge("crawl", "process")
        workflow.add_edge("process", "verify")
        workflow.add_edge("verify", "repair")
        workflow.add_edge("repair", "summary")
        workflow.add_edge("summary", END)
        
        return workflow.compile()

    async def execute(self, base_url: str, max_pages: int = 10, stories: Optional[str] = None) -> Ctx:
        """Execute the pipeline."""
        print_header("PLAYWRIGHT TEST GENERATOR")
        print_info(f"URL: {base_url} | Max: {max_pages}")
        
        initial_state = Ctx(
            base_url=base_url,
            max_pages=max_pages,
            stories=stories or "",
        )
        
        result_dict = await self.graph.ainvoke(initial_state.model_dump())
        return Ctx(**result_dict)
