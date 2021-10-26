from tracardi.domain.context import Context
from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from tracardi.domain.profile import Profile
from tracardi.domain.session import Session
from tracardi_plugin_sdk.service.plugin_runner import run_plugin
from tracardi_sentiment_analysis.plugin import SentimentAnalysisAction

init = {
    "source": {
        "id": "e7a3979e-7f31-452b-a571-8ca613de77fb"
    },
    "language": "en",
    "text": "This seems awesome, but on the second though it is not."
}
payload = {}
profile = Profile(id="profile-id")
event = Event(id="event-id",
              type="event-type",
              profile=profile,
              session=Session(id="session-id"),
              source=Entity(id="source-id"),
              context=Context())
result = run_plugin(SentimentAnalysisAction, init, payload,
                    profile)

print("OUTPUT:", result.output)
print("PROFILE:", result.profile)
