class Config:
    def __init__(self, is_mock_assert_optional: bool, mock_name_pattern: str):
        self.is_mock_assert_optional = is_mock_assert_optional
        self.mock_name_pattern = mock_name_pattern


class DefaultConfig(Config):
    def __init__(self, is_mock_assert_optional: bool = True, mock_name_pattern: str = r"(?=.*mock)(?!.*grpc)"):
        super().__init__(is_mock_assert_optional=is_mock_assert_optional, mock_name_pattern=mock_name_pattern)
