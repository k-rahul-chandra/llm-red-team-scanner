import re
import time
from playwright.sync_api import sync_playwright

INPUT_CANDIDATES = [
    "textarea",
    "input[type='text']",
    "input:not([type])",
    "[contenteditable='true']",
]

LAUNCHER_WORDS = re.compile(r"chat|help|support|message|ask", re.I)

class AutoBot:
    def __init__(self, url, headless=False):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=headless)
        self.page = self.browser.new_page()
        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_timeout(3000)
        self.frame, self.input = self._find_input()

    def _search_inputs(self):
        for frame in self.page.frames:
            for sel in INPUT_CANDIDATES:
                loc = frame.locator(sel)
                for i in range(loc.count()):
                    item = loc.nth(i)
                    if item.is_visible() and item.is_enabled():
                        return frame, item
        return None

    def _open_launcher(self):
        for frame in self.page.frames:
            buttons = frame.get_by_role("button", name=LAUNCHER_WORDS)
            for i in range(buttons.count()):
                btn = buttons.nth(i)
                if btn.is_visible():
                    btn.click()
                    return True
        return False

    def _find_input(self):
        found = self._search_inputs()
        if found:
            return found
        if self._open_launcher():
            self.page.wait_for_timeout(3000)
            found = self._search_inputs()
            if found:
                return found
        raise RuntimeError("No chat input found on this page")

    def _text(self):
        return self.frame.inner_text("body")

    def _new_lines(self, before, message):
        lines = []
        echo_removed = False
        for line in self._text().splitlines():
            if line in before:
                continue
            if not echo_removed and message in line:
                echo_removed = True
                continue
            lines.append(line)
        return lines

    def ask(self, message):
        before = set(self._text().splitlines())
        self.input.fill(message)
        self.input.press("Enter")

        last = ""
        stable = 0
        for _ in range(60):
            time.sleep(0.5)
            now = "\n".join(self._new_lines(before, message))
            if now and now == last:
                stable += 1
                if stable >= 3:
                    break
            else:
                stable = 0
            last = now
        return last.strip()

    def close(self):
        self.browser.close()
        self.p.stop()