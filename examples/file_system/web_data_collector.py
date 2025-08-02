import asyncio
import os
import pathlib
import shutil

from dotenv import load_dotenv

from browser_use import Agent
from browser_use.llm import ChatOpenAI

load_dotenv()

"""
Web Data Collector Example

This example demonstrates file system usage through a data collection and analysis workflow:
1. Collects product information from an e-commerce site
2. Saves raw data to JSON files
3. Processes and analyzes the data
4. Creates summary reports in multiple formats
5. Maintains logs of the collection process

The agent will use various file system operations to organize and process collected data.
"""

SCRIPT_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
agent_dir = SCRIPT_DIR / 'data_collection'
agent_dir.mkdir(exist_ok=True)
conversation_dir = agent_dir / 'conversations' / 'conversation'
print(f'Agent logs directory: {agent_dir}')

try:
	from lmnr import Laminar

	Laminar.initialize(project_api_key=os.getenv('LMNR_PROJECT_API_KEY'))
except Exception as e:
	print(f'Error initializing Laminar: {e}')

task = """
You are a data collection agent tasked with gathering and analyzing product information from an online store.

Your mission: Collect data about laptops from an e-commerce website and create a comprehensive analysis.

WORKFLOW STEPS:

1. SETUP PHASE:
   - Create a log file called "collection_log.txt" to track your progress
   - Write an initial entry with the current timestamp and task description

2. DATA COLLECTION:
   - Go to an e-commerce site (like Amazon, Best Buy, or similar) and search for "laptops"
   - Collect information for at least 5 different laptop products
   - For each laptop, create a separate JSON file named "laptop_1.json", "laptop_2.json", etc.
   - Each JSON file should contain: name, price, brand, specifications, rating, availability
   - After collecting each product, append an entry to your log file with the product name and status

3. DATA AGGREGATION:
   - Read all the individual laptop JSON files you created
   - Create a comprehensive CSV file called "laptops_database.csv" with all products
   - Include columns: product_name, brand, price, rating, specifications_summary, file_reference

4. ANALYSIS PHASE:
   - Analyze the collected data and create insights
   - Write a markdown analysis report called "laptop_analysis.md" that includes:
     - Price range analysis
     - Brand comparison
     - Top-rated products
     - Specifications trends
     - Recommendations by price category
   - Use the data from your CSV file as the source for this analysis

5. FINAL PROCESSING:
   - Create a summary JSON file called "collection_summary.json" with:
     - Total products collected
     - Date of collection
     - Price statistics (min, max, average)
     - Most common brands
     - File inventory (list of all files created)
   - Append a final entry to your log file with completion status
   - Generate a PDF report from your markdown analysis

6. VERIFICATION:
   - Read your log file to show the complete collection process
   - Read the collection summary to display final statistics
   - List all files you created and their purposes

REQUIREMENTS:
- Use ALL file types: txt (log), json (data), csv (database), md (analysis), pdf (report)
- Use BOTH write_file AND append_file operations
- Must read files to verify content and use previous data for subsequent steps
- Show a clear workflow from raw data collection to final analysis
- Each file should serve a specific purpose in the data pipeline

Your success will be measured by the completeness of your data collection and the quality of your analysis pipeline using the file system.
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
		for file_path in sorted(fs_dir.iterdir()):
			if file_path.is_file():
				size = file_path.stat().st_size
				print(f'  - {file_path.name:<25} ({size:>6} bytes)')

	input('Press Enter to view collection log and summary, then clean the file system...')

	# Show the collection log if it exists
	log_path = fs_dir / 'collection_log.txt'
	if log_path.exists():
		print('\n=== Collection Log ===')
		print(log_path.read_text())

	# Show the summary if it exists
	summary_path = fs_dir / 'collection_summary.json'
	if summary_path.exists():
		print('\n=== Collection Summary ===')
		print(summary_path.read_text())

	# clean the file system
	if (agent_dir / 'fs').exists():
		shutil.rmtree(str(agent_dir / 'fs'))


if __name__ == '__main__':
	asyncio.run(main())
