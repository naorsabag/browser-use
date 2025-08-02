import asyncio
import os
import pathlib
import shutil

from dotenv import load_dotenv

from browser_use import Agent
from browser_use.llm import ChatOpenAI

load_dotenv()

"""
Research Report Generator Example

This example demonstrates comprehensive file system usage by creating a research agent that:
1. Searches for information about a specific topic across multiple sources
2. Saves individual findings to separate text files
3. Compiles all findings into a comprehensive markdown report
4. Creates a CSV file with source metadata
5. Generates a final PDF report from the markdown content

The agent will be forced to use multiple file system operations:
- write_file: Creating initial files for each source
- append_file: Adding information as it's found
- read_file: Reviewing saved content to compile final report
- Multiple file types: txt, md, csv, pdf
"""

SCRIPT_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
agent_dir = SCRIPT_DIR / 'research_report'
agent_dir.mkdir(exist_ok=True)
conversation_dir = agent_dir / 'conversations' / 'conversation'
print(f'Agent logs directory: {agent_dir}')

try:
	from lmnr import Laminar

	Laminar.initialize(project_api_key=os.getenv('LMNR_PROJECT_API_KEY'))
except Exception as e:
	print(f'Error initializing Laminar: {e}')

task = """
You are a research assistant tasked with creating a comprehensive research report about "Latest developments in AI assistants and automation tools in 2024".

Please follow these steps using the file system:

1. RESEARCH PHASE:
   - Search for recent AI assistant developments on at least 3 different sources (news sites, tech blogs, etc.)
   - For each source you visit, create a separate text file named "source_1.txt", "source_2.txt", etc.
   - In each source file, save the URL, title, and key findings from that source
   - Use append_file to add additional information as you find more relevant details on each source

2. METADATA COLLECTION:
   - Create a CSV file called "sources_metadata.csv" with columns: source_number, url, title, date_accessed, key_topics
   - Fill this CSV with information about all the sources you visited

3. COMPILATION PHASE:
   - Read all the individual source files you created
   - Compile all findings into a comprehensive markdown report called "ai_developments_report.md"
   - The report should include:
     - Executive summary
     - Key trends identified
     - Detailed findings from each source (reference the source files)
     - Conclusion with future implications

4. FINAL REPORT:
   - Create a PDF version of your markdown report called "ai_developments_report.pdf"
   - Read the final markdown file to verify it contains all necessary information
   - List all files you created and provide a brief summary of what each contains

Requirements:
- You MUST use at least 3 different file types (txt, csv, md, pdf)
- You MUST use both write_file and append_file operations
- You MUST read files you created to verify content before proceeding
- Do NOT use extract_structured_data action - manually extract and organize information
- Make sure each source file contains substantial information (not just titles)

Your final deliverable should be a complete research report with supporting source files and metadata.
""".strip('\n')

llm = ChatOpenAI(model='gpt-4.1-mini')

agent = Agent(
	task=task,
	llm=llm,
	save_conversation_path=str(conversation_dir),
	file_system_path=str(agent_dir / 'fs'),
)


async def main():
	agent_history = await agent.run()
	print(f'Final result: {agent_history.final_result()}', flush=True)

	# Show the files that were created
	fs_dir = agent_dir / 'fs' / 'browseruse_agent_data'
	if fs_dir.exists():
		print(f'\nFiles created in {fs_dir}:')
		for file_path in fs_dir.iterdir():
			if file_path.is_file():
				print(f'  - {file_path.name} ({file_path.stat().st_size} bytes)')

	input('Press Enter to view the final report and clean the file system...')

	# Show the final report if it exists
	report_path = fs_dir / 'ai_developments_report.md'
	if report_path.exists():
		print('\n=== Final Report Content ===')
		print(report_path.read_text())

	# clean the file system
	if (agent_dir / 'fs').exists():
		shutil.rmtree(str(agent_dir / 'fs'))


if __name__ == '__main__':
	asyncio.run(main())
