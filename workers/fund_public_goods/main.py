try:
  import unzip_requirements # type: ignore
except ImportError:
  pass


import sys

# Check if the platform is Linux
if sys.platform == "linux":
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from dotenv import load_dotenv
from fastapi import FastAPI
import inngest.fast_api
from mangum import Mangum
from fund_public_goods.inngest_client import inngest_client
from fund_public_goods.workflows.index_gitcoin.functions import functions as gitcoin_functions
from fund_public_goods.api import runs, run, funding_entries
from fund_public_goods.get_version import router as get_version_router

load_dotenv()

app = FastAPI()

inngest.fast_api.serve(app, inngest_client, [*gitcoin_functions])
app.include_router(runs.router)
app.include_router(run.router)
app.include_router(funding_entries.router)
app.include_router(get_version_router)

handler = Mangum(app=app)
