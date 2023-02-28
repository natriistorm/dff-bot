import re

from dff.script import Context, Actor, TRANSITIONS, RESPONSE, Message
import dff.script.conditions as cnd
import dff.script.responses as rsp
import dff.script.labels as lbl


def user_asked_how_bot(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = ctx.last_request
    if request is None or request.text is None:
        return False
    return "how are you" in request.text.lower()


def user_replied_about_themselves(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = ctx.last_request
    if request is None or request.text is None:
        return False
    return "i am" in request.text.lower() or "i'm" in request.text.lower()


def hi_lower_case_condition(ctx: Context, actor: Actor, *args, **kwargs) -> bool:
    request = ctx.last_request
    if request is None or request.text is None:
        return False
    return "hi" in request.text.lower()


def cannot_talk_about_topic_response(ctx: Context, actor: Actor, *args, **kwargs) -> Message:
    request = ctx.last_request
    if request is None or request.text is None:
        topic = None
    else:
        topic_pattern = re.compile(r"(.*talk about )(.*)")
        topic = topic_pattern.findall(request.text)
        topic = topic and topic[0] and topic[0][-1]
    if topic:
        return Message(text=f"Sorry, I can not talk about {topic} now.")
    else:
        return Message(text="Sorry, I can not talk about that now.")


general_script = {
    "greeting_flow": {
        "start_node": {
            RESPONSE: Message(),
            TRANSITIONS: {"node1": cnd.any([hi_lower_case_condition, cnd.exact_match(Message(text="/start"))])},
        },
        "node1": {
            RESPONSE: rsp.choice(
                [Message(text="Hi, how you're doin?"), Message(text="Hello, how are you?")]
            ),
            TRANSITIONS: {"node2_1": cnd.all([user_asked_how_bot, user_replied_about_themselves]),
                          "node2_2": cnd.any([user_replied_about_themselves])
                          },
        },
        "node2_1": {
            RESPONSE: Message(text="I am good, thank you!"),
            TRANSITIONS: {"node3": cnd.regexp(r"talk", re.IGNORECASE)},
        },
        "node2_2": {
            RESPONSE: Message(text="Nice. What do you want to talk about?"),
            TRANSITIONS: {"node4_1": cnd.regexp(r"science", re.IGNORECASE),
                          "node4_2": cnd.true()},
        },
        "node3": {
            RESPONSE: Message(text="Yeah, right. What do you want to talk about?"),
            TRANSITIONS: {"node4_1": cnd.regexp(r"science", re.IGNORECASE),
                          "node4_2": cnd.true()},
        },
        "node4_1": {
            RESPONSE: Message(text="Yeah, let's talk about science! What branch of it you are interested of?"),
            TRANSITIONS: {"node5_1": cnd.regexp("math", re.IGNORECASE),
                          "node4_2": cnd.true()},
        },
        "node4_2": {
            RESPONSE: cannot_talk_about_topic_response,
            TRANSITIONS: {"node6": cnd.regexp("bye", re.IGNORECASE)},
        },
        "node5_1": {
            RESPONSE: Message(text="You can use three cuts to a cake and get 8 pieces."),
            TRANSITIONS: {lbl.forward(): cnd.regexp(r"next", re.IGNORECASE),
                          lbl.repeat(): cnd.regexp(r"repeat", re.IGNORECASE),
                          lbl.to_fallback(): cnd.true()},
        },
        "node5_2": {
            RESPONSE: Message(
                text="“Forty” is the only number that is spelt with letters arranged in alphabetical order."),
            TRANSITIONS: {lbl.forward(): cnd.regexp(r"next", re.IGNORECASE),
                          lbl.repeat(): cnd.regexp(r"repeat", re.IGNORECASE),
                          lbl.to_fallback(): cnd.true()},
        },
        "node5_3": {
            RESPONSE: Message(
                text="Conversely, “one” is the only number that is spelt with letters arranged in descending order."),
            TRANSITIONS: {lbl.backward(): cnd.regexp(r"previous", re.IGNORECASE),
                          lbl.forward(): cnd.regexp(r"next", re.IGNORECASE),
                          lbl.repeat(): cnd.regexp(r"repeat", re.IGNORECASE),
                          lbl.to_fallback(): cnd.true()},
        },
        "node5_4": {
            RESPONSE: Message(
                text="That's all I know."),
            TRANSITIONS: {lbl.backward(): cnd.regexp(r"previous", re.IGNORECASE),
                          "node6": cnd.true()},
        },
        "node6": {
            RESPONSE: Message(text="Goodbye"),
            TRANSITIONS: {
                "node1": cnd.any([hi_lower_case_condition, cnd.exact_match(Message(text="/start"))])
            },
        },
        "fallback_node": {
            RESPONSE: Message(text="Ooops"),
            TRANSITIONS: {
                "node1": cnd.any([cnd.exact_match(Message(text="/start")), hi_lower_case_condition]),
                "fallback_node": cnd.true(),
            },
        },
    }
}
