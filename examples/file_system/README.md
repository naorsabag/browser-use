# File System Examples

This directory contains examples demonstrating how browser-use agents can effectively utilize the file system to organize, store, and process data during web automation tasks.

## Available Examples

### 1. Basic File System Usage (`file_system.py`)
**Purpose**: Demonstrates basic file system operations
- Visits a simple webpage
- Saves title and content to a markdown file
- Shows fundamental read/write operations

### 2. Document Processing (`alphabet_earnings.py`)
**Purpose**: Shows PDF handling and data extraction
- Downloads and processes PDF documents
- Extracts key data points from financial reports
- Demonstrates external file handling

### 3. Data Collection (`excel_sheet.py`)
**Purpose**: Creates structured data files
- Collects stock price information
- Generates CSV files with tabular data
- Shows data organization and formatting

### 4. Research Report Generator (`research_report_generator.py`) ⭐ NEW
**Purpose**: Comprehensive research workflow with multiple file types
- **Research Phase**: Visits multiple sources and saves findings to individual text files
- **Metadata Collection**: Creates CSV database of sources
- **Compilation**: Builds comprehensive markdown report from collected data
- **Final Report**: Generates PDF version of the research

**File Types Used**: `.txt`, `.csv`, `.md`, `.pdf`  
**Operations**: `write_file`, `append_file`, `read_file`  
**Complexity**: High - demonstrates complete research workflow

### 5. Web Data Collector (`web_data_collector.py`) ⭐ NEW
**Purpose**: End-to-end data collection and analysis pipeline
- **Setup**: Creates activity logs to track progress
- **Collection**: Gathers structured product data into JSON files
- **Aggregation**: Compiles data into CSV database
- **Analysis**: Performs data analysis and creates insights report
- **Processing**: Generates summary statistics and final reports

**File Types Used**: `.txt`, `.json`, `.csv`, `.md`, `.pdf`  
**Operations**: `write_file`, `append_file`, `read_file`  
**Complexity**: High - demonstrates complete data pipeline

## Key File System Features Demonstrated

### File Types Supported
- **Text Files (`.txt`)**: Logs, notes, raw text data
- **Markdown (`.md`)**: Formatted reports and documentation
- **JSON (`.json`)**: Structured data storage
- **CSV (`.csv`)**: Tabular data and databases
- **PDF (`.pdf`)**: Final reports and document generation

### File Operations
- **`write_file`**: Create new files or overwrite existing content
- **`append_file`**: Add content to existing files
- **`read_file`**: Access file content for processing or verification
- **`replace_file_str`**: Find and replace text within files

### Advanced Patterns

#### Multi-Stage Workflows
The new examples demonstrate how to:
1. **Collect** data from multiple sources
2. **Organize** information into structured files
3. **Process** and analyze collected data
4. **Generate** comprehensive reports
5. **Maintain** activity logs and metadata

#### File Organization Strategies
- **Individual files per data item** (source_1.txt, laptop_1.json)
- **Centralized databases** (sources_metadata.csv, laptops_database.csv)
- **Progress tracking** (collection_log.txt)
- **Final deliverables** (reports in multiple formats)

## Running the Examples

Each example follows the same pattern:

```python
# Install dependencies
uv sync

# Run an example
python examples/file_system/research_report_generator.py
python examples/file_system/web_data_collector.py
```

The examples will:
1. Create a dedicated directory for file storage
2. Execute the automation task with extensive file system usage
3. Display created files and their contents
4. Clean up the file system after review

## When to Use File System Features

File system integration is particularly valuable for:

- **Research Tasks**: Collecting and organizing information from multiple sources
- **Data Collection**: Systematically gathering and structuring web data
- **Report Generation**: Creating formatted documents from collected information
- **Workflow Tracking**: Maintaining logs of agent activities
- **Data Analysis**: Processing collected data and generating insights
- **Content Management**: Organizing and accessing previously saved information

The file system enables agents to maintain state across multiple web interactions, build comprehensive datasets, and generate professional-quality deliverables.
