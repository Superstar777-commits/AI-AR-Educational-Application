"""
    Service for ML model
    Contains all the logic for the ml_router
"""

from typing import Optional, List, Dict, Any
import pandas as pd
# all the relevant schemas
from src.api.schemas.analysis_schema import AnalysisCreate, AnalysisResponse
from src.api.schemas.answer_schema import AnswerResponse
from src.api.schemas.log_schema import LogResponse
from src.api.schemas.question_schema import QuestionResponse
from src.api.schemas.user_schema import UserResponse

from src.ml_core.data_processing import DataPrepocessor

# repositories
from src.repositories.analysis_repository import AnalysisRepository
from src.repositories.answer_repository import AnswerRepository
from src.repositories.log_repository import LogRepository
from src.repositories.question_repository import QuestionRepository
from src.repositories.user_repository import UserRepository
from src.repositories.quiz_repository import QuizRepository

class MLService:
    def __init__(self, analysis_repo: AnalysisRepository, answer_repo: AnswerRepository, log_repo: LogRepository, question_repo: QuestionRepository, user_repo: UserRepository, quiz_repo: QuizRepository) -> None:
        self.preprocessor = DataPrepocessor()
        self.analysis_repo = analysis_repo
        self.answer_repo = answer_repo
        self.log_repo = log_repo
        self.question_repo = question_repo
        self.user_repo = user_repo
        self.quiz_repo = quiz_repo

    # functions for the machine learning model e.g. sentiment analysis, classification
    async def analyse(self, id: int, skip: int = 0, limit: int = 10, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        # initialise the list of dataframes
        dfs: List[pd.DataFrame] = []
        # if the user_id query exists
        if user_id is not None:
            user = await self.user_repo.get_user_by_id(user_id)
            # if the user exists
            if(user is not None):
                u_answers = await self.answer_repo.get_answers_by_user_and_quiz_id(user["id"], id, skip=skip, limit=limit)
                if len(u_answers) == 0:
                    return []
                u_logs = await self.log_repo.get_logs_by_user_id(user["id"], skip=skip, limit=limit)
                if len(u_logs) == 0:
                    return []
                singular_df = self.preprocessor.convert_to_df(user=user, answers=u_answers, logs=u_logs)
                dfs.append(singular_df)
            # else return an empty array
            else:
                return []
        # if the user_id query doesn't exist
        else:
            print("Getting by all users")
            users = await self.user_repo.get_users()
            for user in users:
                u_answers = await self.answer_repo.get_answers_by_user_and_quiz_id(user["id"], id)
                # if there are no answers or logs, skip to the next user
                # otherwise will cause an error with Pandas
                # TODO: Create a "no answers" and "no logs" placeholder
                if len(u_answers) == 0:
                    continue
                # go through each answer and get every log that matches the answer's question
                for u_answer in u_answers:
                    u_logs = await self.log_repo.get_logs_by_user_id(user["id"], question_id=u_answer["question_id"])
                    if len(u_logs) == 0:
                        continue
                    singular_df = self.preprocessor.convert_to_df(user=user, answers=u_answers, logs=u_logs)
                    print(singular_df.head())
                    dfs.append(singular_df)
        # if the dataframes exist, create one dataframe
        if len(dfs) > 0:
            df = pd.concat(dfs, ignore_index=True)
        else:
            return []
        # return as list of dicts
        return df.to_dict(orient='records') # type: ignore