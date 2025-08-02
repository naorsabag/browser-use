#!/usr/bin/env python3
"""
Enhanced debug example with specific watch expressions for prompts.py debugging.
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from browser_use import Agent
from browser_use.llm.openai.chat import ChatOpenAI


async def main():
	"""
	Debug prompts.py with specific breakpoints and watch expressions.

	BREAKPOINTS TO SET:
	1. browser_use/agent/prompts.py:41 (_load_prompt_template)
	2. browser_use/agent/prompts.py:142 (_get_browser_state_description)
	3. browser_use/agent/prompts.py:250 (get_user_message)
	4. browser_use/agent/prompts.py:143 (elements_text creation)

	WATCH EXPRESSIONS TO ADD:
	- self.flash_mode
	- self.use_thinking
	- self.prompt_template[:100] if hasattr(self, 'prompt_template') else "Not loaded"
	- len(elements_text) if 'elements_text' in locals() else 0
	- self.browser_state.url if hasattr(self, 'browser_state') else "No browser state"
	- len(self.browser_state.tabs) if hasattr(self, 'browser_state') else 0
	- self.step_info.step_number if hasattr(self, 'step_info') and self.step_info else "No step info"
	- len(self.screenshots) if hasattr(self, 'screenshots') else 0
	"""

	print('🐛 Starting enhanced prompts.py debugging...')
	print('\n📍 SET THESE BREAKPOINTS:')
	print('   • browser_use/agent/prompts.py:41  (_load_prompt_template)')
	print('   • browser_use/agent/prompts.py:142 (_get_browser_state_description)')
	print('   • browser_use/agent/prompts.py:250 (get_user_message)')
	print('   • browser_use/agent/prompts.py:143 (elements_text = ...)')

	print('\n⌚ ADD THESE WATCH EXPRESSIONS:')
	watch_expressions = [
		'self.flash_mode',
		'self.use_thinking',
		"self.prompt_template[:100] if hasattr(self, 'prompt_template') else 'Not loaded'",
		"len(elements_text) if 'elements_text' in locals() else 0",
		"self.browser_state.url if hasattr(self, 'browser_state') else 'No browser state'",
		"len(self.browser_state.tabs) if hasattr(self, 'browser_state') else 0",
		"self.step_info.step_number if hasattr(self, 'step_info') and self.step_info else 'No step info'",
		"len(self.screenshots) if hasattr(self, 'screenshots') else 0",
	]

	for i, expr in enumerate(watch_expressions, 1):
		print(f'   {i}. {expr}')

	print('\n🎮 DEBUG CONSOLE COMMANDS TO TRY:')
	console_commands = [
		"print(f'Current URL: {self.browser_state.url}')",
		"print(f'Page title: {self.browser_state.title}')",
		"print(f'Number of tabs: {len(self.browser_state.tabs)}')",
		'print(f\'Elements text length: {len(elements_text) if "elements_text" in locals() else "N/A"}\')',
		'[tab.url for tab in self.browser_state.tabs]',
		'self.browser_state.element_tree.clickable_elements_to_string()[:200]',
		'dir(self.browser_state)',
	]

	for i, cmd in enumerate(console_commands, 1):
		print(f'   {i}. {cmd}')

	# Initialize with debug-friendly settings
	llm = ChatOpenAI(model='gpt-4.1-mini')

	agent = Agent(
		task='Find information about browser-use on their GitHub page',
		llm=llm,
		max_steps=2,  # Limit for debugging
	)

	print('\n🚀 Starting agent execution...')
	print(f'   Task: {agent.task}')
	print(f'   Max steps: {agent.max_steps}')

	try:
		await agent.run()
		print('\n✅ Debug session completed successfully!')
	except Exception as e:
		print(f'\n❌ Error during execution: {e}')
		print("   This is normal if you don't have an API key set")


if __name__ == '__main__':
	if not os.getenv('OPENAI_API_KEY'):
		print('⚠️  No OPENAI_API_KEY found - the agent will fail, but you can still debug the prompt generation!')
		print('   Set your API key in .env to see the full execution')

	asyncio.run(main())
