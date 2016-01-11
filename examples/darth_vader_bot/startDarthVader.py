from slackbotReplier import SlackbotReplier

token = ""

def main():
    darthVaderBot = SlackbotReplier(token)
    darthVaderBot.run()

if __name__ == "__main__":
    main()