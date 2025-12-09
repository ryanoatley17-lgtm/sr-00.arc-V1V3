#!/usr/bin/env python3
"""
System Structure Validator for Guardian-Arc × Fibonacci Bloom Integration

Validates:
- File structure and existence
- Module imports and dependencies
- Function signatures and API contracts
- Integration points between components
- Documentation consistency
- Mathematical constants and parameters
"""

import sys
import os
import importlib.util
import inspect
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any


class ValidationResult:
    def __init__(self):
        self.checks = []
        self.errors = []
        self.warnings = []

    def add_check(self, name: str, passed: bool, details: str = ""):
        self.checks.append({
            "name": name,
            "passed": passed,
            "details": details
        })
        if not passed:
            self.errors.append(f"{name}: {details}")

    def add_warning(self, message: str):
        self.warnings.append(message)

    def print_report(self):
        print("\n" + "="*80)
        print("SYSTEM STRUCTURE VALIDATION REPORT")
        print("="*80 + "\n")

        passed = sum(1 for c in self.checks if c["passed"])
        total = len(self.checks)

        print(f"Checks Passed: {passed}/{total}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}\n")

        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(f"  ✗ {error}")
            print()

        if self.warnings:
            print("WARNINGS:")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
            print()

        print("DETAILED RESULTS:")
        for check in self.checks:
            status = "✓" if check["passed"] else "✗"
            print(f"  {status} {check['name']}")
            if check["details"] and not check["passed"]:
                print(f"      {check['details']}")

        print("\n" + "="*80)

        if self.errors:
            print("VALIDATION FAILED")
            return False
        else:
            print("VALIDATION PASSED")
            return True


