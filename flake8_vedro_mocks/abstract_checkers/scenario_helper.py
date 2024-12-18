import ast
import re
from typing import List, Tuple

from flake8_vedro_mocks.types import FuncType

SCENARIOS_FOLDER = 'scenarios'


class ScenarioHelper:

    def get_all_steps(self, class_node: ast.ClassDef) -> List:
        return [
            element for element in class_node.body if (
                isinstance(element, ast.FunctionDef)
                or isinstance(element, ast.AsyncFunctionDef)
            )
        ]

    def get_when_steps(self, steps: List) -> List:
        return [
            step for step in steps if step.name.startswith('when')
        ]

    def get_assertion_steps(self, steps: List) -> List:
        return [
            step for step in steps if step.name.startswith(('then', 'and', 'but'))
        ]

    def get_assert_statements_from_steps(self, steps: List) -> List[ast.Assert]:
        assert_statements = []
        for step in steps:
            for statement in step.body:
                for statement_node in ast.walk(statement):
                    if isinstance(statement_node, ast.Assert):
                        assert_statements.append(statement_node)
        return assert_statements

    def get_mock_context_managers_from_step(self,
                                            step: FuncType,
                                            mock_name_pattern: str) -> List[Tuple[ast.withitem, int, int]]:
        """
        Returns list of context managers that match mock_name_pattern and their positions (line and column offset).
        """
        mock_context_managers: List[Tuple[ast.withitem, int, int]] = []

        for statement in step.body:
            for statement_node in ast.walk(statement):
                if isinstance(statement_node, (ast.With, ast.AsyncWith)):
                    for item in statement_node.items:
                        if (
                                isinstance(item.context_expr, ast.Call)
                                and isinstance(item.context_expr.func, ast.Name)
                                and re.search(mock_name_pattern, item.context_expr.func.id)
                        ):
                            mock_context_managers.append((item, statement.lineno, statement.col_offset))

        return mock_context_managers
