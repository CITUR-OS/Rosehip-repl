from markdown2 import Markdown;import os;os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide";import html2text,pygame_gui,pygame,requests;from urllib.parse import urljoin
class Webbrowser(pygame_gui.elements.UIWindow):
    def __init__(self, pos, manager):self.MOUSE_BUTTONS = {'SCROLL_WHEEL_UP': 4,'SCROLL_WHEEL_DOWN': 5,'BACK_BUTTON': 8,'FORWARD_BUTTON': 9};self.REPLACE_MAP_STRIPPED_HTML = {'-ROBRACKET-': '(','-RCBRACKET-': ')','-EOBRACKET-': '[','-ECBRACKTE-': ']','\t': '&nbsp;&nbsp;&nbsp;&nbsp;',"\n": '<br>',"<p>": '',"<\p>": "<br>","<ul>": "","</ul>": "","<li>": "* ","</li>": "<br>","<h1>": "<b>","</h1>": "</b>","<h2>": "<b>","</h2>": "</b>","<h>": "<b>","</h1>": "</b>","<blockquote>": "<i>","</blockquote>": "</i>"};self.REPLACE_MAP_FULL_HTML = {'(': '-ROBRACKET-',')': '-RCBRACKET-','[': '-EOBRACKET-',']': '-ECBRACKTE-'};super().__init__(pygame.Rect(pos, (600, 400)),manager,window_display_title="Webbrowser",object_id="#webbrowser",resizable=True,);self.current_base_url = str();self.x_position = 0;self.url_history_stack = [];self.url_history_stack_pointer = 0;self.is_newly_entered_url = False;self.page_cache = {};self.markdowner = Markdown();self.page_content = pygame_gui.elements.UITextBox("",relative_rect=pygame.Rect(0, 35, 568, 300),manager=manager,container=self,anchors={"left": "left","right": "right","top": "top","bottom": "bottom",},);self.input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(0, -337, 568, 30),manager=manager,container=self,anchors={"left": "left","right": "right","top": "bottom","bottom": "bottom",},);self.input.focus()
    def process_string_with_map(self, string, map):
        result_string = string
        for key in map:result_string = result_string.replace(key, map[key])
        return result_string
    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:self.is_newly_entered_url = True;input_url = ('http' not in self.input.get_text())*'https://www.google.com/search?lang=en&q='+self.input.get_text();self.perform_browsing(input_url.lower());self.url_history_stack = self.url_history_stack[0:self.url_history_stack_pointer]
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:self.handle_link_click(event.link_target)
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:position_update_requested = False
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP and event.button == self.MOUSE_BUTTONS['BACK_BUTTON'] and self.url_history_stack_pointer != 0:self.url_history_stack_pointer -= 1;self.perform_browsing(self.url_history_stack[self.url_history_stack_pointer])
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP and event.button == self.MOUSE_BUTTONS['FORWARD_BUTTON'] and (len(self.url_history_stack) - 1) > self.url_history_stack_pointer:self.url_history_stack_pointer += 1;self.perform_browsing(self.url_history_stack[self.url_history_stack_pointer])
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP and event.button == self.MOUSE_BUTTONS['SCROLL_WHEEL_UP'] and self.x_position != 0:self.x_position -= 1;position_update_requested = True
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP and event.button == self.MOUSE_BUTTONS['SCROLL_WHEEL_DOWN']:self.x_position += 1;position_update_requested = True
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP and(self.page_content.scroll_bar is not None) and position_update_requested:self.page_content.scroll_bar.scroll_position = self.x_position;self.page_content.scroll_bar.scroll_wheel_down = True
    def handle_link_click(self, url):url = f"{self.current_base_url}{url}".replace("//", "/").replace(":/", "://").replace("<br>", "") if (self.current_base_url not in url) and ('://' not in url) else url;self.is_newly_entered_url = True;self.perform_browsing(url)
    def render_links(self, stripped_html, base_url):return self.markdowner.convert(stripped_html)
    def perform_browsing(self, url):
        url = url.replace("<br>", "");self.input.set_text(url);self.page_content.html_text = str();self.page_content.rebuild()
        if url.lower() in self.page_cache:stripped_html = self.page_cache[url.lower()]
        else:
            try:
                r = requests.get(url, allow_redirects=True);r.close()
                if r.status_code == 200:html_content = r.content.decode('UTF-8');html_content = self.process_string_with_map(html_content, self.REPLACE_MAP_FULL_HTML);stripped_html = html2text.html2text(html_content);stripped_html = self.render_links(stripped_html, self.current_base_url);stripped_html = str(self.process_string_with_map(stripped_html, self.REPLACE_MAP_STRIPPED_HTML))
                else:stripped_html = f"Error {r.status_code} code"
            except:stripped_html = "Error 404 code"
        self.current_base_url = urljoin(url, '.')
        if self.is_newly_entered_url:self.url_history_stack.append(url);self.url_history_stack_pointer += 1;self.is_newly_entered_url = False;self.page_content.html_text = stripped_html;self.page_content.rebuild();self.page_cache[url.lower()] = stripped_html;self.x_position = 0
def load(manager, params):pos = (100, 100);pos = params[0] if params is not None and len(params) > 0 else pos;Webbrowser(pos, manager)
