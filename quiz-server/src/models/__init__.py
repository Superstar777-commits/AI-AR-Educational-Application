# import all SQLAlchemy models here so Base.metadata.create_all can find them
from .user_model import users_table
from .question_model import questions_table
from .quiz_model import quizzes_table