import requests
import json
from bot.models import Log
from lxml import html, etree
from lxml.etree import XPathSyntaxError, XPathEvalError
from lxml.cssselect import CSSSelector, SelectorError, SelectorSyntaxError

SPLIT = 'SPLIT_'
LOOP = 'LOOP_'
COMPARE = 'COMPARE_'
CONCAT = 'CONCAT_'
VAR = 'VAR_'


class Spider(object):
    _all = [
        'xpath', 'css', 'let', 'split', 'concat', 'get', 'replace', 'loop', 'open', 'back'
    ]
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    __vars = {}
    __opened_urls = {}
    tree = None

    def __init__(self, url: str = '', id: int = None, headers: dict = None, type: str = 'main', vars: dict = None):
        self.url = url
        self.id = id

        if type == 'main':
            self.__opened_urls.clear()
            self.__opened_urls.update({type: url})
            if vars is not None:
                self.__vars.update(vars)
            else:
                self.__vars.clear()
        else:
            self.__opened_urls.update({'sub': [].append(url)})
            if vars is not None:
                self.__vars.update(vars)

        if headers is not None:
            self._headers.update(headers)

        Log(bot_id=id, message=f'Bot {id} started working', level='I').save()

    def open(self, part: str):
        """
        Currently in development
        """
        pass

    #     data = part.split()
    #
    #     try:
    #         dataURL = data[0]
    #     except IndexError:
    #         raise BaseException(
    #             "Error in using 'open' - forgot to give a variable or string URL"
    #         )
    #
    #     try:
    #         dataURL = data[0]
    #     except IndexError:
    #         raise BaseException(
    #             "Error in using 'open' - forgot to set a type of URL"
    #         )
    #
    #     if dataURL in self.__vars.keys():
    #         Spider(url=self.__vars[dataURL], type=URLtype, vars=self.get_vars)._get_tree_from_request()
    #     else:
    #         Spider(url=dataURL, type=URLtype, vars=self.get_vars)._get_tree_from_request()

    def back(self, part: str):
        """
        Currently in development
        """
        pass

    #     data = part.split()
    #     linkType = count = None
    #
    #     try:
    #         linkType = data[0]
    #     except IndexError:
    #         pass
    #
    #     try:
    #         count = data[1]
    #     except IndexError:
    #         pass
    #
    #     if linkType is not None:
    #         if linkType in self.__opened_urls.keys() and linkType != 'sub':
    #             Spider(url=self.__opened_urls[linkType], type=URLtype, vars=self.get_vars).__get_tree_from_request()
    #         else:
    #             length = self.__opened_urls[linkType]
    #             Spider(url=self.__opened_urls[linkType][length-1], type=URLtype, vars=self.get_vars)._get_tree_from_request()
    #
    #
    #     if count is not None:
    #         if linkType != 'main':
    #             length = self.__opened_urls['sub']
    #             Spider(url=self.__opened_urls['sub'][length-count], type=URLtype, vars=self.get_vars)._get_tree_from_request()

    def parse(self, data: str):
        lines = data.splitlines()
        loop_data = ''
        for line in lines:
            partial = line.split()
            if line.startswith('loop'):
                loop_data = data[data.find("loop"):data.find("loopend") + len('loopend')]
                if hasattr(self, partial[0]):
                    getattr(self, partial[0])(loop_data)
            else:
                if hasattr(self, partial[0]):
                    getattr(self, partial[0])(' '.join(partial[1:]))

    def __parse_line(self, line: str):
        partial = line.split()
        if hasattr(self, partial[0]):
            getattr(self, partial[0])(' '.join(partial[1:]))

    def get(self, part: str):

        """
        Used to get the value for the specified variable.<br>
        Example: get [VARIABLE_NAME] xpath|[exspression]<br> get [VARIABLE_NAME] css|[exspression] {text} <br><br>

         <b>WARNING:</b> For using <i>xpath</i> or <i>css</i> you need to put '|' between function and expression. Also <i>css</i> function can get type <i>text</i> for geting text node of element/-s -
         recommends using while you want to collect list of variables or please use <i>xpath</i> function.
        """

        Log(bot_id=self.id, message=f'Running "get" function', level='I').save()

        data = part.split(' ', 1)
        # print('get data', data)
        try:
            variable = data[0]
        except:
            Log(bot_id=self.id, message="Error in using 'get' {}".format(data),
                level='E').save()
            return

        temp = data[1].split('|')

        # raise BaseException("Error in using 'get' - forgot to set variable to store {}".format(data))

        type = None

        if hasattr(self, temp[0]):
            try:
                type = temp[2]
            except IndexError:
                pass

            func = getattr(self, temp[0], type)

        if variable in self.__vars.keys():
            self.__vars[VAR + variable] = func(temp[1], type)
        else:
            self.let(' '.join([variable, '1']))
            self.__vars[VAR + variable] = func(temp[1], type)

        Log(bot_id=self.id, message=f'Ending work with "get" function', level='I').save()

    def loop(self, part: str):
        """
        The loop is used to iterate the elements.<br>
        You could access in <i>loop</i> statement to variables: <i>loop_index</i> and
        <i>loop_item</i>.<br><br>
        <b>WARNING:</b> After <i>loopend</i> - variables will be cleared.
        <br>        <br>

        Example:<br>
            loop variable<br>
                ... another list of code ... <br>
            loopend
        """

        Log(bot_id=self.id, message=f'Running "loop" function', level='I').save()

        _local_loop_vars = {

            'index': 0,
            'variable': 0
        }

        lines = part.splitlines()
        data = lines[0].split()
        if data[1] in self.__vars.keys():
            for idx, item in enumerate(self.__vars[data[1]]):
                _local_loop_vars['index'] = idx
                _local_loop_vars['variable'] = item
                self.__vars.update({'loop': _local_loop_vars})

                for line in lines[1:]:
                    if idx == len(self.__vars[data[1]]) - 1:
                        if lines[len(lines) - 1] == 'loopend':
                            Log(bot_id=self.id, message=f'Ending work with "loop" function', level='I').save()
                        return
                    else:
                        self.__parse_line(line)

        else:
            Log(bot_id=self.id, message="Error in using 'loop' - bad variable in line {}".format(lines[0]),
                level='E').save()
            if 'loop' in self.__vars.keys():
                del self.__vars['loop']
            return

    def concat(self, part: str):
        """
        Used to sum up variables.<br>
        Also you will be noticed that you forgot to set variable for saving data.<br><br>
        Example: concat VARIABLE_NAME [variable or any value] .. [] <br>
        You can access CONCAT_save_var.
        """

        Log(bot_id=self.id, message=f'Starting "concat" function', level='I').save()

        data = part.split()
        if data[0].startswith('VAR') or data[0].isdigit():
            Log(bot_id=self.id, message='Forgotten to set variable to store the result or store variable is digit',
                level='E').save()
            return

        result = ''
        for i in data[1:]:
            if i in self.__vars.keys():
                result += self.__vars[i]
            else:
                result += str(i)

        self.__vars[CONCAT + data[0]] = result

        Log(bot_id=self.id, message=f'Ending work with "concat" function', level='I').save()

    def split(self, part: str):
        """
        Used to split variable.<br>
        Also you will be noticed that you forgot to set variable for saving data.<br><br>
        Example: split VARIABLE_NAME separator <br>
        You can access SPLIT_VARIABLE_NAME_[id of element].
        """

        Log(bot_id=self.id, message=f'Starting "split" function', level='I').save()

        result = []
        data = part.split()
        if data[0] in self.__vars.keys():
            result = self.__vars[data[0]].split(data[1])
            for idx, item in enumerate(result):
                self.__vars.update({
                    SPLIT + data[0] + '_' + str(idx): item
                })
        else:

            Log(bot_id=self.id,
                message='Error in using "split" function - {}. You forgot to set variable to store'.format(part),
                level='E').save()
            return

        Log(bot_id=self.id, message=f'Ending work with "split" function', level='I').save()

    def replace(self, part: str):
        """
        Used to replace part data in variable.<br>
        Also you can got exeption and you will be know where mistake.<br><br>
        Example: replace VAR_VARIABLE_NAME string_to_replace new_data<br>
        You can access to the variable with the same name VAR_VARIABLE_NAME.<br>
        <br>
        <b>WARNING:</b> You need to use already declared variable.
        """

        Log(bot_id=self.id, message=f'Starting "replace" function', level='I').save()

        data = part.split()

        if data[0] in self.__vars.keys():
            ms = self.__vars[data[0]]
        else:

            Log(bot_id=self.id,
                message='Error in using "replace" function - {}. You forgot to use variable'.format(part),
                level='E').save()
            return

        try:
            old = data[1]
        except IndexError:

            Log(bot_id=self.id,
                message='Error in using "replace" function - {}. You forgot to set string that wil be replaced'.format(
                    part),
                level='E').save()
            return
        try:
            new = data[2]
        except IndexError:

            Log(bot_id=self.id,
                message='Error in using "replace" function - {}. You forgot to set string for replacing'.format(part),
                level='E').save()
            return

        ns = ms.replace(old, new)
        self.__vars[data[0]] = ns

        Log(bot_id=self.id, message=f'Ending work with "replace" function', level='I').save()

    def let(self, part: str):

        """
        Used to create variables and set values ​​for them.<br>
        If part of <i>let</i> function will have a third element - raised error of using.
        <br><br>
        Example: let [VARIABLE_NAME] [value]
        <br>
        You can access using VAR_[VARIABLE_NAME]
        """

        Log(bot_id=self.id, message=f'Starting "let" function', level='I').save()

        data = part.split(' ', 1)

        if len(data) >= 3:
            Log(bot_id=self.id,
                message='Error in using "let" function - {}, A lot of args'.format(part),
                level='E').save()
            return
        else:
            # print(data)
            if 'index' in data[1]:
                name = data[0]
                value = self.__vars['loop']['index']
            elif 'item' in data[1]:
                name = data[0]
                value = self.__vars['loop']['variable']
            else:
                name = data[0]
                value = data[1]

        self.__vars[VAR + name] = value

        Log(bot_id=self.id, message=f'Ending work with "let" function', level='I').save()

    def _get_tree_from_request(self):

        Log(bot_id=self.id, message=f'Starts to get HTML document', level='I').save()

        """
        Method returns object of 'tree' of HTML page by GET method
        """
        resp = requests.get(self.url, headers=self._headers)
        content = resp.content
        self.tree = html.fromstring(content)

        Log(bot_id=self.id, message=f'HTML document succesfully getted', level='I').save()

    @property
    def get_vars(self):
        return self.__vars

    @property
    def get_all_funcs(self):
        return self._all

    @property
    def get_opened_urls(self):
        return self.__opened_urls

    def xpath(self, expression, type=None):
        """
        Used to extract an item or list of items from a page using a special expression.<br>
        Or you can got exception of syntax error or namespace error.<br>
        <a target='_blank' href='https://www.w3schools.com/xml/xpath_intro.asp'>More about XPath</a>
        """
        Log(bot_id=self.id, message=f'Starts "xpath" function', level='I').save()

        try:
            element = self.tree.xpath(expression)
        except (XPathSyntaxError, XPathEvalError) as error:
            Log(bot_id=self.id, message='XPath error - {}'.format(error), level='E').save()
            return

        Log(bot_id=self.id, message=f'Ending work with "xpath" function', level='I').save()
        print(element)
        if len(element) == 1:
            return element[0]
        else:
            return element

    def css(self, expression, type=None):
        """
        Used to extract an item or list of items from a page using a special expression.<br>
        Or you can got exception of syntax error or selector error.<br>
        <a target='_blank' href='https://www.w3schools.com/cssref/css_selectors.asp'>More about CSS Selectors</a>
        """

        Log(bot_id=self.id, message=f'Starts "css" function', level='I').save()

        try:
            element = self.tree.cssselect(expression)
        except (SelectorError, SelectorSyntaxError) as error:
            Log(bot_id=self.id, message='CSS selector error - {}'.format(error), level='E').save()
            return

        Log(bot_id=self.id, message=f'Ending work with "css" function', level='I').save()
        print(element)
        if len(element) == 1:
            return element[0]
        else:
            if type is None:
                return [(x.get('href')).strip() for x in element]
            elif type == 'text':
                return [(x.text).strip() for x in element]

    @property
    def html_to_string(self):
        return etree.tostring(self.__get_tree_from_request())

    @property
    def data_to_json(self):
        if 'loop' in self.__vars.keys():
            del self.__vars['loop']
        Log(bot_id=self.id, message='Saving data..', level='I').save()
        result = json.dumps(self.get_vars, ensure_ascii=False)

        return result
