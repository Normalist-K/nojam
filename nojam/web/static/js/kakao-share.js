/**
 * 카카오톡 공유 기능 구현
 * 
 * 심리테스트 결과를 카카오톡으로 공유하는 기능을 제공합니다.
 * 각 결과 유형별로 맞춤형 메시지를 생성하고 사용자 행동을 추적합니다.
 */

class KakaoShareManager {
    constructor() {
        this.isInitialized = false;
        this.init();
    }

    /**
     * 카카오 SDK 초기화 상태 확인
     */
    init() {
        // DOM이 로드된 후 초기화 확인
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.checkSDKInitialization();
            });
        } else {
            this.checkSDKInitialization();
        }
    }

    /**
     * SDK 초기화 상태 확인
     */
    checkSDKInitialization() {
        this.initAttempts = (this.initAttempts || 0) + 1;
        
        if (typeof Kakao !== 'undefined' && Kakao.isInitialized()) {
            this.isInitialized = true;
            console.log('Kakao SDK is ready for sharing');
        } else if (this.initAttempts < 5) {
            console.warn(`Kakao SDK is not initialized (attempt ${this.initAttempts}/5)`);
            // 1초 후 다시 확인 (최대 5회)
            setTimeout(() => {
                this.checkSDKInitialization();
            }, 1000);
        } else {
            console.error('Kakao SDK initialization failed after 5 attempts');
        }
    }

    /**
     * 결과 페이지에서 공유 버튼 클릭 시 호출되는 메인 함수
     * @param {Object} resultData - 공유할 결과 데이터
     */
    shareResult(resultData) {
        if (!this.isInitialized) {
            console.error('Kakao SDK is not initialized');
            this.logShareEvent('share_fail', 'kakao', resultData.quizId, resultData.resultType, {
                error: 'SDK not initialized'
            });
            return;
        }

        // 공유 클릭 이벤트 로깅
        this.logShareEvent('share_click', 'kakao', resultData.quizId, resultData.resultType);

        // 공유 메시지 생성
        const shareMessage = this.createShareMessage(resultData);

        // 카카오톡 공유 실행
        try {
            Kakao.Share.sendDefault({
                objectType: 'feed',
                content: {
                    title: shareMessage.title,
                    description: shareMessage.description,
                    imageUrl: shareMessage.imageUrl,
                    link: {
                        mobileWebUrl: shareMessage.link,
                        webUrl: shareMessage.link
                    }
                },
                buttons: [
                    {
                        title: '나도 테스트하기',
                        link: {
                            mobileWebUrl: shareMessage.quizLink,
                            webUrl: shareMessage.quizLink
                        }
                    }
                ],
                // 공유 성공/실패 콜백
                success: () => {
                    this.logShareEvent('share_success', 'kakao', resultData.quizId, resultData.resultType);
                    // GA4 이벤트 전송
                    this.sendGA4Event('share', {
                        method: 'kakao',
                        content_type: 'quiz_result',
                        item_id: resultData.quizId,
                        custom_parameters: {
                            result_type: resultData.resultType
                        }
                    });
                },
                fail: (error) => {
                    this.logShareEvent('share_fail', 'kakao', resultData.quizId, resultData.resultType, {
                        error: error.message || 'Unknown error'
                    });
                    console.error('Kakao share failed:', error);
                }
            });
        } catch (error) {
            this.logShareEvent('share_fail', 'kakao', resultData.quizId, resultData.resultType, {
                error: error.message || 'Exception occurred'
            });
            console.error('Kakao share exception:', error);
        }
    }

    /**
     * 결과 데이터를 바탕으로 공유 메시지 생성
     * @param {Object} resultData - 결과 데이터
     * @returns {Object} 공유 메시지 객체
     */
    createShareMessage(resultData) {
        const baseUrl = window.location.origin;
        const currentUrl = window.location.href;
        
        // UTM 파라미터 추가
        const shareUrl = this.addUTMParams(currentUrl, 'kakao');
        const quizUrl = this.addUTMParams(`${baseUrl}/quiz?quiz_id=${resultData.quizId}`, 'kakao');

        // 기본 메시지 템플릿
        const defaultMessage = {
            title: `🎯 ${resultData.title}`,
            description: `${resultData.description}\n\n${resultData.keywords ? resultData.keywords.join(' · ') : ''}`,
            imageUrl: resultData.imageUrl || `${baseUrl}/static/images/default-share.png`,
            link: shareUrl,
            quizLink: quizUrl
        };

        // 결과 유형별 맞춤 메시지 (필요시 확장)
        const customMessages = {
            '7080': {
                title: '🎵 나는 7080 감성형!',
                description: '향수와 낭만을 사랑하는 당신의 마음나이를 확인해보세요!'
            },
            'IMF': {
                title: '💪 나는 IMF 생존형!',
                description: '위기를 기회로 바꾸는 당신의 강인한 정신력을 확인해보세요!'
            },
            'MBTI': {
                title: `🧠 나는 ${resultData.resultType}형!`,
                description: '5060 세대를 위한 특별한 MBTI 테스트 결과입니다!'
            }
        };

        // 결과 유형에 맞는 메시지 적용
        const customMessage = customMessages[resultData.resultType] || customMessages['MBTI'];
        
        return {
            ...defaultMessage,
            ...customMessage
        };
    }

    /**
     * URL에 UTM 파라미터 추가
     * @param {string} url - 원본 URL
     * @param {string} source - UTM 소스
     * @returns {string} UTM 파라미터가 추가된 URL
     */
    addUTMParams(url, source) {
        const urlObj = new URL(url);
        urlObj.searchParams.set('utm_source', source);
        urlObj.searchParams.set('utm_medium', 'social');
        urlObj.searchParams.set('utm_campaign', 'result_share');
        return urlObj.toString();
    }

    /**
     * 공유 이벤트 서버 로깅
     * @param {string} eventType - 이벤트 타입
     * @param {string} platform - 플랫폼
     * @param {string} quizId - 퀴즈 ID
     * @param {string} resultType - 결과 유형
     * @param {Object} extra - 추가 데이터
     */
    logShareEvent(eventType, platform, quizId, resultType, extra = {}) {
        // 서버에 이벤트 로깅 요청
        fetch('/api/log-share-event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                event_type: eventType,
                platform: platform,
                quiz_id: quizId,
                result_type: resultType,
                ...extra,
                timestamp: new Date().toISOString(),
                user_agent: navigator.userAgent,
                referrer: document.referrer
            })
        }).catch(error => {
            console.error('Failed to log share event:', error);
        });
    }

    /**
     * GA4 이벤트 전송
     * @param {string} eventName - 이벤트 명
     * @param {Object} parameters - 이벤트 파라미터
     */
    sendGA4Event(eventName, parameters) {
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, parameters);
        } else {
            console.warn('gtag is not available for GA4 event tracking');
        }
    }
}

// 전역 인스턴스 생성
const kakaoShareManager = new KakaoShareManager();

/**
 * 결과 페이지에서 호출할 공유 함수
 * @param {Object} resultData - 공유할 결과 데이터
 */
window.shareKakaoResult = function(resultData) {
    kakaoShareManager.shareResult(resultData);
};

/**
 * 페이지 로드 시 공유 버튼 이벤트 리스너 등록
 */
document.addEventListener('DOMContentLoaded', function() {
    const shareButton = document.getElementById('kakao-share-btn');
    if (shareButton) {
        shareButton.addEventListener('click', function() {
            // 결과 데이터는 HTML에서 주입되거나 전역 변수로 설정
            const resultData = window.quizResultData || {};
            if (Object.keys(resultData).length > 0) {
                window.shareKakaoResult(resultData);
            } else {
                console.error('Quiz result data is not available');
            }
        });
    }
});