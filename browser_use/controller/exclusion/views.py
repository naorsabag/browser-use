# @file purpose: Data models for tool exclusion service
"""
Data models and views for the tool exclusion service.
"""

from typing import Any

from pydantic import BaseModel

from browser_use.agent.views import AgentStepInfo
from browser_use.browser.views import BrowserStateSummary
from browser_use.filesystem.file_system import FileSystem


class ExclusionRules(BaseModel):
	"""Configuration for tool exclusion rules"""

	# High confidence rules (always apply)
	enable_domain_exclusions: bool = True
	enable_tab_exclusions: bool = True
	enable_file_system_exclusions: bool = True
	enable_upload_exclusions: bool = True

	# Medium confidence rules (usually apply)
	enable_element_exclusions: bool = True
	enable_dropdown_exclusions: bool = True
	enable_navigation_exclusions: bool = True
	enable_content_exclusions: bool = True
	enable_scroll_exclusions: bool = True

	# Low confidence rules (contextual)
	enable_search_exclusions: bool = True
	enable_wait_exclusions: bool = True
	enable_pdf_exclusions: bool = True

	# Thresholds
	min_elements_for_scrollability: int = 5
	min_elements_for_interactivity: int = 1


class ExclusionContext(BaseModel):
	"""Context information for tool exclusion decisions"""

	model_config = {'arbitrary_types_allowed': True}

	# Required context
	browser_state: BrowserStateSummary

	# Optional context
	file_system: FileSystem | None = None
	available_file_paths: list[str] | None = None
	step_info: AgentStepInfo | None = None
	task: str | None = None

	# Additional context for advanced exclusions
	sensitive_data: dict[str, Any] | None = None
	page_extraction_llm: Any | None = None


class ExclusionResult(BaseModel):
	"""Result of tool exclusion analysis"""

	excluded_tools: list[str]
	exclusion_reasons: dict[str, list[str]]  # tool_name -> list of reasons
	stats: dict[str, Any]

	def get_total_excluded(self) -> int:
		"""Get total number of excluded tools"""
		return len(self.excluded_tools)

	def get_exclusion_reason(self, tool_name: str) -> list[str]:
		"""Get exclusion reasons for a specific tool"""
		return self.exclusion_reasons.get(tool_name, [])

	def is_tool_excluded(self, tool_name: str) -> bool:
		"""Check if a specific tool is excluded"""
		return tool_name in self.excluded_tools


class ToolCategory(BaseModel):
	"""Represents a category of tools with exclusion rules"""

	name: str
	tools: list[str]
	exclusion_rule: str
	confidence_level: str  # 'high', 'medium', 'low'
	description: str
