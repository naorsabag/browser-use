#!/usr/bin/env python3
"""
Test script to verify that input messages are being saved to files.
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from browser_use import Agent
from browser_use.llm.openai.chat import ChatOpenAI


def check_debug_messages():
	"""Check if debug_messages directory was created and show file contents."""
	if os.path.exists('debug_messages'):
		files = os.listdir('debug_messages')
		if files:
			print(f'✅ Found {len(files)} message files:')
			for file in sorted(files):
				file_path = os.path.join('debug_messages', file)
				file_size = os.path.getsize(file_path)
				print(f'   📄 {file} ({file_size} bytes)')

				# Show first few lines of each file
				print('      Preview:')
				with open(file_path, encoding='utf-8') as f:
					lines = f.readlines()
					for i, line in enumerate(lines[:5]):  # First 5 lines
						print(f'      {i + 1:2d}: {line.rstrip()}')
					if len(lines) > 5:
						print(f'      ... (+{len(lines) - 5} more lines)')
				print()
		else:
			print('❌ debug_messages directory exists but is empty')
	else:
		print('❌ debug_messages directory was not created')


async def main():
	"""
	Test the message saving functionality.
	"""

	print('🧪 Testing message saving functionality...')
	print('=' * 60)

	# Clean up any existing debug_messages directory
	if os.path.exists('debug_messages'):
		import shutil

		shutil.rmtree('debug_messages')
		print('🗑️  Cleaned up previous debug_messages directory')

	print('\n🤖 Creating agent (this will trigger message generation)...')

	# Initialize the agent
	llm = ChatOpenAI(model='gpt-4.1-mini')

	agent = Agent(
		task='Test task for message saving',
		llm=llm,
		max_steps=1,  # Just one step to test
	)

	print(f'📋 Task: {agent.task}')
	print('🎯 Max steps: 1 (limited for testing)')

	try:
		print('\n🚀 Running agent (this should save messages to files)...')
		await agent.run()

		print('\n✅ Agent execution completed!')

	except Exception as e:
		print(f'\n❌ Agent failed: {e}')
		print('   This might be expected if no API key is set')

	# Check if debug_messages directory was created
	print('\n📁 Checking for saved message files...')
	check_debug_messages()

	print('🏁 Test completed!')


if __name__ == '__main__':
	if not os.getenv('OPENAI_API_KEY'):
		print('⚠️  No OPENAI_API_KEY found')
		print('   The agent will fail, but message files should still be created with system prompt and context')
		print('   Set your API key in .env to see the full execution')

	asyncio.run(main())
