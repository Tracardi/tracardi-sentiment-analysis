import aiohttp
from tracardi.service.storage.helpers.source_reader import read_source
from tracardi_dot_notation.dot_accessor import DotAccessor
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.domain.result import Result
from tracardi_sentiment_analysis.model.configuration import Configuration
from tracardi_sentiment_analysis.model.sa_source_onfiguration import SASourceConfiguration


class SentimentAnalysisAction(ActionRunner):

    @staticmethod
    async def build(**kwargs) -> 'SentimentAnalysisAction':
        plugin = SentimentAnalysisAction(**kwargs)
        source = await read_source(plugin.config.source.id)
        plugin.source = SASourceConfiguration(
            **source.config
        )

        return plugin

    def __init__(self, **kwargs):
        self.source = None
        self.config = Configuration(**kwargs)

    async def run(self, payload):
        dot = DotAccessor(self.profile, self.session, payload, self.event, self.flow)

        async with aiohttp.ClientSession() as session:
            params = {
                "key": self.source.token,
                "lang": self.config.language,
                "txt": dot[self.config.text]
            }
            try:
                async with session.post('https://api.meaningcloud.com/sentiment-2.1', params=params) as response:
                    if response.status != 200:
                        raise ConnectionError("Could not connect to service https://api.meaningcloud.com. "
                                              f"It returned `{response.status}` status.")

                    data = await response.json()
                    if 'status' in data and 'msg' in data['status']:
                        if data['status']['msg'] != "OK":
                            raise ValueError(data['status']['msg'])

                    result = {
                        "sentiment": data['score_tag'],
                        "agreement": data['agreement'],
                        "subjectivity": data['subjectivity'],
                        "confidence": float(data['confidence'])
                    }

                    return Result(port="payload", value=result), Result(port="error", value=None)
            except Exception as e:
                self.console.error(repr(e))
                return Result(port="payload", value=None), Result(port="error", value=str(e))


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_sentiment_analysis.plugin',
            className='SentimentAnalysisAction',
            inputs=["payload"],
            outputs=['payload', 'error'],
            version='0.1',
            license="MIT",
            author="Risto Kowaczewski",
            init={
                "source": {
                    "id": None
                },
                "language": "en",
                "text": None
            }
        ),
        metadata=MetaData(
            name='Sentiment analysis',
            desc='It connects to the service that infers sentiment from a given sentence',
            type='flowNode',
            width=200,
            height=100,
            icon='icon',
            group=["Machine learning"]
        )
    )
