"""Quiz Loader for JSON-driven platform.

JSON 파일을 로드하고 Pydantic 모델로 파싱하며 메모리 캐시를 제공한다.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from ..models.quiz import Quiz

logger = logging.getLogger(__name__)


class QuizLoader:
    """JSON 기반 퀴즈 로더 및 캐시 관리자."""

    def __init__(self, quiz_dir: str | Path = "assets/quizzes"):
        """
        매개변수
        --------
        quiz_dir : str | Path
            퀴즈 JSON 파일들이 저장된 디렉토리 경로
        """
        self.quiz_dir = Path(quiz_dir)
        self._cache: dict[str, Quiz] = {}
        self._file_timestamps: dict[str, float] = {}

    def load_quiz(self, quiz_id: str, force_reload: bool = False) -> Quiz:
        """퀴즈 JSON 파일을 로드하고 파싱한다.

        매개변수
        --------
        quiz_id : str
            로드할 퀴즈 ID (파일명에서 .json 제외)
        force_reload : bool
            캐시를 무시하고 강제로 다시 로드할지 여부

        반환
        -----
        Quiz
            파싱된 퀴즈 객체

        예외
        ----
        FileNotFoundError
            퀴즈 파일을 찾을 수 없는 경우
        ValueError
            JSON 파싱 또는 Pydantic 검증 실패
        """
        file_path = self.quiz_dir / f"{quiz_id}.json"

        if not file_path.exists():
            raise FileNotFoundError(f"퀴즈 파일을 찾을 수 없습니다: {file_path}")

        # 파일 수정 시간 확인
        current_mtime = file_path.stat().st_mtime
        cached_mtime = self._file_timestamps.get(quiz_id, 0)

        # 캐시된 데이터가 있고 파일이 변경되지 않았으면 캐시 반환
        if (
            not force_reload
            and quiz_id in self._cache
            and current_mtime <= cached_mtime
        ):
            logger.debug(f"캐시에서 퀴즈 반환: {quiz_id}")
            return self._cache[quiz_id]

        # JSON 파일 로드 및 파싱
        try:
            with file_path.open("r", encoding="utf-8") as f:
                raw_data = json.load(f)

            # Pydantic 모델로 검증 및 파싱
            quiz = Quiz.model_validate(raw_data)

            # 캐시 업데이트
            self._cache[quiz_id] = quiz
            self._file_timestamps[quiz_id] = current_mtime

            logger.info(f"퀴즈 로드 완료: {quiz_id} (v{quiz.meta.version})")
            return quiz

        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 파싱 실패: {file_path} - {e}") from e
        except Exception as e:
            raise ValueError(f"퀴즈 검증 실패: {quiz_id} - {e}") from e

    def get_available_quizzes(self) -> list[str]:
        """사용 가능한 퀴즈 ID 목록을 반환한다.

        반환
        -----
        list[str]
            .json 확장자를 제거한 퀴즈 ID 목록
        """
        if not self.quiz_dir.exists():
            return []

        quiz_files = list(self.quiz_dir.glob("*.json"))
        return [f.stem for f in quiz_files]

    def clear_cache(self, quiz_id: str | None = None) -> None:
        """캐시를 비운다.

        매개변수
        --------
        quiz_id : Optional[str]
            특정 퀴즈만 캐시에서 제거. None이면 전체 캐시 비우기
        """
        if quiz_id is None:
            self._cache.clear()
            self._file_timestamps.clear()
            logger.info("전체 퀴즈 캐시 비움")
        elif quiz_id in self._cache:
            del self._cache[quiz_id]
            del self._file_timestamps[quiz_id]
            logger.info(f"퀴즈 캐시 제거: {quiz_id}")

    def get_cache_info(self) -> dict[str, dict]:
        """캐시 상태 정보를 반환한다.

        반환
        -----
        dict[str, dict]
            퀴즈 ID별 캐시 정보 (버전, 로드 시간 등)
        """
        info = {}
        for quiz_id, quiz in self._cache.items():
            info[quiz_id] = {
                "version": quiz.meta.version,
                "title": quiz.meta.title,
                "question_count": quiz.config.question_count,
                "result_types": quiz.config.result_types,
                "cached_at": self._file_timestamps.get(quiz_id, 0),
            }
        return info


# 전역 로더 인스턴스
_loader: QuizLoader | None = None


def get_quiz_loader() -> QuizLoader:
    """전역 QuizLoader 인스턴스를 반환한다.

    싱글턴 패턴으로 구현되어 애플리케이션 전체에서 동일한 로더 인스턴스를 사용한다.

    반환
    -----
    QuizLoader
        전역 로더 인스턴스
    """
    global _loader
    if _loader is None:
        _loader = QuizLoader()
    return _loader
