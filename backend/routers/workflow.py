from datetime import date

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from services.BodyBatteryService import BodyBatteryService
from services.SimilaritySearchService import SimilaritySearchService
from services.WorkflowService import WorkflowService

workflow = APIRouter(tags=['Workflow'], prefix='/backend/workflow')
bodyBatteryService = BodyBatteryService()
workflowService = WorkflowService()
similaritySearchService = SimilaritySearchService()


@workflow.get('/init')
async def init(userId: str):
    """
    Initializes the workflow by training the model for the specified user.

    Parameters:
    -----------
    userId : str
        The unique identifier of the user.

    Returns:
    --------
    Response
        HTTP 200 OK upon successful initiation.
    """
    await workflowService.train(userId)
    return Response(status_code=status.HTTP_200_OK)


@workflow.post('/train')
async def train(userId: str):
    """
    Triggers model training explicitly for the specified user.

    Parameters:
    -----------
    userId : str
        The unique identifier of the user.

    Returns:
    --------
    Response
        HTTP 200 OK upon successful training trigger.
    """
    await workflowService.train(userId)
    return Response(status_code=status.HTTP_200_OK)


@workflow.get('/similarity-search')
async def similarity_search(userId: str, targetDate: date):
    """
    Performs a similarity search to find days similar to the given target date for the user.

    Parameters:
    -----------
    userId : str
        The unique identifier of the user.
    targetDate : date
        The target date for similarity comparison.

    Returns:
    --------
    Any
        The result of the similarity computation (typically JSON serializable).
    """
    return await similaritySearchService.compute_distance(userId, targetDate)
