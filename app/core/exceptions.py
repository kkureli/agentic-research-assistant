class AppError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 500,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ResearchTimeoutError(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="timeout",
            message="The research request timed out.",
            status_code=504,
        )


class AgentMaxStepsError(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="agent_max_steps",
            message="The research agent exceeded its maximum number of steps.",
            status_code=504,
        )
