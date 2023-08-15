import uvicorn
import sys

if __name__ == '__main__':
    sys.exit(
        uvicorn.run(
            'app.main:app',
            host='0.0.0.0',
            port=8080,
            log_level='info',
            reload=False
        )
    )
