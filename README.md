# AI Agent - Function Calling with Google Gemini

This project implements an AI agent that can execute various file operations using Google's Gemini 2.0 Flash model with function calling capabilities.

## Overview

The AI agent can perform four core operations:
- **List directory contents** with file sizes and types
- **Read file contents** (with truncation for large files)  
- **Write/create files** with content
- **Execute Python files** with optional arguments

All operations are restricted to a secure working directory to prevent unauthorized file access.

## Setup

### Prerequisites
- Python 3.12+
- Google Gemini API key
- `uv` package manager

### Installation
1. Clone the repository
2. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   uv sync
   ```

## Usage

### Basic Command Structure
```bash
uv run main.py "<your prompt>" [--verbose]
```

### Examples

#### List Directory Contents
```bash
uv run main.py "list the directory contents" --verbose
```

#### Read a File
```bash
uv run main.py "read the contents of main.py" --verbose
```

#### Create a File
```bash
uv run main.py "create a file called output.txt with the content 'Hello World'" --verbose
```

#### Execute a Python File
```bash
uv run main.py "run tests.py" --verbose
```

## Architecture

### Core Components

1. **main.py** - Entry point that handles:
   - Command line argument parsing
   - Gemini API client setup
   - Function call orchestration
   - Response handling

2. **functions/get_files_info.py** - Contains:
   - Function schemas for Gemini API
   - Core file operation implementations
   - Security restrictions and validations
   - Function dispatcher (`call_function`)

3. **calculator/** - Example working directory with:
   - Calculator application for testing
   - Unit tests (9 tests total)
   - Package structure demonstration

### Function Schemas

The AI agent uses four predefined function schemas:

- `get_files_info`: List directory contents with metadata
- `get_file_content`: Read file contents (max 10,000 chars)
- `write_file`: Create or overwrite files
- `run_python_file`: Execute Python scripts with arguments

### Security Features

- **Directory Restriction**: All operations confined to working directory
- **Path Validation**: Prevents access outside permitted areas  
- **File Type Checking**: Python execution limited to `.py` files
- **Timeout Protection**: 30-second timeout for script execution
- **Content Limits**: File reading truncated at 10,000 characters

## Technical Details

### Function Calling Implementation

The project uses manual function calling rather than Gemini's automatic function calling to avoid parsing issues with complex type signatures:

1. **Schema Registration**: Function schemas registered with Gemini API
2. **Call Detection**: Manual detection of function calls in AI responses
3. **Function Execution**: Direct function invocation with security checks
4. **Result Integration**: Function results fed back to AI for final response

### Error Handling

- **Path Security Errors**: Blocked attempts to access unauthorized locations
- **File Not Found**: Graceful handling of missing files
- **Execution Timeouts**: Protection against infinite loops
- **Invalid Operations**: Clear error messages for malformed requests

## Testing

The calculator directory contains comprehensive tests:

```bash
# Run unit tests directly
cd calculator && python -m unittest tests.py

# Result: Ran 9 tests in 0.000s - OK
```

### Test Coverage
- Basic arithmetic operations (addition, subtraction, multiplication, division)
- Complex expressions with multiple operations  
- Error handling (empty expressions, invalid operators, insufficient operands)
- File operation security boundaries

## Troubleshooting

### Common Issues

1. **"ValueError: Failed to parse the parameter function_call_part"**
   - **Fixed**: Updated to use manual function calling instead of automatic parsing

2. **Function calls timeout**  
   - Check for recursive calls in executed scripts
   - Verify file paths are correct
   - Ensure working directory permissions

3. **Path access denied**
   - Verify files are within the calculator working directory
   - Check file permissions
   - Confirm paths use relative addressing

## Development

### Adding New Functions

1. Define function schema in `functions/get_files_info.py`
2. Implement function with security checks
3. Add function to `function_map` in `call_function`
4. Update schema list in `main.py`

### Working Directory

The AI agent operates within the `calculator/` directory by default. This can be modified in the `call_function` implementation:

```python
working_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "calculator")
```

## License

[Specify your license here]

## Contributing

[Add contribution guidelines here]
