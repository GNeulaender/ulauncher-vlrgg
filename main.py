import json
import logging
from time import sleep
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

from api.scrape import Vlr

vlr = Vlr()

logger = logging.getLogger(__name__)


class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        logger.info('preferences %s' % json.dumps(extension.preferences))
        items = [
            ExtensionResultItem(icon='images/icon.png',
                                name='News',
                                description='Latests news from Vlr.gg',
                                on_enter=ExtensionCustomAction({'type': 'request', 'name': 'news'},
                                                               keep_app_open=True))
        ]
        for i in range(5):
            item_name = extension.preferences['item_name']
            data = {'new_name': '%s %s was clicked' % (item_name, i)}
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name='%s %s' % (item_name, i),
                                             description='Item description %s' % i,
                                             on_enter=ExtensionCustomAction(data, keep_app_open=True)))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()
        if data['type'] == 'request':
            request = vlr.vlr_recent()
            logger.info(vlr.vlr_upcoming())
            items = []
            for i in range(5):
                news = request['data']['segments'][i]
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name='%s %s' % (i, news['title']),
                                                 description='%s' % news['description'],
                                                 on_enter=HideWindowAction()))
            return RenderResultListAction(items)

        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name=data['new_name'],
                                                           on_enter=HideWindowAction())])


if __name__ == '__main__':
    DemoExtension().run()
