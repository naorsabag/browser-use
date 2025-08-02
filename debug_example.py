#!/usr/bin/env python3
"""
Debug example for browser-use with focus on prompts.py
This file is specifically designed to trigger the code in prompts.py for debugging.
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from browser_use import Agent
from browser_use.llm.openai.chat import ChatOpenAI


async def main():
	"""
	Main function for debugging browser-use with prompts.py breakpoints.

	Key areas where prompts.py code will be executed:
	1. SystemPrompt.__init__() - when Agent is created
	2. SystemPrompt._load_prompt_template() - loading system prompt
	3. AgentMessagePrompt.get_user_message() - during each step
	4. AgentMessagePrompt._get_browser_state_description() - DOM formatting
	"""

	print('🐛 Starting browser-use debug session...')
	print('📍 Set breakpoints in browser_use/agent/prompts.py:')
	print('   - Line 41: _load_prompt_template()')
	print('   - Line 142: _get_browser_state_description()')
	print('   - Line 250: get_user_message()')
	print('   - Line 218: _get_agent_state_description()')

	# Initialize the model
	llm = ChatOpenAI(
		model='gpt-4.1-mini',
	)

	# Simple task that will trigger prompt generation
	task = 'Find the founders of browser-use'

	# Create agent (this will trigger SystemPrompt.__init__)
	print('\n🤖 Creating agent (will trigger SystemPrompt creation)...')
	agent = Agent(
		task=task,
		llm=llm,
		# Enable additional debugging
		max_steps=3,  # Limit steps for debugging
	)

	# Run the agent (this will trigger AgentMessagePrompt.get_user_message() multiple times)
	print('\n🚀 Running agent (will trigger prompt generation for each step)...')
	try:
		history = await agent.run()
		print('\n✅ Agent completed successfully!')
		print(f'📊 Total steps: {len(history)}')

		# Print final result if available
		if history and hasattr(history[-1], 'result'):
			print(f'📄 Result: {history[-1].result}')

	except Exception as e:
		print(f'\n❌ Agent failed: {e}')
		# Don't re-raise so we can examine the state

	print('\n🏁 Debug session complete!')


if __name__ == '__main__':
	# Ensure we have proper environment setup
	if not os.getenv('OPENAI_API_KEY'):
		print('❌ Please set OPENAI_API_KEY in your .env file')
		print('   You can get one from: https://platform.openai.com/account/api-keys')
		sys.exit(1)

	# Run the debug session
	asyncio.run(main())
