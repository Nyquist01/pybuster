from fastapi import APIRouter

from ...pybuster.consts import DEFAULT_DIRECTORIES
from ...pybuster.requester import Requester, ResponseResult

router = APIRouter(prefix="/v1.0/scan", tags=["scan"])


@router.post("/", response_model=list[ResponseResult])
async def initiate_scan(target_host: str):
    """Send a request to scan the target host."""
    requester = Requester(target_host=target_host, target_paths=DEFAULT_DIRECTORIES)
    return await requester.enumerate()


@router.get("/{target_host}", response_model=None)
async def get_scan_results(target_host: str):
    """Get scan results for the target host."""
    print(f"Getting results for {target_host}")
    return None


@router.delete("/{target_host}", response_model=None)
async def delete_scan_results(target_host: str):
    """Delete scan results for the target host."""
    print(f"Deleting results for {target_host}")
    return None
