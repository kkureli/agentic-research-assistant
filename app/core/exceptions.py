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


class UnauthorizedError(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="unauthorized",
            message="Invalid or missing API key.",
            status_code=401,
        )


class RateLimitError(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="rate_limit_exceeded",
            message="Rate limit exceeded. Try again later.",
            status_code=429,
        )


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