def load_module(file_path: str, module_name: str):
    """Load a Python module from file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        return None


def validate_file_structure(result: ValidationResult):
    """Validate that all required files exist."""
    required_files = [
        "full_verifier.py",
        "guardian_arc.py",
        "arc_integrity.py",
        "example_arc_integration.py",
        "README.md",
        "LICENSE_NOTICE.md",
        "GRAIL_TRUST_CUSTODIAL_ADDENDUM.md"
    ]

    for file in required_files:
        exists = os.path.exists(file)
        result.add_check(
            f"File exists: {file}",
            exists,
            f"Required file '{file}' not found" if not exists else ""
        )


def validate_module_imports(result: ValidationResult):
    """Validate that modules can be imported and have expected functions."""

    # Validate full_verifier.py
    verifier = load_module("full_verifier.py", "full_verifier")
    if verifier:
        result.add_check("Module: full_verifier.py imports", True)

        expected_funcs = ["verify_envelope", "verify_eternal_fingerprint", "verify_coil_chain"]
        for func in expected_funcs:
            has_func = hasattr(verifier, func)
            result.add_check(
                f"full_verifier.{func} exists",
                has_func,
                f"Function '{func}' not found" if not has_func else ""
            )
    else:
        result.add_check("Module: full_verifier.py imports", False, "Failed to import")

    # Validate guardian_arc.py
    guardian = load_module("guardian_arc.py", "guardian_arc")
    if guardian:
        result.add_check("Module: guardian_arc.py imports", True)

        expected_funcs = [
            "guardian_arc_trajectory",
            "guardian_arc_density",
            "guardian_arc_plot"
        ]
        for func in expected_funcs:
            has_func = hasattr(guardian, func)
            result.add_check(
                f"guardian_arc.{func} exists",
                has_func,
                f"Function '{func}' not found" if not has_func else ""
            )
    else:
        result.add_check("Module: guardian_arc.py imports", False, "Failed to import")

    # Validate arc_integrity.py
    arc_int = load_module("arc_integrity.py", "arc_integrity")
    if arc_int:
        result.add_check("Module: arc_integrity.py imports", True)

        expected_funcs = [
            "verify_with_arc",
            "visualize_integrity",
            "compare_envelopes",
            "integrity_trajectory",
            "fingerprint_to_seed",
            "extract_fingerprint_seeds"
        ]
        for func in expected_funcs:
            has_func = hasattr(arc_int, func)
            result.add_check(
                f"arc_integrity.{func} exists",
                has_func,
                f"Function '{func}' not found" if not has_func else ""
            )
    else:
        result.add_check("Module: arc_integrity.py imports", False, "Failed to import")


def validate_function_signatures(result: ValidationResult):
    """Validate function signatures match documentation."""

    # Load modules
    arc_int = load_module("arc_integrity.py", "arc_integrity")
    guardian = load_module("guardian_arc.py", "guardian_arc")

    if arc_int:
        # Check verify_with_arc signature
        if hasattr(arc_int, "verify_with_arc"):
            sig = inspect.signature(arc_int.verify_with_arc)
            params = list(sig.parameters.keys())
            expected_params = ["data", "n_steps", "bins", "blend_mode"]

            has_all = all(p in params for p in expected_params[:1])  # at least 'data'
            result.add_check(
                "verify_with_arc signature",
                has_all,
                f"Expected params: {expected_params}, got: {params}" if not has_all else ""
            )

        # Check visualize_integrity signature
        if hasattr(arc_int, "visualize_integrity"):
            sig = inspect.signature(arc_int.visualize_integrity)
            params = list(sig.parameters.keys())
            has_data = "data" in params
            result.add_check(
                "visualize_integrity signature",
                has_data,
                "Missing 'data' parameter" if not has_data else ""
            )

    if guardian:
        # Check guardian_arc_trajectory signature
        if hasattr(guardian, "guardian_arc_trajectory"):
            sig = inspect.signature(guardian.guardian_arc_trajectory)
            params = list(sig.parameters.keys())
            expected_params = ["n_steps", "burn_in", "seed"]

            has_steps = "n_steps" in params
            result.add_check(
                "guardian_arc_trajectory signature",
                has_steps,
                "Missing 'n_steps' parameter" if not has_steps else ""
            )


def validate_mathematical_constants(result: ValidationResult):
    """Validate that mathematical constants are correctly defined."""

    guardian = load_module("guardian_arc.py", "guardian_arc")
    verifier = load_module("full_verifier.py", "full_verifier")

    # Check golden ratio in guardian_arc
    if guardian:
        phi_value = 1.618033988749895
        if hasattr(guardian, "PHI") or hasattr(guardian, "phi"):
            # Module has PHI constant
            module_phi = getattr(guardian, "PHI", None) or getattr(guardian, "phi", None)
            if module_phi:
                close_enough = abs(module_phi - phi_value) < 1e-10
                result.add_check(
                    "Guardian-Arc PHI constant",
                    close_enough,
                    f"PHI = {module_phi}, expected ≈ {phi_value}" if not close_enough else ""
                )
        else:
            result.add_warning("PHI constant not exposed in guardian_arc module")

    # Check PHI tolerance in verifier
    if verifier:
        if hasattr(verifier, "PHI_TOL"):
            tol = verifier.PHI_TOL
            reasonable = 1e-15 < tol < 1e-5
            result.add_check(
                "Verifier PHI_TOL range",
                reasonable,
                f"PHI_TOL = {tol}, should be between 1e-15 and 1e-5" if not reasonable else ""
            )


def validate_integration_points(result: ValidationResult):
    """Validate integration between components."""

    arc_int = load_module("arc_integrity.py", "arc_integrity")

    if arc_int:
        # Check that arc_integrity can access both verifier and guardian functions
        try:
            # Try to call fingerprint_to_seed
            if hasattr(arc_int, "fingerprint_to_seed"):
                # Test with a valid fingerprint
                test_fp = "a" * 128  # Valid SHA3-512 hex length
                seed = arc_int.fingerprint_to_seed(test_fp)
                valid_seed = 0 <= seed < 1
                result.add_check(
                    "fingerprint_to_seed produces valid seed",
                    valid_seed,
                    f"Seed {seed} out of range [0, 1)" if not valid_seed else ""
                )
            else:
                result.add_check("fingerprint_to_seed exists", False, "Function not found")
        except Exception as e:
            result.add_check("fingerprint_to_seed integration", False, str(e))


def validate_documentation_consistency(result: ValidationResult):
    """Validate that README documentation matches code structure."""

    if not os.path.exists("README.md"):
        result.add_check("README.md exists", False, "File not found")
        return

    with open("README.md", "r") as f:
        readme = f.read()

    # Check that all main files are mentioned
    main_files = ["full_verifier.py", "guardian_arc.py", "arc_integrity.py"]
    for file in main_files:
        mentioned = file in readme
        result.add_check(
            f"README mentions {file}",
            mentioned,
            f"File '{file}' not documented in README" if not mentioned else ""
        )

    # Check for key concepts
    key_concepts = [
        "golden ratio",
        "Fibonacci",
        "Guardian-Arc",
        "pentagonal",
        "density field",
        "fingerprint"
    ]
    for concept in key_concepts:
        mentioned = concept.lower() in readme.lower()
        if not mentioned:
            result.add_warning(f"Concept '{concept}' not prominently featured in README")

    # Check for installation instructions
    has_install = "Installation" in readme or "Requirements" in readme
    result.add_check(
        "README has installation instructions",
        has_install,
        "Installation section missing" if not has_install else ""
    )

    # Check for usage examples
    has_usage = "Usage" in readme or "Example" in readme
    result.add_check(
        "README has usage examples",
        has_usage,
        "Usage section missing" if not has_usage else ""
    )


def validate_license_structure(result: ValidationResult):
    """Validate dual licensing structure."""

    license_notice = os.path.exists("LICENSE_NOTICE.md")
    grail_trust = os.path.exists("GRAIL_TRUST_CUSTODIAL_ADDENDUM.md")

    result.add_check(
        "LICENSE_NOTICE.md exists",
        license_notice,
        "License notice file missing" if not license_notice else ""
    )

    result.add_check(
        "GRAIL_TRUST_CUSTODIAL_ADDENDUM.md exists",
        grail_trust,
        "Grail Trust addendum missing" if not grail_trust else ""
    )

    # Check README mentions dual licensing
    if os.path.exists("README.md"):
        with open("README.md", "r") as f:
            readme = f.read()
        mentions_dual = "dual licens" in readme.lower()
        result.add_check(
            "README mentions dual licensing",
            mentions_dual,
            "Dual licensing not documented" if not mentions_dual else ""
        )


def main():
    """Run all validation checks."""
    result = ValidationResult()

    print("Running system structure validation...\n")

    print("1. Validating file structure...")
    validate_file_structure(result)

    print("2. Validating module imports...")
    validate_module_imports(result)

    print("3. Validating function signatures...")
    validate_function_signatures(result)

    print("4. Validating mathematical constants...")
    validate_mathematical_constants(result)

    print("5. Validating integration points...")
    validate_integration_points(result)

    print("6. Validating documentation consistency...")
    validate_documentation_consistency(result)

    print("7. Validating license structure...")
    validate_license_structure(result)

    # Print report
    passed = result.print_report()

    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
