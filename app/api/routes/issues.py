from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def list_issues():
    return [
        {'id': 1, 'title': 'some title'},
        {'id': 2, 'title': 'another issue'},
    ]
