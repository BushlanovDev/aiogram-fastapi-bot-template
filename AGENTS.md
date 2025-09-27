# Agent Instructions

This is a Telegram bot project.

## Project Structure

The project has a modular structure where each component has a clearly defined responsibility.

- `/bot/callbacks/`: Contains `CallbackData` factories for handling inline button clicks.
- `/bot/configs/`: Manages configuration using `pydantic-settings`. Settings are loaded from environment variables and a
  `.env` file.
- `/bot/handlers/`: The main logic for processing incoming messages and callbacks from Telegram. The `Handlers` class
  contains all the handler methods.
- `/bot/i18n/`: Implements internationalization (i18n). Contains translation files (`ru.py`, `en.py`) and the `Lexicon`
  class for accessing texts in the desired language.
- `/bot/keyboards/`: The `Keyboards` class for generating Reply and Inline keyboards.
- `/bot/middlewares/`: Middleware.
    - `i18n.py`: Determines the user's language.
    - `throttling.py`: Limits the rate of user requests.
    - `context.py`: Gathers dependencies into a single context object.
- `/bot/services/`: The service layer and business logic.
    - `bot_service.py`: An example of a service with business logic (e.g., `upper()`).
    - `context.py`: The `HandlerContext` `dataclass` which aggregates all major dependencies.
- `/bot/states/`: State definitions for the FSM (Finite State Machine) using `StatesGroup`.
- `main.py`: The application's entry point. This is where the initialization of `FastAPI`, the bot, the dispatcher, and
  the registration of all handlers, middlewares, and dependencies occurs.

## Architecture Overview

The project is built on the **aiogram 3**, **FastAPI**, and **Pydantic** stack. It uses webhooks to receive updates from
Telegram, which is the preferred method for a production environment.

### Dependency Injection (DI) with a Context Object

Instead of passing multiple dependencies into each handler, we use a single context object.

**How it works:**

1. **Singleton Initialization:** In `main.py`, within the `register_workflow_data` function, we create a single instance
   of all key services (`Keyboards`, `BotService`, `Lexicon`) and store them in `dp.workflow_data`.
2. **Context Assembly:** The `ContextMiddleware` runs with every incoming update. It retrieves the previously created
   services from `data` and packs them into the `HandlerContext` `dataclass`.
3. **Injection into Handler:** The prepared `ctx: HandlerContext` object is automatically passed as an argument to any
   handler that requests it via a type hint.

**Agent Instruction:**
> When adding new functionality that requires access to services (e.g., a database), follow this
> pattern:
> 1. Create a new service class (e.g., `DatabaseService`).
> 2. Add an instance of it to `workflow_data` in `main.py`.
> 3. Add a new field to the `HandlerContext` `dataclass`.
> 4. Add the initialization for this field in `ContextMiddleware`.
> 5. You can now access your service in any handler via `ctx.database_service`.

### Update Flow

1. Telegram sends a JSON update to the FastAPI endpoint (`/webhook/tg`).
2. The `webhook_handler` in `main.py` validates the data and passes it to `dispatcher.feed_update()`.
3. The dispatcher sequentially runs the **outer middlewares**:
    - `I18nMiddleware` determines the `user_lang`.
    - `ThrottlingMiddleware` checks the request frequency.
    - `ContextMiddleware` assembles the `ctx` object.
4. The dispatcher finds a suitable handler based on filters (`CommandStart`, `F.text`, etc.).
5. The dispatcher calls the found handler, passing it all necessary data, including `message`, `state`, and our `ctx`.

## Coding Style & Naming Conventions

Maintaining a consistent code style is critically important for the project's readability and maintainability.

- **Language:** Python 3.12+, line length 120. Strict typing is non-negotiable.
- **Type Hinting:** **Mandatory.** All new functions, methods, and variables must have strict type annotations. This is
  the foundation for DI and static analysis.
- **Naming:**
    - Classes: `PascalCase` (e.g., `BotService`, `HandlerContext`).
    - Functions, methods, variables: `snake_case` (e.g., `start_command`, `user_lang`).
    - Constants: `UPPER_SNAKE_CASE` (e.g., `LEXICON_RU`).
    - Modules: `snake_case` (e.g., `bot_service.py`).
- **Internationalization:** All user-visible strings (messages, button text) must be moved to the lexicon files in
  `/i18n/` and retrieved using `ctx.lexicon.get_text()`. Do not hardcode strings in handlers and keyboards.
