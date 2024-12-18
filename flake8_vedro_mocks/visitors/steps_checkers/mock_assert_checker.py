from typing import List

from flake8_plugin_utils import Error

from flake8_vedro_mocks.abstract_checkers import StepsChecker
from flake8_vedro_mocks.errors import (
    MockCallResultNotAsserted,
    MockCallResultNotSavedAsSelfAttribute
)
from flake8_vedro_mocks.helpers import (
    is_self_attribute,
    is_self_attribute_asserted
)
from flake8_vedro_mocks.visitors.scenario_visitor import (
    Context,
    ScenarioVisitor
)


@ScenarioVisitor.register_steps_checker
class MockAssertChecker(StepsChecker):

    def check_steps(self, context: Context, config) -> List[Error]:
        errors = []
        when_steps = self.get_when_steps(context.steps)
        assertion_steps = self.get_assertion_steps(context.steps)
        if not when_steps or not assertion_steps:
            return []

        mock_context_managers = self.get_mock_context_managers_from_step(when_steps[0], config.mock_name_pattern)
        for context_manager, lineno, col_offset in mock_context_managers:
            mock_func_name = context_manager.context_expr.func.id
            mock_var = context_manager.optional_vars
            if not is_self_attribute(mock_var):
                errors.append(MockCallResultNotSavedAsSelfAttribute(lineno, col_offset, mock_func_name=mock_func_name))
                continue

            assert_statements = self.get_assert_statements_from_steps(assertion_steps)
            if not is_self_attribute_asserted(assert_statements, mock_var):
                mock_var_name = '{}.{}'.format(mock_var.value.id, mock_var.attr)
                errors.append(MockCallResultNotAsserted(lineno, col_offset, mock_var_name=mock_var_name))

        return errors
