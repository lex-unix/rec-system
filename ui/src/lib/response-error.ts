export class ResponseError extends Error {
  status: number;
  error: string | Record<string, string>;

  constructor(status: number, error: string | Record<string, string>) {
    super(`Response error: ${status}`);
    this.status = status;
    this.error = error;
  }

  isUnauthorized(): this is { error: string } {
    return this.status === 401;
  }

  isFormError(): this is { error: Record<string, string> } {
    return this.status === 422;
  }

  isServerError(): this is { error: string } {
    return this.status >= 500;
  }

  isNotFoundError(): this is { error: string } {
    return this.status === 404;
  }
}
