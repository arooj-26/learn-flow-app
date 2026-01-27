-- V002: Seed default Python modules and topics
-- This is a function that creates modules/topics for a given class

CREATE OR REPLACE FUNCTION seed_class_modules(p_class_id UUID) RETURNS void AS $$
DECLARE
    mod_id UUID;
BEGIN
    -- Module 1: Basics
    INSERT INTO modules (id, class_id, name, description, order_index)
    VALUES (uuid_generate_v4(), p_class_id, 'Basics', 'Python fundamentals: variables, types, operators, I/O', 1)
    RETURNING id INTO mod_id;
    INSERT INTO topics (module_id, name, description, order_index) VALUES
        (mod_id, 'Variables & Types', 'Variable declaration, int, float, str, bool', 1),
        (mod_id, 'Operators', 'Arithmetic, comparison, logical operators', 2),
        (mod_id, 'Input/Output', 'print(), input(), string formatting', 3),
        (mod_id, 'Type Conversion', 'int(), float(), str(), type()', 4);

    -- Module 2: Control Flow
    INSERT INTO modules (id, class_id, name, description, order_index)
    VALUES (uuid_generate_v4(), p_class_id, 'Control Flow', 'Conditionals, loops, and flow control', 2)
    RETURNING id INTO mod_id;
    INSERT INTO topics (module_id, name, description, order_index) VALUES
        (mod_id, 'If/Elif/Else', 'Conditional statements and branching', 1),
        (mod_id, 'For Loops', 'Iteration with for loops and range()', 2),
        (mod_id, 'While Loops', 'Condition-based loops and break/continue', 3),
        (mod_id, 'Nested Loops', 'Loop nesting and complex iteration', 4);

    -- Module 3: Data Structures
    INSERT INTO modules (id, class_id, name, description, order_index)
    VALUES (uuid_generate_v4(), p_class_id, 'Data Structures', 'Lists, tuples, dictionaries, sets', 3)
    RETURNING id INTO mod_id;
    INSERT INTO topics (module_id, name, description, order_index) VALUES
        (mod_id, 'Lists', 'List creation, indexing, slicing, methods', 1),
        (mod_id, 'Tuples', 'Immutable sequences and packing/unpacking', 2),
        (mod_id, 'Dictionaries', 'Key-value pairs and dictionary methods', 3),
        (mod_id, 'Sets', 'Set operations: union, intersection, difference', 4),
        (mod_id, 'List Comprehensions', 'Concise list creation with comprehensions', 5);

    -- Module 4: Functions
    INSERT INTO modules (id, class_id, name, description, order_index)
    VALUES (uuid_generate_v4(), p_class_id, 'Functions', 'Defining and using functions', 4)
    RETURNING id INTO mod_id;
    INSERT INTO topics (module_id, name, description, order_index) VALUES
        (mod_id, 'Function Basics', 'def, parameters, return values', 1),
        (mod_id, 'Arguments', 'Positional, keyword, default, *args, **kwargs', 2),
        (mod_id, 'Scope', 'Local vs global scope, LEGB rule', 3),
        (mod_id, 'Lambda Functions', 'Anonymous functions and functional programming', 4),
        (mod_id, 'Recursion', 'Recursive functions and base cases', 5);

    -- Module 5: OOP
    INSERT INTO modules (id, class_id, name, description, order_index)
    VALUES (uuid_generate_v4(), p_class_id, 'OOP', 'Object-Oriented Programming in Python', 5)
    RETURNING id INTO mod_id;
    INSERT INTO topics (module_id, name, description, order_index) VALUES
        (mod_id, 'Classes & Objects', 'Class definition, __init__, self', 1),
        (mod_id, 'Methods', 'Instance, class, and static methods', 2),
        (mod_id, 'Inheritance', 'Single and multiple inheritance, super()', 3),
        (mod_id, 'Encapsulation', 'Public, protected, private attributes', 4),
        (mod_id, 'Polymorphism', 'Method overriding and duck typing', 5);

    -- Module 6: Files
    INSERT INTO modules (id, class_id, name, description, order_index)
    VALUES (uuid_generate_v4(), p_class_id, 'Files', 'File handling and I/O operations', 6)
    RETURNING id INTO mod_id;
    INSERT INTO topics (module_id, name, description, order_index) VALUES
        (mod_id, 'Reading Files', 'open(), read(), readlines(), with statement', 1),
        (mod_id, 'Writing Files', 'write(), writelines(), file modes', 2),
        (mod_id, 'CSV Files', 'csv module for reading/writing CSV', 3),
        (mod_id, 'JSON Files', 'json module for serialization', 4);

    -- Module 7: Errors
    INSERT INTO modules (id, class_id, name, description, order_index)
    VALUES (uuid_generate_v4(), p_class_id, 'Errors', 'Error handling and exceptions', 7)
    RETURNING id INTO mod_id;
    INSERT INTO topics (module_id, name, description, order_index) VALUES
        (mod_id, 'Try/Except', 'Basic exception handling', 1),
        (mod_id, 'Exception Types', 'Built-in exceptions: ValueError, TypeError, etc.', 2),
        (mod_id, 'Raising Exceptions', 'raise statement and custom exceptions', 3),
        (mod_id, 'Finally & Else', 'Cleanup with finally, else clause', 4);

    -- Module 8: Libraries
    INSERT INTO modules (id, class_id, name, description, order_index)
    VALUES (uuid_generate_v4(), p_class_id, 'Libraries', 'Standard library and package management', 8)
    RETURNING id INTO mod_id;
    INSERT INTO topics (module_id, name, description, order_index) VALUES
        (mod_id, 'Importing Modules', 'import, from...import, aliases', 1),
        (mod_id, 'Standard Library', 'math, random, datetime, os, sys', 2),
        (mod_id, 'pip & Packages', 'Installing and using third-party packages', 3),
        (mod_id, 'Virtual Environments', 'venv, managing dependencies', 4);
END;
$$ LANGUAGE plpgsql;
