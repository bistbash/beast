# BEAST - Dynamic Framework for Techni Beer Sheva

A modular, dynamic framework for managing a military school (טכני באר שבע). Built with extensibility and runtime configuration in mind.

## Features

- **Dynamic Hierarchy System**: Roles and ranks are loaded from configuration files, allowing runtime changes
- **Plugin-based Departments**: Departments can be added, removed, or modified without code changes
- **Event-driven Architecture**: Departments communicate via events
- **Automation System**: Dynamic automation registration and execution
- **Hot-reload Support**: Departments and configurations can be reloaded at runtime

## Architecture

### Hierarchy System

The system supports the following roles (defined in `config/hierarchy.yaml`):

- **שוחר/ת** (Shocher) - Student
- **מק"ס/ית** (MAKS) - Class Commander (מפקד כיתה)
- **ממ"ח/ית** (MEMACH) - Section Commander (מפקד שכבה)
- **מפקד/ת תיכון** (Tichon Commander) - High School Commander
- **מפקד/ת מכללה** (Machlala Commander) - College Commander

### Departments

The framework includes four core departments:

1. **הדרכה** (Hadracha) - Education/Instruction Department
   - Manages classes, MAKS, and students
   - Tracks attendance and grades

2. **לוגיסטיקה** (Logistika) - Logistics Department
   - Manages inventory and equipment

3. **כוח אדם** (Kochav Adam) - Human Resources Department
   - Manages personnel and role assignments

4. **תפעול** (Tifool) - Operations Department
   - Manages daily operations and coordination

## Installation

### Requirements

- Python 3.8 or higher
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/bistbash/beast.git
cd beast

# Install dependencies
pip install -r requirements.txt

# Install the package (optional, for development)
pip install -e .
```

## Quick Start

### Basic Usage

```python
from beast.core.factory import create_beast
from beast.core.models.user import User

# Initialize the system
beast = create_beast()

# Get a department
hadracha = beast.registry.get_department("hadracha")

# Create users
maks = User(
    id_number="123456789",
    full_name="יוסי כהן",
    rank_name="maks",
    department="hadracha",
    class_name="יא-1",
    hierarchy_manager=beast.hierarchy_manager
)

# Create a class
classroom = hadracha.create_class("יא-1", maks)

# Run initialization script
python scripts/init_system.py
```

## Configuration

### Hierarchy Configuration

Edit `config/hierarchy.yaml` to modify roles and their permissions:

```yaml
ranks:
  - name: maks
    display_name: "מק\"ס/ית"
    level: 1
    can_manage_classes: true
    departments: ["hadracha"]
```

### Departments Configuration

Edit `config/departments.yaml` to enable/disable departments or add new ones:

```yaml
departments:
  - name: hadracha
    display_name: "הדרכה"
    enabled: true
    module_path: "beast.departments.hadracha.hadracha_department"
    class_name: "HadrachaDepartment"
```

## Creating a New Department

1. Create a new directory under `beast/departments/your_department/`

2. Create your department class inheriting from `BaseDepartment`:

```python
from beast.departments.base_department import BaseDepartment

class YourDepartment(BaseDepartment):
    @property
    def name(self) -> str:
        return "המחלקה שלך"
    
    @property
    def name_en(self) -> str:
        return "your_department"
    
    def get_available_automations(self):
        return {}
```

3. Register it in `config/departments.yaml`

4. The system will automatically load it on next initialization

## Creating Automations

Automations inherit from `BaseAutomation`:

```python
from beast.automation.base_automation import BaseAutomation

class MyAutomation(BaseAutomation):
    @property
    def name(self) -> str:
        return "האוטומציה שלי"
    
    @property
    def name_en(self) -> str:
        return "my_automation"
    
    def execute(self, **kwargs):
        # Your automation logic
        return {"result": "success"}
```

## Project Structure

```
beast/
├── beast/                 # Main package
│   ├── core/             # Core systems (registry, events, etc.)
│   ├── departments/      # Department implementations
│   ├── automation/       # Automation system
│   └── api/             # API layer (future)
├── config/               # Configuration files
├── scripts/              # Utility scripts
├── tests/                # Test suite
└── docs/                 # Documentation
```

## Development

### Running Tests

```bash
# Tests to be added
pytest tests/
```

### Code Style

- Code comments and documentation: English
- User-facing text and display names: Hebrew
- Internal code: English variable/function names

## License

[To be determined]

## Contributing

This is an internal project for Techni Beer Sheva. For questions or suggestions, contact the development team.
