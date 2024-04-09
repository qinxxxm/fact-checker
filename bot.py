import asyncio
import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, PollHandler, filters, ContextTypes
from config import BOT_TOKEN, FACT_CHECKER_GROUP_ID

# Dictionary to store active polls and their expiration times
active_polls = {}


# TODO: Integrate ChatGPT for fact-checking, now its just a placeholder function
async def chatgpt_fact_check(message: str) -> str:
    # Placeholder function for ChatGPT integration
    response = "This is a placeholder response from ChatGPT."
    return response

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me. I am a fact checker. Send a message to fact check.')

async def process_factcheck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    # Fact-check the user message using ChatGPT
    chatgpt_response = await chatgpt_fact_check(user_message)

    # Notify the user about the results from ChatGPT and inform about further fact-checking
    await update.message.reply_text(
         f'This is the result of fact-checking with ChatGPT:\n\n{chatgpt_response}\n\n'
        'Meanwhile, we will also fact-check with real people.'
    )
    
    # Start a poll in a specified group
    poll_message = await context.bot.sendPoll(
        chat_id = FACT_CHECKER_GROUP_ID,
        question = f"Is this true or false?\n\n{user_message}",
        options = ['True', 'False'],
        is_anonymous = False,
        allows_multiple_answers = False,
        open_period = 15  # 15 seconds
    )

     # Store the poll message ID along with the user ID
    active_polls[poll_message.poll.id] = {
        'user_id': update.message.from_user.id,
        'original_message': user_message,
        'expiration_time': datetime.datetime.now() + datetime.timedelta(seconds=25),  # 10 second buffer
        'true_count': 0,
        'false_count': 0
    }

    print("poll id is", poll_message.poll.id)

async def check_expired_polls(bot):
    while True:
        print("entered check_expired_polls")
        now = datetime.datetime.now()
        expired_polls = [poll_id for poll_id, poll_data in active_polls.items() if poll_data['expiration_time'] < now]
        print("expiredpolls", expired_polls)
        for poll_id in expired_polls:
            poll_data = active_polls.pop(poll_id)
            user_id = poll_data['user_id']
            original_message = poll_data['original_message']
            true_count = poll_data['true_count']
            false_count = poll_data['false_count']
            
            # Calculate the percentage of truth
            total_votes = true_count + false_count
            if total_votes > 0:
                percentage_true = (true_count / total_votes) * 100
                reply_message = (
                    f'The poll for the message: {original_message} has ended.\n\n'
                    f'Here are the results:\n'
                    f'True: {true_count} votes\n'
                    f'False: {false_count} votes\n'
                    f'Truth percentage of message is is {percentage_true:.2f}%'
                )
            else:
                reply_message = f"Sorry, no one replied to the poll for the following message:\n\n{original_message}"
            
            # Send the results back to the user
            await bot.send_message(chat_id=user_id, text=reply_message)
        await asyncio.sleep(10)

async def handle_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Retrieve poll object from update
    print("Entered handle_poll")
    poll = update.poll
    print("Poll:", poll)
    # Get the user ID and original message associated with this poll
    poll_data = active_polls[poll.id]
    print("Poll data:", poll_data)
    # Calculate the total count of "True" and "False" votes
    # Extract options and voter count
    options = {option.text: option.voter_count for option in poll.options}
    # Update the counts in the active_polls dictionary
    poll_data['true_count'] = options.get('True', 0)
    poll_data['false_count'] = options.get('False', 0)
    print("Updated poll counts in active polls:", poll_data)


if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~ filters.COMMAND , process_factcheck))
    app.add_handler(PollHandler(handle_poll)) # We will use this to send the poll result after each user adds to the poll, as i cant seem to find a method to get the poll results from the poll message id after it expires
     
    loop = asyncio.get_event_loop() # Create a task for the check_expired_polls coroutine and run it in the event loop
    check_expired_polls_task = loop.create_task(check_expired_polls(app.bot))
    print("Polling...")
    app.run_polling()


