/**
 * 온라인 연수 "다음" 버튼 자동 클릭 스크립트
 *
 * 사용법:
 *   1. 브라우저에서 연수 페이지를 연다.
 *   2. F12(개발자 도구) → Console 탭을 연다.
 *   3. 이 스크립트 전체를 복사하여 콘솔에 붙여넣고 Enter를 누른다.
 *   4. 중지하려면 콘솔에 stopAutoClick() 을 입력한다.
 *
 * 설정:
 *   CLICK_INTERVAL_SEC : 클릭 간격(초). 기본 60초.
 */

(function () {
  const CLICK_INTERVAL_SEC = 60;

  // 다음 버튼을 찾기 위한 선택자 및 텍스트 목록
  const BUTTON_SELECTORS = [
    'button',
    'a',
    'input[type="button"]',
    'input[type="submit"]',
    'span[role="button"]',
    'div[role="button"]',
    '.btn',
    '.button',
    '.next',
    '.btn-next',
    '#next',
    '#btn_next',
    '#btnNext',
  ];

  const NEXT_KEYWORDS = [
    '다음',
    '다음으로',
    '다음 화면',
    '다음화면',
    '다음페이지',
    '다음 페이지',
    'next',
    'Next',
    'NEXT',
    '넘어가기',
    '계속',
    '진행',
  ];

  function findNextButton() {
    for (const selector of BUTTON_SELECTORS) {
      const elements = document.querySelectorAll(selector);
      for (const el of elements) {
        const text = (el.textContent || el.value || '').trim();
        const title = (el.getAttribute('title') || '').trim();
        const alt = (el.getAttribute('alt') || '').trim();

        for (const keyword of NEXT_KEYWORDS) {
          if (text.includes(keyword) || title.includes(keyword) || alt.includes(keyword)) {
            // 숨겨져 있거나 비활성화된 버튼은 건너뛴다
            if (el.disabled) continue;
            const style = window.getComputedStyle(el);
            if (style.display === 'none' || style.visibility === 'hidden') continue;

            return el;
          }
        }
      }
    }

    // iframe 내부도 탐색 (같은 도메인일 경우)
    const iframes = document.querySelectorAll('iframe');
    for (const iframe of iframes) {
      try {
        const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        for (const selector of BUTTON_SELECTORS) {
          const elements = iframeDoc.querySelectorAll(selector);
          for (const el of elements) {
            const text = (el.textContent || el.value || '').trim();
            for (const keyword of NEXT_KEYWORDS) {
              if (text.includes(keyword)) {
                if (el.disabled) continue;
                const style = iframe.contentWindow.getComputedStyle(el);
                if (style.display === 'none' || style.visibility === 'hidden') continue;
                return el;
              }
            }
          }
        }
      } catch (e) {
        // cross-origin iframe는 접근 불가 — 무시
      }
    }

    return null;
  }

  function clickNext() {
    const btn = findNextButton();
    if (btn) {
      btn.click();
      const now = new Date().toLocaleTimeString();
      console.log(`[${now}] ✔ "${(btn.textContent || btn.value || '').trim()}" 버튼 클릭 완료`);
    } else {
      const now = new Date().toLocaleTimeString();
      console.log(`[${now}] ⏳ 다음 버튼을 찾지 못했습니다. 다음 주기에 다시 시도합니다.`);
    }
  }

  // 기존 타이머가 있으면 중지
  if (window._autoClickTimer) {
    clearInterval(window._autoClickTimer);
  }

  // 시작
  console.log(`🚀 자동 클릭 시작! (${CLICK_INTERVAL_SEC}초 간격)`);
  console.log('   중지하려면: stopAutoClick()');
  clickNext(); // 즉시 1회 실행
  window._autoClickTimer = setInterval(clickNext, CLICK_INTERVAL_SEC * 1000);

  // 전역 중지 함수
  window.stopAutoClick = function () {
    clearInterval(window._autoClickTimer);
    window._autoClickTimer = null;
    console.log('⛔ 자동 클릭이 중지되었습니다.');
  };
})();
