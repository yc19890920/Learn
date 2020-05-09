from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from lvt.settings import PROJECT_NAME, DEBUG, VERSION, ALLOWED_HOSTS, API_PREFIX
from lvt.router import router as api_router
from lvt_core.events import create_start_app_handler, create_stop_app_handler
from lvt_core.errors.http import http_error_handler
from lvt_core.errors.validation import http422_error_handler


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册应用事件的处理，默认的启动和关闭的监听
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    # 注册默认的路由
    application.include_router(api_router, prefix=API_PREFIX)

    return application


app = get_application()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
